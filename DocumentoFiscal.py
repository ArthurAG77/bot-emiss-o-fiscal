import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import utilities


class DocumentoFiscal:
    def __init__(self):

        # nome do arquivo seguindo o padrão DATA EMIT_FORNECEDOR_Nº DA NF
        self.nome_para_renomear = None

        # informações para adicionar na planilha
        self.numero_da_nf = None
        self.nome_fornecedor = None
        self.data_emissao = None
        self.valor_nota = None
        # nome para renomear
        nome_formatado = None

        # xml root
        xml_root = None

    def load_xml(self, xml_path):
        self.xml_root = ET.parse(xml_path).getroot()

    def extract_xml_info(self):
        # XML namespace:
        xml_ns = {
            'portal_fiscal': "http://www.portalfiscal.inf.br/nfe",  # tag nfeProc
            'sped_fazenda': "http://www.sped.fazenda.gov.br/nfse",  # tag NFSe
            'pref_sp': ""  # tag RetornoConsulta
        }

        # Condicionais para selecionar o modelo de xml no qual estamos lidando:
        if self.xml_root.tag == "{http://www.portalfiscal.inf.br/nfe}nfeProc":
            try:
                self.numero_da_nf = self.xml_root.find(
                    "portal_fiscal:NFe/portal_fiscal:infNFe/portal_fiscal:ide/portal_fiscal:nNF", xml_ns).text
            except AttributeError:
                self.numero_da_nf = None

            # Nome do Fornecedor
            try:
                self.nome_fornecedor = self.xml_root.find(
                    "portal_fiscal:NFe/portal_fiscal:infNFe/portal_fiscal:emit/portal_fiscal:xNome", xml_ns).text
            except AttributeError:
                self.nome_fornecedor = None

            # Data de emissão
            try:
                data_emissao_str = self.xml_root.find(
                    "portal_fiscal:NFe/portal_fiscal:infNFe/portal_fiscal:ide/portal_fiscal:dhEmi", xml_ns).text

                self.data_emissao_datetime = datetime.strptime(
                    data_emissao_str, "%Y-%m-%dT%H:%M:%S%z")

                self.data_emissao = self.data_emissao_datetime.strftime(
                    "%d/%m/%y")
            except AttributeError:
                self.data_emissao = None
            # V. Total / liquido da nota
            try:
                self.valor_nota = float(self.xml_root.find(
                    "portal_fiscal:NFe/portal_fiscal:infNFe/portal_fiscal:total/portal_fiscal:ICMSTot/portal_fiscal:vNF", xml_ns).text)
            except AttributeError:
                self.valor_nota = None

            # formatar nome de arquivo:
            utilities.renomear(self)

        elif self.xml_root.tag == "{http://www.sped.fazenda.gov.br/nfse}NFSe":
            # Numero da nota
            try:
                self.numero_da_nf = self.xml_root.find(
                    "sped_fazenda:infNFSe/sped_fazenda:nNFSe", xml_ns).text
            except AttributeError:
                self.numero_da_nf = None

            # Nome Fornecedor
            try:
                self.nome_fornecedor = self.xml_root.find(
                    "sped_fazenda:infNFSe/sped_fazenda:emit/sped_fazenda:xNome", xml_ns).text
            except AttributeError:
                self.nome_fornecedor = None
            # Data emissão
            try:
                data_emissao_str = self.xml_root.find(
                    "sped_fazenda:infNFSe/sped_fazenda:DPS/sped_fazenda:infDPS/sped_fazenda:dhEmi", xml_ns).text

                self.data_emissao_datetime = datetime.strptime(
                    data_emissao_str, "%Y-%m-%dT%H:%M:%S%z")

                self.data_emissao = self.data_emissao_datetime.strftime(
                    "%d/%m/%y")
            except AttributeError:
                self.data_emissao = None
            # V. total / liquido
            try:
                self.valor_nota = float(self.xml_root.find(
                    "sped_fazenda:infNFSe/sped_fazenda:valores/sped_fazenda:vLiq", xml_ns).text)
            except AttributeError:
                self.valor_nota = None

            # formatar nome_arquivo
            utilities.renomear(self)

        elif self.xml_root.tag == "{http://www.prefeitura.sp.gov.br/nfe}RetornoConsulta":
            # Numero da nota
            try:
                self.numero_da_nf = self.xml_root.find(
                    ".//pref_sp:NFe/pref_sp:ChaveNFe/pref_sp:NumeroNFe", xml_ns).text
            except AttributeError:
                self.numero_da_nf = None
            # Nome do Fornecedor
            try:
                self.nome_fornecedor = self.xml_root.find(
                    ".//pref_sp:RazaoSocialPrestador", xml_ns).text
            except:
                self.nome_fornecedor = None

            # Data de emissão
            try:
                data_emissao_str = self.xml_root.find(
                    ".//pref_sp:DataEmissaoNFe", xml_ns).text
                self.data_emissao_datetime = datetime.strptime(
                    data_emissao_str, "%Y-%m-%dT%H:%M:%S")
                self.data_emissao = self.data_emissao_datetime.strftime(
                    "%d/%m/%y")
            except:
                self.data_emissao = None

            # Valor total/liquido
            try:
                self.valor_nota = float(self.xml_root.find(
                    ".//pref_sp:ValorServicos", xml_ns).text)
            except:
                self.valor_nota = None

            utilities.renomear(self)
        # else:
            # print(
            # "ESTE MODELO DE XML NÃO ESTÁ NO NOSSO SISTEMA, IREMOS CHECAR PARA NOVAS ATUALIZAÇÕES")
            # self.nome_fornecedor = self.xml_root.find("portal_fiscal:")

    def clear_infos(self):
        self.data_emissao = None
        self.numero_da_nf = None
        self.nome_para_renomear = None
        self.nome_fornecedor = None
        self.valor_nota = None

# TODO Pegar esses try de extrair coisa e colocar cada em um um def em utilities pra que eu só passe (self, Caminho_busca_xml, ns)
