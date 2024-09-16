import os

import pandas

from .sala_de_telecomunicacoes import SET
from .salas_de_equipamentos import SEQPrimaria, SEQSecundaria
from dataclasses import dataclass
import pandas as pd
import tempfile


@dataclass
class CaracteristicasFibra:
    modo: str = ''
    nucleo: str = ''
    indice: str= ''
    categoria: str = ''


@dataclass
class CleanedInput:
    seq: SEQPrimaria | SEQSecundaria
    caracteristicas_set: CaracteristicasFibra
    caracteristicas_seq_secundaria: CaracteristicasFibra
    caracteristicas_seq_primaria: CaracteristicasFibra
    backbone_primario: bool = False
    backbone_secundario: bool = False


def dicts_to_xlsx(outer_dict: dict[str, dict]) -> bytes:
    quantification = pd.DataFrame()
    start = 0

    for inner_dict_str in outer_dict:
        inner_dict_keys = []
        inner_dict_values = []

        for key in outer_dict[inner_dict_str].keys():
            inner_dict_keys.append(key)

        for key in outer_dict[inner_dict_str].values():
            inner_dict_values.append(key)

        space = pd.Series([''] * (1000 - len(inner_dict_keys)))
        space_full = pd.Series([''] * 1000)

        quantification.insert(start, f'{inner_dict_str} - Material', pd.concat([pd.Series(inner_dict_keys), space], ignore_index=True))
        quantification.insert(start+1, f'{inner_dict_str} - Quantidade', pd.concat([pd.Series(inner_dict_values), space], ignore_index=True), allow_duplicates = True)
        quantification.insert(start+2, ' ', space_full, allow_duplicates = True)

        start += 3

    return get_xls(quantification)


def get_xls(df: pandas.DataFrame) -> bytes:
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, 'quantificacao.xlsx')
        df.to_excel(file_path, index=False)
        with open(file_path, 'rb') as f:
            return f.read()


def _calcular_quantificacao_total_projeto_simples(entrada):
    sala_equipamento = entrada.seq.quantificacao_equipamentos_de_fibra_seq
    sets = entrada.seq.quantificacao_equipamentos_de_fibra_sets
    quantificacao_total = {
        "Chassi DIO (Distribuido Interno Optico) com 24 portas - 1U - 19": sala_equipamento.dios + sets.dios,
        "Bandeja para emenda de fibra no DIO - (comporta ate 12 emendas)": sala_equipamento.caixas_de_emenda + sets.caixas_de_emenda,
        "Terminador Optico para 8 fibras": sala_equipamento.terminadores_opticos + sets.terminadores_opticos}

    if entrada.caracteristicas_set.nucleo == entrada.caracteristicas_seq_secundaria.nucleo:
        quantificacao_total[
            f"Acoplador optico {entrada.caracteristicas_set.nucleo} x 125um - {entrada.caracteristicas_set.modo} - LC - duplo"] = sala_equipamento.acopladores_lc_duplo + sets.acopladores_lc_duplo

        quantificacao_total[
            f"Cordao Optico {entrada.caracteristicas_set.nucleo} x 125um - {entrada.caracteristicas_set.modo} - 3m - duplo - conector LC"] = sala_equipamento.cordao_optico + sets.cordao_optico

        quantificacao_total[
            f"Pig tail {entrada.caracteristicas_set.nucleo} x 125um - {entrada.caracteristicas_set.modo} - 1,5m - simples - conector LC"] = sala_equipamento.pig_tails_simples + sets.pig_tails_simples

        quantificacao_total[
            f"Pig tail {entrada.caracteristicas_set.nucleo} x 125um - {entrada.caracteristicas_set.modo} - 3,0m - duplo - conector LC"] = sala_equipamento.pig_tails_duplos + sets.pig_tails_duplos

    else:
        quantificacao_total[
            f"Acoplador optico {entrada.caracteristicas_set.nucleo} x 125um - {entrada.caracteristicas_set.modo} - LC - duplo"] = sets.acopladores_lc_duplo
        quantificacao_total[
            f"Acoplador optico {entrada.caracteristicas_seq_secundaria.nucleo} x 125um - {entrada.caracteristicas_seq_secundaria.modo} - LC - duplo"] = sala_equipamento.acopladores_lc_duplo

        quantificacao_total[
            f"Cordao Optico {entrada.caracteristicas_set.nucleo} x 125um - {entrada.caracteristicas_set.modo} - 3m - duplo - conector LC"] = sets.cordao_optico
        quantificacao_total[
            f"Cordao Optico {entrada.caracteristicas_seq_secundaria.nucleo} x 125um - {entrada.caracteristicas_seq_secundaria.modo} - 3m - duplo - conector LC"] = sala_equipamento.cordao_optico

        quantificacao_total[
            f"Pig tail {entrada.caracteristicas_set.nucleo} x 125um - {entrada.caracteristicas_set.modo} - 1,5m - simples - conector LC"] = sets.pig_tails_simples
        quantificacao_total[
            f"Pig tail {entrada.caracteristicas_seq_secundaria.nucleo} x 125um - {entrada.caracteristicas_seq_secundaria.modo} - 1,5m - simples - conector LC"] = sala_equipamento.pig_tails_simples

        quantificacao_total[
            f"Pig tail {entrada.caracteristicas_set.nucleo} x 125um - {entrada.caracteristicas_set.modo} - 3,0m - duplo - conector LC"] = sets.pig_tails_duplos
        quantificacao_total[
            f"Pig tail {entrada.caracteristicas_seq_secundaria.nucleo} x 125um - {entrada.caracteristicas_seq_secundaria.modo} - 3,0m - duplo - conector LC"] = sala_equipamento.pig_tails_duplos

    return quantificacao_total


def _calcular_quantificacao_total_projeto_complexo(entrada):
    return _calcular_quantificacao_total_projeto_simples(entrada)


def _calcular_quantificacao_projeto(
        entrada: CleanedInput
) -> dict[str, dict[str, str]]:
    quantificacao_fibra = {}
    if entrada.backbone_primario:
        seqp = entrada.seq.quantificacao_equipamentos_de_fibra_seq_primaria
        seqs = entrada.seq.quantificacao_equipamentos_de_fibra_seqs_secundarias
        quantificacao_fibra["Quantificacao total"]
        _calcular_quantificacao_total_projeto_complexo(entrada)
    else:
        quantificacao_fibra[
            "Quantificacao total"] = _calcular_quantificacao_total_projeto_simples(
            entrada)

    return quantificacao_fibra


if __name__ == "__main__":
    carac_fibra1 = CaracteristicasFibra("SM", "9", "Indice Gradual", "Loose")
    carac_fibra2 = CaracteristicasFibra("SM", "9", "Indice Degrau", "Loose")
    carac_fibra3 = CaracteristicasFibra("MM", "50", "Indice Degrau", "Loose")
    sala_telecom1 = SET(2, [4])
    sala_telecom2 = SET(3, [4])
    sala_telecom3 = SET(4, [4])

    sala_equipamento1 = SEQSecundaria(4, 1, 5,
                                      [sala_telecom1, sala_telecom2, sala_telecom3])
    sala_equipamento2 = SEQSecundaria(12, 1, 5,
                                      [sala_telecom1, sala_telecom2, sala_telecom3])

    sala_equipamento_mestre = SEQPrimaria(12, 5, [sala_equipamento1, sala_equipamento2])

    input = CleanedInput(sala_equipamento1, carac_fibra3, carac_fibra2, carac_fibra3,
                         False, True)
    # input = CleanedInput(sala_equipamento_mestre, carac_fibra3, carac_fibra2,  None, True)

    dicionario = _calcular_quantificacao_projeto(input)
    for i in dicionario['Quantificacao total']:
        if not dicionario['Quantificacao total'][i]:
            print(f"{i} : {dicionario['Quantificacao total'][i]}")
