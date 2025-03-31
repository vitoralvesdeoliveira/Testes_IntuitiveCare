import os
import pandas as pd
from src.config import DATA_DIR
from tabula import read_pdf
import zipfile

class PDFProcessor:

    PROCESSED_DIR = DATA_DIR/"processed"
    COMPRESSED_DIR = DATA_DIR/"compressed"
    RAW_DIR = DATA_DIR/"raw"

    def __init__(self) -> None:
        os.makedirs(self.PROCESSED_DIR, exist_ok=True)
        os.makedirs(self.COMPRESSED_DIR, exist_ok=True)
    
    def _extract_table_from_pdf(self)-> pd.DataFrame:
        tables = read_pdf(
                str(self.RAW_DIR/"Anexo_I.pdf"),
                pages='all',
                multiple_tables=True,
                lattice=True,
                # pandas_options={'header': None}
        )[2:]

        if not tables:
            raise ValueError("Nenhuma tabela encontrada no PDF")

        df_final = pd.concat(tables, ignore_index=True)
        
        # Limpeza dos dados
        df_final.columns = df_final.columns.str.replace("\r", "", regex=True)  # Limpa os nomes das colunas
        df_final = df_final.replace("\r", " ", regex=True)  # Remove '\r' dos valores das células
        df_final.rename(columns={"OD": "Seg. Odontológica", "AMB": "Seg. Ambulatorial"}, inplace=True)
        df_final.replace({"OD": "Seg. Odontológica", "AMB": "Seg. Ambulatorial"}, inplace=True)
        
        return df_final
    
    def _save_to_csv(self, df: pd.DataFrame, filename: str) -> None:
        """Salva o DataFrame como CSV."""
        csv_path = self.PROCESSED_DIR / filename
        df.to_csv(csv_path, index=False, encoding='utf-8-sig')
    
    def create_zip(self, csv_filename: str, zip_filename: str) :
        """Cria arquivo ZIP com o CSV processado."""
        csv_path = self.PROCESSED_DIR / csv_filename
        zip_path = self.COMPRESSED_DIR / zip_filename
        
        with zipfile.ZipFile(zip_path, 'w') as zipf:
            zipf.write(csv_path, arcname=csv_filename)   
            print(f"Arquivo ZIP criado com sucesso: {zip_filename}")
         

    def run(self) -> None:
        try:
            table = self._extract_table_from_pdf()
            self._save_to_csv(table, "Teste_VitorAlves.csv")
            self.create_zip('Teste_VitorAlves.csv',"Teste_VitorAlves.zip")
        except Exception as e:
            print(f"Erro na transformação: {str(e)}")
            raise


if __name__ == "__main__":
    processor = PDFProcessor()
    processor.run()