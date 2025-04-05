import re

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

def convert_text_to_latex():
    pass

replace = {
    "[":"\[",
    "]":"\]"
}


testos='''[ch]Em[/ch]   [ch]A[/ch]
[ch]Em[/ch]   [ch]A[/ch]

[Verse 1]
[tab][ch]Em[/ch]                     [ch]G[/ch]
   All around me are familiar faces[/tab]
[tab][ch]D[/ch]                [ch]A[/ch]
Worn out places, worn out faces[/tab]
[tab][ch]Em[/ch]                            [ch]G[/ch]
   Bright and early for their daily races[/tab]'''

rem(testos, replace)
print(regex(testos, "[tab]", "[/tab]"))