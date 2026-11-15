import re
from bs4 import BeautifulSoup
import logging as log
import os

class dataParser():

    def __init__(self):
        self.log = log.getLogger(__name__)

        #DEFINE
        self.save_file_path = "./songs/"

        self.replace ={
        "[":r"\[",
        "]":r"\]"}
        self.replacingRules = {
        "\\n":"",
        "\\r":"\n",
        "[ch]":"",
        "[/ch]":"",
        "[tab]":"",
        "[/tab]":"",
        "\\&quot;":"",
        "'":"'"
    }

    def blob_to_clean(self, blob: str) -> str:

        self.log.info(f"Estracting text blob using BeautifulSoup...")
        
        soup = BeautifulSoup(blob, 'html.parser')

        #selecting js-store class
        selected_div = soup.find('div', {'class': 'js-store'})

        #searching for text
        section = self.regex(str(selected_div.prettify()), "\\\\r", "&quot;,")

        #cleaning messy text from special chars
        cleanText = self.remove_html_format(section, self.replacingRules)

        self.log.info(f"Text blob Extracted!")
        return cleanText

    @staticmethod
    def remove_html_format(raw_text: str, substitutions:dict) -> str:
        
        raws = raw_text.splitlines()
        
        parsed_lines = [] #output list
        for raw in raws:
            for k, v in substitutions.items():
                raw = raw.replace(k, v)
            parsed_lines.append(raw)
        
        # Joining text with parsed lines
        return '\n'.join(parsed_lines)

    @staticmethod
    def regex(testo: str, regex_iniziale: str, regex_finale: str) -> str | None:
        # Cerca la parte del testo che si trova tra le due regex
        pattern = rf'({regex_iniziale})(.*?){regex_finale}'
        
        # Esegui la ricerca con la regex combinata
        match = re.search(pattern, testo)
        
        if match:
            return match.group(2)
        else:
            return None

    def save_to_file_as_text(self, filename: str, content: str) -> None:
        relative_file_path = f"{self.save_file_path}{filename}.txt"
        self.log.info(f"Trying to save data into text file {filename}")
        
        os.makedirs(os.path.dirname(self.save_file_path), exist_ok=True)
        with open(relative_file_path, 'w', encoding='utf-8') as file:
            file.write(str(content))

        self.log.info(f"File saved! location: {relative_file_path}")