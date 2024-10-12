from brazilfiscalreport.danfe import Danfe
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

xml_dir = ''
done_xml_output_dir = ''
danfe_output_dir = ''


excel_sheet = ''
sheet_name = '' #nome da aba da planilha

#TODO 
#
#Add informações do documento na planilha -> Ler Documento fiscal usando a classe DocumentoFiscal -> adicionar na planilha suas informações dc.nome_fornecedor...
#Def com todo o programa pra rodar em loop
#Programa deve iterar por cada xml, salvar infos na planilha selecionada -> Gerar DANFE -> mover xml para pasta: validada
#
#