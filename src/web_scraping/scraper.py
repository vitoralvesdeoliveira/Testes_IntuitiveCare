import os
import zipfile
from requests import get
from bs4 import BeautifulSoup

from src.config import DATA_DIR

class ANSWebScraper:
    """Realiza web scraping e baixa arquivos."""
    BASE_URL = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
    ZIP_FILENAME = "Teste_IntuitiveCare.zip"
    ZIP_DIR = DATA_DIR/"compressed"
    DOWNLOAD_DIR =  DATA_DIR/"raw"

    def __init__(self):
        """Inicializa o scraper e cria o diretório de downloads caso não exista."""
        os.makedirs(self.DOWNLOAD_DIR, exist_ok=True)
        os.makedirs(self.ZIP_DIR, exist_ok=True)

    def _get_page_content(self) -> BeautifulSoup:
        """Obtém o conteúdo HTML da página."""
        try:
            response = get(self.BASE_URL, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            raise Exception(f"Falha ao buscar conteúdo da página: {e}")
          
    def _filter_pdf_links(self,soup: BeautifulSoup) -> list[str]:
        links = soup.find_all('a',href=True)
        links_anexos = [
            link["href"] for link in links 
            if("Anexo_I" in link["href"] or "Anexo_II" in link["href"]) and link["href"].lower().endswith(".pdf") 
        ]
        return links_anexos
    
    def _download_file(self,url:str,filename:str) -> bool:
        try:
            response = get(url, timeout = 10)
            response.raise_for_status()
            filepath = os.path.join(self.DOWNLOAD_DIR, filename)

            with open(filepath,'wb') as file: 
                file.write(response.content) 

            return True
        except Exception as e:
            print(f"Falha no download: {e}")
            return False

    def _download_attachments(self) -> None:
        page_content = self._get_page_content()
        pdf_links = self._filter_pdf_links(page_content)

        if not pdf_links:
            raise Exception("Nenhum link válido encontrado para os Anexos I e II")
        
        for link in pdf_links:
            filename = link.split('/')[-1]
            if "Anexo_II" in filename:
                standart_name = "Anexo_II.pdf"
            elif "Anexo_I" in filename:
                standart_name = "Anexo_I.pdf"
            else:
                #add log caso o nome do pdf mude
                continue
            if self._download_file(link,standart_name):
                print(f"{filename} baixado como {standart_name}.")
            else:
                print(f"{filename} não pode ser baixado.")

    def _create_zip(self) -> None:
        zip_path = os.path.join(self.ZIP_DIR, self.ZIP_FILENAME)

        with zipfile.ZipFile(zip_path,'w') as zipf:
            for root, dirs, files in os.walk(self.DOWNLOAD_DIR):
                for file in files:
                    file_path = os.path.join(root,file)
                    zipf.write(file_path)
                print(f"Arquivo ZIP criado com sucesso: {self.ZIP_FILENAME}")


    def run(self) -> None:
        """Executa todo o fluxo do web scraping."""
        try:
            self._download_attachments()
            self._create_zip()
        except Exception as e:
            print(f"Erro durante a execução: {str(e)}")
            raise

if __name__ == "__main__":
    scraper = ANSWebScraper()
    scraper.run()
    
