from datetime import datetime


def formatar_nome_arquivo(self):
    """não funcina sem self"""
    try:
        data_formatada_date = datetime.strptime(self.data_emissao, "%d/%m/%y")
        data_formatada_str = datetime.strftime(data_formatada_date, "%d.%m")

        self.nome_para_renomear = f"{data_formatada_str}_{
            self.nome_fornecedor}_NF_{self.numero_da_nf}"
    except Exception as e:
        self.nome_para_renomear = None


def formatar_data_emissao(data_str: str):
    """
    formata a data extraida do xml
    preencha com string retirada do xml
    :fuso -> False: Para datas no qual não é necessario fuso horario (os dois primeiros formatos de xml)
    :fuso -> True Para datas qual necessitam de fuso 
    """

    try:
        data_emissao_datetime = datetime.strptime(
            data_str, "%Y-%m-%dT%H:%M:%S%z")
        return data_emissao_datetime.strftime("%d/%m/%y")
    except:
        try:
            data_emissao_datetime = datetime.strptime(
                data_str, "%Y-%m-%dT%H:%M:%S")
            return data_emissao_datetime.strftime("%d/%m/%y")
        except:
            try:
                data_emissao_datetime = datetime.strptime(data_str, "%Y-%m-%d")
                return data_emissao_datetime.strftime("%d/%m/%y")
            except:
                return None


def procurar_em_xml(self, xpath, xml_ns):
    try:
        return self.xml_root.find(xpath, xml_ns).text
    except AttributeError as e:
        return None


def iterar_por_caminho_generico(self, generic_path: list, xml_ns: dict):
    for xpath in generic_path:
        try:
            testar_paths = procurar_em_xml(self, xpath, xml_ns)
            if testar_paths != None:
                return testar_paths
        except Exception as e:
            print(f"Erro ao procurar {xpath}")
            continue
    return None
