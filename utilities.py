def renomear(self):
    try:
        self.nome_para_renomear = f"{self.data_emissao_datetime.strftime(
            "%d.%m")}_{self.nome_fornecedor}_{self.numero_da_nf}"
    except (AttributeError, TypeError) as e:
        self.nome_para_renomear = None
