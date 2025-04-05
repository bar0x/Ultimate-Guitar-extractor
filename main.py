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


#---------------
#    MAIN
#---------------

#making GUI

app = ctk.CTk()
app.title("UG Extractor")
app.geometry("600x350")
app.grid_columnconfigure(0, weight=1)

label = ctk.CTkLabel(app, text="Welcome! paste here your Ultimate Guitar link!",text_color="orange", fg_color="transparent")
label.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

entry = ctk.CTkEntry(app, placeholder_text="Paste UG link here (ctrl + v to paste)")
entry.grid(row=1, column=0, padx=20, pady=20, sticky="ew")


button = ctk.CTkButton(app, text="Start extracting", command=execute)
button.grid(row=2, column=0, padx=20, pady=20, sticky="ew")

frame = ctk.CTkFrame(app, width=200, height=100, bg_color="transparent", border_color="black")
frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")

label_text = ctk.StringVar(value="")
label2 = ctk.CTkLabel(master=frame, textvariable=label_text,justify="left", anchor="nw")
label2.grid(row=0, column=0, padx=0, pady=0, sticky="ew")


app.mainloop()


