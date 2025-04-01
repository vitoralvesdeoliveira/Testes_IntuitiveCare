import os
import requests
from bs4 import BeautifulSoup
import datetime
from src.config import DATA_DIR

class ANSDataDownloader:
    BASE_URL = "https://dadosabertos.ans.gov.br/FTP/PDA/"
    DOWNLOAD_DIR = f"{DATA_DIR}/compressed"

    def __init__(self) -> None:
        os.makedirs(self.DOWNLOAD_DIR, exist_ok=True)


    def _list_past_2_years(self) -> list:
        # try:
        response = requests.get(f"{self.BASE_URL}/demonstracoes_contabeis")
        response.raise_for_status()

        soup = BeautifulSoup(response.text,'html.parser')
        links = soup.find_all('a')
        
        years = []
        for link in links:
            href = link.get('href')
            if href and href.endswith('/'):
                dir_name = href.rstrip('/')
                if dir_name.isdigit() and len(dir_name) == 4:
                    year = int(dir_name)
                    if 2000 <= year <= datetime.datetime.now().year + 1:
                        years.append(href) 
        years.sort(reverse=True)
        past_2_years = years[:2]
        return past_2_years

    def _download_file(self,url:str,filename:str) -> bool:
        try:
            response = requests.get(url, timeout = 10)
            response.raise_for_status()
            filepath = os.path.join(self.DOWNLOAD_DIR, filename)

            with open(filepath,'wb') as file: 
                file.write(response.content) 

            return True
        
        except Exception as e:
            print(f"Falha no download: {e}")
            return False

    def _download_past_2_years_archive(self,list):
        for year in list:
            year_url = f"{self.BASE_URL}demonstracoes_contabeis/{year}"
            response = requests.get(year_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            zip_links = [
                link.get('href') for link in soup.find_all('a') 
                if link.get('href') and link.get('href').endswith('.zip')
            ]
            for zip_file in zip_links:
                zip_url = f"{year_url}{zip_file}"
                os.makedirs(f"{self.DOWNLOAD_DIR}/Demonstracoes_{year}", exist_ok=True)
                local_filename = f"{self.DOWNLOAD_DIR}/Demonstracoes_{year}_{zip_file}"
                self._download_file(zip_url, local_filename)
                print(f"Downloaded: {local_filename}")

    def _download_registration_data(self):
        filename = "DadosCadastrais.csv"
        self._download_file(f'{self.BASE_URL}/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv',f'{DATA_DIR}/raw/{filename}')
        print(f"Relatório Cadop baixado com sucesso como {filename}.")

    def run(self) -> None:
            """Executa todo o fluxo do download."""
            try:
                years_list = self._list_past_2_years()
                self._download_past_2_years_archive(years_list)
                self._download_registration_data()
            except Exception as e:
                print(f"Erro durante a execução: {str(e)}")
                raise

if __name__ == "__main__":
    downloader = ANSDataDownloader()
    downloader.run()