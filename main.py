import requests
from bs4 import BeautifulSoup
import re
import sys
import os
import customtkinter as ctk

#dictionary for char replacement
replace = {
    "\\n":"",
    "\\r":"\n",
    "[ch]":"",
    "[/ch]":"",
    "[tab]":"",
    "[/tab]":"",
    "\\&quot;":"",
    "'":"'"
}



#---------------
#    FUNCT
#---------------

def rem(testo, sostituzioni):
    righe = testo.splitlines()
    
    righe_modificate = []
    for riga in righe:
        for chiave, valore in sostituzioni.items():
            riga = riga.replace(chiave, valore)
        righe_modificate.append(riga)
    
    # Riassembliamo il testo con le righe modificate
    return '\n'.join(righe_modificate)

def regex(testo, regex_iniziale, regex_finale):
    # Cerca la parte del testo che si trova tra le due regex
    pattern = rf'({regex_iniziale})(.*?){regex_finale}'
    
    # Esegui la ricerca con la regex combinata
    match = re.search(pattern, testo)
    
    if match:
        return match.group(2)
    else:
        return None

def link2title(link):
    frame = link.split('/')
    #print(frame)
    link_content = {
        "site": frame[2],  
        "tab": frame[3],   
        "singer": frame[4],  
        "title": frame[5]  
    }
    return link_content

def log_append(new_text):
    current = label_text.get()
    updated = current + "\n" + new_text
    label_text.set(updated)

def extract (url):
    
    

    #HTML fetch 
    response = requests.get(url)

    if response.status_code != 200:
        print(response.status_code)
        log_append("Page fetch error:" + response.status_code)
        exit()

    log_append("Page fetch status 200 (successfull)")

    #making file title based on link
    name = regex(link2title(url)["title"], "^", "-[0-9]")


    soup = BeautifulSoup(response.text, 'html.parser')

    #writing raw html data (for debug purpose)
    #with open('rawPage_content.html', 'w', encoding='utf-8') as file:
    #    file.write(str(soup))

    #selecting js-store class
    selected_div = soup.find('div', {'class': 'js-store'})

    #searching for text
    section = regex(str(selected_div.prettify()), "\\\\r", "&quot;,")

    #cleaning messy text from special chars
    cleanText = rem(section, replace)

    log_append("Removing useless stuff...")

    #writing text body in the file
    filename = f"./songs/{name}.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(str(cleanText))

    log_append("Done!")
    log_append("File name: "+ name)
    log_append("you can find it in: " + filename + "\n")
    log_append("-----------------------------")

def execute():
    extract(entry.get())



def parse_chords_and_lyrics(tab_block):
    lines = tab_block.strip().split('\n')
    if len(lines) != 2:
        return None  # Ogni blocco deve avere 2 righe: una con gli accordi, una col testo

    chords_line, lyrics_line = lines

    # Trova tutti gli accordi e le loro posizioni nella riga
    chord_matches = list(re.finditer(r'\[ch\](.*?)\[/ch\]', chords_line))
    chords = []
    for i, match in enumerate(chord_matches):
        chord = match.group(1)
        start = match.start()
        # Calcola la distanza in spazi fino al prossimo accordo (escludendo tag)
        if i + 1 < len(chord_matches):
            next_start = chord_matches[i + 1].start()
            spaces = len(re.sub(r'\[ch\].*?\[/ch\]', '', chords_line[match.end():next_start]))
        else:
            spaces = len(re.sub(r'\[ch\].*?\[/ch\]', '', chords_line[match.end():]))
        chords.append((chord, spaces))

    # Calcola offset iniziale ignorando spazi iniziali del testo
    stripped_lyrics = lyrics_line.lstrip()
    initial_offset = len(lyrics_line) - len(stripped_lyrics)
    result_line = stripped_lyrics

    insert_pos = 0
    for chord, space in chords:
        result_line = result_line[:insert_pos] + f"^{{{chord}}}" + result_line[insert_pos:]
        insert_pos += len(f"^{{{chord}}}") + space

    # Riaggiungi gli spazi iniziali originali alla riga modificata
    return ' ' * initial_offset + result_line

def process_song(text):
    tab_blocks = re.findall(r'\[tab\](.*?)\[/tab\]', text, re.DOTALL)
    processed_lines = []

    for block in tab_blocks:
        processed_line = parse_chords_and_lyrics(block)
        if processed_line:
            processed_lines.append(processed_line + "\\\\")

    return "\n".join(processed_lines)

input_text = '''
[ch]Em[/ch]   [ch]A[/ch]
[ch]Em[/ch]   [ch]A[/ch]

[Verse 1]
[tab][ch]Em[/ch]                     [ch]G[/ch]
   All around me are familiar faces[/tab]
[tab][ch]D[/ch]                [ch]A[/ch]
Worn out places, worn out faces[/tab]
[tab][ch]Em[/ch]                            [ch]G[/ch]
   Bright and early for their daily races[/tab]
[tab][ch]D[/ch]              [ch]A[/ch]
Going nowhere, going nowhere[/tab]
[tab][ch]Em[/ch]                         [ch]G[/ch]
   Their tears are filling up their glasses[/tab]
[tab][ch]D[/ch]              [ch]A[/ch]
No expression, no expression[/tab]
[tab][ch]Em[/ch]                         [ch]G[/ch]
   Hide my head, I want to drown my sorrow[/tab]
[tab][ch]D[/ch]            [ch]A[/ch]
No tomorrow, no tomorrow[/tab]

[Chorus]
[tab][ch]Em[/ch]                     [ch]A[/ch]                      [ch]Em[/ch]
   And I find it kinda funny, I find it kinda sad[/tab]
[tab]                        [ch]A[/ch]                            [ch]Em[/ch]
The dreams in which I'm dying are the best I've ever had[/tab]
[tab]                  [ch]A[/ch]                           [ch]Em[/ch]
I find it hard to tell you, I find it hard to take[/tab]
[tab]                   [ch]A[/ch]
When people run in circles, it's a very, very[/tab]
[tab][ch]Em[/ch]      [ch]A[/ch]
   Mad world[/tab]
[tab][ch]Em[/ch]      [ch]A[/ch]
   Mad world[/tab]

[Verse 2]
[tab][ch]Em[/ch]                          [ch]G[/ch]
   Children waiting for the day they feel good[/tab]
[tab][ch]D[/ch]               [ch]A[/ch]
Happy birthday, happy birthday[/tab]
[tab][ch]Em[/ch]                         [ch]G[/ch]
   And I feel the way that every child should[/tab]
[tab][ch]D[/ch]               [ch]A[/ch]
Sit and listen, sit and listen[/tab]
[tab][ch]Em[/ch]                           [ch]G[/ch]
   Went to school, and I was very nervous[/tab]
[tab][ch]D[/ch]               [ch]A[/ch]
No one knew me, no one knew me[/tab]
[tab][ch]Em[/ch]                         [ch]G[/ch]
   Hello, teacher, tell me what's my lesson[/tab]
[tab][ch]D[/ch]                      [ch]A[/ch]
Look right through me, look right through me[/tab]

[Chorus]
[tab][ch]Em[/ch]                     [ch]A[/ch]                      [ch]Em[/ch]
   And I find it kinda funny, I find it kinda sad[/tab]
[tab]                        [ch]A[/ch]                            [ch]Em[/ch]
The dreams in which I'm dying are the best I've ever had[/tab]
[tab]                  [ch]A[/ch]                           [ch]Em[/ch]
I find it hard to tell you, I find it hard to take[/tab]
[tab]                   [ch]A[/ch]
When people run in circles, it's a very, very[/tab]
[tab][ch]Em[/ch]      [ch]A[/ch]
   Mad world[/tab]
[tab][ch]Em[/ch]      [ch]A[/ch]
   Mad world[/tab]
[tab][ch]Em[/ch]              [ch]A[/ch]
   Enlarging your world[/tab]
[tab][ch]Em[/ch]      [ch]A[/ch]
   Mad world[/tab]
'''

output = process_song(input_text)
print(output)


#---------------
#    MAIN
#---------------

#making GUI


