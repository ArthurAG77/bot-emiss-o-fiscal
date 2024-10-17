from DocumentoFiscal import DocumentoFiscal
import shutil
import os
import pandas as pd
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path

xml_dir = r'D:\Área de Trabalho\PARA TESTAR EXTRATOR - Copia'
done_xml_output_dir = r"D:\Área de Trabalho\PARA TESTAR EXTRATOR - Copia\adicionados a excel"
danfe_output_dir = ''
saved_xml = {
    "path": [],
    "Rename": []
}

# caminho até a planilha
excel_path = r'D:\Área de Trabalho\processo envolvendo xmls\validando.xlsx'
sheet_name = 'validar'  # nome da aba da planilha

df = pd.read_excel(excel_path, sheet_name="validar")
novos_dados = {
    "FORNECEDOR": [],
    "DATA EMISSAO": [],
    "VALOR": [],
    "NF": []
}

documento = DocumentoFiscal()


for xml in Path(xml_dir).glob("*"):
    if xml.suffix == ".xml":
        documento.load_xml(xml)
        documento.extract_xml_main_info()
        root = ET.parse(xml).getroot()

        if documento.nome_fornecedor != None:
            saved_xml["path"].append(f"{xml}")
            saved_xml["Rename"].append(f"{documento.nome_para_renomear}")
            novos_dados["FORNECEDOR"].append(documento.nome_fornecedor)
            novos_dados["DATA EMISSAO"].append(documento.data_emissao)
            novos_dados["VALOR"].append(documento.valor_nf)
            novos_dados["NF"].append(documento.numero_da_nf)

df_novos = pd.DataFrame(novos_dados)
df = pd.concat([df, df_novos], ignore_index=True)

df.to_excel(excel_path, sheet_name="validar", index=False)

for i in range(len(saved_xml["path"])):
    os.rename(saved_xml["path"][i], os.path.join(done_xml_output_dir, saved_xml["Rename"][i]))

    # TODO
    #
    # Add informações do documento na planilha -> Ler Documento fiscal usando a classe DocumentoFiscal -> adicionar na planilha suas informações dc.nome_fornecedor...
    # Def com todo o programa pra rodar em loop (ele vai rodar em um schedule loop)
    # Programa deve iterar por cada xml, salvar infos na planilha selecionada -> Gerar DANFE -> mover xml para pasta: validada
    #
    #
