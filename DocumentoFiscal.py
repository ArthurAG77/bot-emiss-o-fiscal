import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


class DocumentoFiscal:
    def __init__(self):

        # informações para criar DANFE // trocar zeros por pelos valores das var do extract
        self.chave_nf = None
        self.nome_para_renomear = None

        # informações para adicionar na planilha
        self.nome_fornecedor = None
        self.data_emissao = None

        # nome para renomear
        nome_formatado = None

        # xml root
        xml_root = None

    def load_xml(self, xml_path):
        self.xml_root = ET.parse(xml_path).getroot()

    def extract_xml_info(self):
        # XML namespace:
        xml_ns = {'ns': "http://www.portalfiscal.inf.br/nfe"}

        # Chave da NF:

        chave_nf = self.xml_root.find('ns:NFe/ns:infNFe', xml_ns)
        self.chave_nf = chave_nf.attrib['Id']

        # atributos fornecedor

        self.nome_fornecedor = self.xml_root.find(
            'ns:NFe/ns:infNFe/ns:emit/ns:xNome', xml_ns).text

        # dados NF
        self.numero_nf = self.xml_root.find(
            'ns:NFe/ns:infNFe/ns:ide/ns:nNF', xml_ns).text

        self.data_emissao_str = self.xml_root.find(
            'ns:NFe/ns:infNFe/ns:ide/ns:dhEmi', xml_ns).text.split('T')[0]
        self.data_emissao = datetime.strptime(
            self.data_emissao_str, '%Y-%m-%d')
        self.data_emissao_formatada = self.data_emissao.strftime("%d/%m/%Y")

        # informações de pagamento

        self.valor_total = self.xml_root.find(
            'ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vNF', xml_ns).text

        data_vencimento = self.xml_root.find(
            'ns:NFe/ns:infNFe/ns:cobr/ns:dup/ns:dVenc', xml_ns).text
        self.data_vencimento = datetime.strptime(
            data_vencimento, '%Y-%m-%d')

        # Criar nome do arquivo no padrão DD.MM_FORNECEDOR_NF_Nº
        self.nome_formatado = f'{self.data_emissao.strftime("%d.%m")}_{
            self.nome_fornecedor}_NF_{self.numero_nf}'

