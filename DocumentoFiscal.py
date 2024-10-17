import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
import utilities


class DocumentoFiscal:
    def __init__(self):

        # nome do arquivo seguindo o padrão DATA EMIT_FORNECEDOR_Nº DA NF
        self.nome_para_renomear = None
        self.generico = None
        # informações para adicionar na planilha
        self.numero_da_nf = None
        self.nome_fornecedor = None
        self.data_emissao = None
        self.valor_nf = None
        # nome para renomear
        nome_formatado = None

        # xml root
        xml_root = None

    def load_xml(self, xml_path):
        self.xml_root = ET.parse(xml_path).getroot()

    def extract_xml_main_info(self):
        # XML namespace:
        xml_ns = {
            'portal_fiscal': "http://www.portalfiscal.inf.br/nfe",  # tag nfeProc
            'sped_fazenda': "http://www.sped.fazenda.gov.br/nfse",  # tag NFSe
            'pref_sp': ""  # tag RetornoConsulta
        }

        # tags da xml algumas nfs tem a mesma estrutura mas tags diferentes, aqui colocarei as tags para melhor centralização
        xml_tags = {
            "portal_fiscal": ("{http://www.portalfiscal.inf.br/nfe}nfeProc", "{http://www.portalfiscal.inf.br/nfe}NFe"),
            "sped_fazenda": ("{http://www.sped.fazenda.gov.br/nfse}NFSe"),
            "pref_sp": ("{http://www.prefeitura.sp.gov.br/nfe}RetornoConsulta")
        }

        # caminho especifico separado por namespace
        xml_exclusive_path = {
            "portal_fiscal": {
                "numero_nf": ".//portal_fiscal:infNFe/portal_fiscal:ide/portal_fiscal:nNF",
                "nome_fornecedor": ".//portal_fiscal:infNFe/portal_fiscal:emit/portal_fiscal:xNome",
                "data_emissao": ".//portal_fiscal:infNFe/portal_fiscal:ide/portal_fiscal:dhEmi",
                "valor": ".//portal_fiscal:infNFe/portal_fiscal:total/portal_fiscal:ICMSTot/portal_fiscal:vNF"
            },
            "sped_fazenda": {
                "numero_nf": "sped_fazenda:infNFSe/sped_fazenda:nNFSe",
                "nome_fornecedor": "sped_fazenda:infNFSe/sped_fazenda:emit/sped_fazenda:xNome",
                "data_emissao": "sped_fazenda:infNFSe/sped_fazenda:DPS/sped_fazenda:infDPS/sped_fazenda:dhEmi",
                "valor": "sped_fazenda:infNFSe/sped_fazenda:valores/sped_fazenda:vLiq"
            },

            "pref_sp": {
                "numero_nf": ".//pref_sp:NFe/pref_sp:ChaveNFe/pref_sp:NumeroNFe",
                "nome_fornecedor": ".//pref_sp:RazaoSocialPrestador",
                "data_emissao": ".//pref_sp:DataEmissaoNFe",
                "valor": ".//pref_sp:ValorServicos"
            }
        }

        # caminhos genericos para xmls não cadastrados
        xml_generic_path = {
            # ADICIONAR CAMINHOS PARA ITERAR E VERIFICAR SE MESMO NÃO ESTANDO NO MODELO ELE CONSEGUE EXTRAIR
            "numero_nf": (".//infNFSe/nNFSe", ".//nNFSe", ".//NFS-e/infNFSe/Id/nNFS-e", ".//nNFS-e"),
            "nome_fornecedor": (".//emit/xNome", ".//xNome", ".//NFS-e/infNFSe/prest/xNome"),
            "data_emissao": (".//sped_fazenda:infDPS/sped_fazenda:dhEmi", ".//dhEmi", ".//NFS-e/infNFSe/Id/dEmi", ".//dEmi"),
            "valor": (".//valores/vLiq", ".//vLiq", ".//NFS-e/infNFSe/total/vtLiqFaturas")
        }

        # Condicionais para selecionar o modelo de xml no qual estamos lidando:
        if self.xml_root.tag in xml_tags["portal_fiscal"]:
            # Numero da nota:
            self.numero_da_nf = utilities.procurar_em_xml(
                self,  xml_exclusive_path["portal_fiscal"]["numero_nf"], xml_ns)
            # Nome do Fornecedor
            self.nome_fornecedor = utilities.procurar_em_xml(
                self, xml_exclusive_path["portal_fiscal"]["nome_fornecedor"], xml_ns)
            # Data de Emissão
            data_emissao_str = utilities.procurar_em_xml(
                self, xml_exclusive_path["portal_fiscal"]["data_emissao"], xml_ns)
            self.data_emissao = utilities.formatar_data_emissao(
                data_emissao_str)
            # V. Total / liquido da nota
            self.valor_nf = utilities.procurar_em_xml(
                self, xml_exclusive_path["portal_fiscal"]["valor"], xml_ns)
            # formatar nome de arquivo:
            #utilities.formatar_nome_arquivo(self)

        elif self.xml_root.tag in xml_tags["sped_fazenda"]:
            # Numero da nota
            self.numero_da_nf = utilities.procurar_em_xml(
                self, xml_exclusive_path["sped_fazenda"]["numero_nf"], xml_ns)
            # Nome Fornecedor
            self.nome_fornecedor = utilities.procurar_em_xml(
                self, xml_exclusive_path["sped_fazenda"]["nome_fornecedor"], xml_ns)
            # Data emissão
            data_emissao_str = utilities.procurar_em_xml(
                self, xml_exclusive_path["sped_fazenda"]["data_emissao"], xml_ns)
            self.data_emissao = utilities.formatar_data_emissao(
                data_emissao_str)
            # V. total / liquido
            self.valor_nf = utilities.procurar_em_xml(
                self, xml_exclusive_path["sped_fazenda"]["valor"], xml_ns)
            # formatar nome_arquivo
            #utilities.formatar_nome_arquivo(self)

        elif self.xml_root.tag in xml_tags["pref_sp"]:
            # Numero da nota
            self.numero_da_nf = utilities.procurar_em_xml(
                self,  xml_exclusive_path["pref_sp"]["numero_nf"], xml_ns)
            # Nome do Fornecedor
            self.nome_fornecedor = utilities.procurar_em_xml(
                self, xml_exclusive_path["pref_sp"]["nome_fornecedor"], xml_ns)
            # Data de emissão
            data_emissao_str = utilities.procurar_em_xml(
                self, xml_exclusive_path["pref_sp"]["data_emissao"], xml_ns)
            self.data_emissao = utilities.formatar_data_emissao(
                data_emissao_str)
            # Valor total/liquido
            self.valor_nf = utilities.procurar_em_xml(
                self, xml_exclusive_path["pref_sp"]["valor"], xml_ns)

            #utilities.formatar_nome_arquivo(self)
        else:
            # Numero da nota:
            self.numero_da_nf = utilities.iterar_por_caminho_generico(
                self, xml_generic_path["numero_nf"], xml_ns)
            # Nome do fornecedor
            self.nome_fornecedor = utilities.iterar_por_caminho_generico(
                self, xml_generic_path["nome_fornecedor"], xml_ns)
            # Data de emissão
            data_emissao_str = utilities.iterar_por_caminho_generico(
                self, xml_generic_path["data_emissao"], xml_ns)

            self.data_emissao = utilities.formatar_data_emissao(
                data_emissao_str)
            # Valor liquido/total
            self.valor_nf = utilities.iterar_por_caminho_generico(
                self, xml_generic_path["valor"], xml_ns)
            # Formatar nome

            # atributo de classes genericas, pra identificar pois algumas informações podem estar erradas
            self.generico = "SIM"
        utilities.formatar_nome_arquivo(self)

    def clear_infos(self):
        self.data_emissao = None
        self.numero_da_nf = None
        self.nome_para_renomear = None
        self.nome_fornecedor = None
        self.valor_nf = None
        self.generico = None
