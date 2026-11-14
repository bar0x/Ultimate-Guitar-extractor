import logging as log
import requests


class dataScraper():

    def __init__(self):
        self.log = log.getLogger(__name__)
        self.ug_base_url = "https://www.ultimate-guitar.com/"


    def fetch_by_url (self, url: str) -> str:
        self.req_url = url
        try:
            self.log.info(f"Trying to fetch {url}")
            response = requests.get(url, timeout=10)

        except requests.exceptions.HTTPError as e:
            #Logs HTTP error and status code
            self.log.error(f"HTTP Error ({e.response.status_code}) for {url}: {e}")        
        except requests.exceptions.RequestException as e:
            #Logs other errors (dns, timeout and so)
            self.log.error(f"Connection error during GET at {url}: {e}")
        
        self.log.info(f"Webpage Successfully fetched!")
        
        return response.text

    def fetch_by_id(self, id:str) -> None:
        pass # TODO

    def get_song_info(self, url: str) -> dict:
        
        frame = url.split('/')

        link_content = {
            "site": frame[2],  
            "tab": frame[3],   
            "singer": frame[4],  
            "title": frame[5]
        }
        
        return link_content
        #making file title based on link
        #name = regex(get_song_info(url)["title"], "^", "-[0-9]")

        