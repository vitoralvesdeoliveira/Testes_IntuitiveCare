from .web_scraping.scraper import ANSWebScraper
from .data_transformation.data_transformation import PDFProcessor

def main():
    scraper = ANSWebScraper()  
    scraper.run()         
    data_transformation = PDFProcessor()
    data_transformation.run()     

if __name__ == "__main__":
    main()