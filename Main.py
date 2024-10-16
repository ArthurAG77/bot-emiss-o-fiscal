from brazilfiscalreport.danfe import Danfe
from DocumentoFiscal import DocumentoFiscal
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

xml_dir = r'D:\Área de Trabalho\PARA TESTAR EXTRATOR'
done_xml_output_dir = ''
danfe_output_dir = ''


excel_sheet = ''
sheet_name = ''  # nome da aba da planilha

documento = DocumentoFiscal()

# prints de debug

for xml in Path(xml_dir).glob("*"):

    documento.load_xml(xml)
    documento.extract_xml_info() 
    root = ET.parse(xml).getroot()

    print(xml.name)
    print(root.tag)
    print(f"Fornecedor: {documento.nome_fornecedor}")
    print(f"NUMERO DA NF: {documento.numero_da_nf}")
    print(F"DATA EMISSÃO: {documento.data_emissao}")
    print(F"V da NF: {documento.valor_nota}")
    print(f'Nome do arquivo: {documento.nome_para_renomear}')
    print("="*50)
    documento.clear_infos()

# TODO
#
# Add informações do documento na planilha -> Ler Documento fiscal usando a classe DocumentoFiscal -> adicionar na planilha suas informações dc.nome_fornecedor...
# Def com todo o programa pra rodar em loop (ele vai rodar em um schedule loop)
# Programa deve iterar por cada xml, salvar infos na planilha selecionada -> Gerar DANFE -> mover xml para pasta: validada
#
#
