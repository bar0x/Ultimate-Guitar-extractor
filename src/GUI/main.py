import logging
import re
import sys
import os


def main():
    logging.basicConfig(
        level=logging.INFO,
        # %(name)s stamperà automaticamente il nome del file/modulo che ha generato il log!
        format="%(asctime)s - [%(name)s] - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),               # Stampa a video
            logging.FileHandler("applicazione.log") # Salva su file
        ]
    )

   



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


if __name__ == "__main__":
    main()