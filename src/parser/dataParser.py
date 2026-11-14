import re

class dataParser():

    def __init__(self):
        self.replace ={
        "[":"\[",
        "]":"\]"}

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


    self.debug_raw_text='''[ch]Em[/ch]   [ch]A[/ch]
            [ch]Em[/ch]   [ch]A[/ch]
        
            [Verse 1]
            [tab][ch]Em[/ch]                     [ch]G[/ch]
            All around me are familiar faces[/tab]
            [tab][ch]D[/ch]                [ch]A[/ch]
            Worn out places, worn out faces[/tab]
            [tab][ch]Em[/ch]                            [ch]G[/ch]
            Bright and early for their daily races[/tab]'''

    def rem(raw_text: str, substitutions:dict) -> str:
        
        raws = raw_text.splitlines()
        
        parsed_lines = [] #output list
        for raw in raws:
            for k, v in substitutions.items():
                raw = raw.replace(k, v)
            parsed_lines.append(raw)
        
        # Joining text with parsed lines
        return '\n'.join(parsed_lines)

    def regex(testo, regex_iniziale, regex_finale):
        # Cerca la parte del testo che si trova tra le due regex
        pattern = rf'({regex_iniziale})(.*?){regex_finale}'
        
        # Esegui la ricerca con la regex combinata
        match = re.search(pattern, testo)
        
        if match:
            return match.group(2)
        else:
            return None



    print(regex(testos, "[tab]", "[/tab]"))