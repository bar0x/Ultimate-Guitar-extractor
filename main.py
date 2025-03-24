import requests
from bs4 import BeautifulSoup
import re
import sys
import os

CMD_EXEC = False

#usage help

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
#    MAIN
#---------------
if (CMD_EXEC == False):
    url = str(input("Write here the UltimateGuitar site link:\n"))

#making file title based on link
name = regex(link2title(url)["title"], "^", "-[0-9]")

#HTML fetch 
response = requests.get(url)

if response.status_code != 200:
    print(f"SiteFetch: request error for status code: {response.status_code}")
    exit()

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


#writing text body in the file
filename = f"./songs/{name}.txt"
os.makedirs(os.path.dirname(filename), exist_ok=True)
with open(filename, 'w', encoding='utf-8') as file:
    file.write(str(cleanText))

#closing
print("Done!")
print("File name: "+ name)
print("you can find it in: " + filename)

