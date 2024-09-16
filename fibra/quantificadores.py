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

        if outer_dict[inner_dict_str] is None:
            continue

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


def juntar_dicionarios(dict_1, dict_2):
    dict_concat = dict_1.copy()

    for key, value in dict_2.items():
        if key in dict_concat:
            dict_concat[key] += value
        else:
            dict_concat[key] = value

    return dict_concat


def criar_dicionario(quantificacao, carac_fib):
    dict_quantificacao = {}
    value = list(quantificacao.__dict__.values())

    dict_quantificacao[
        "Chassi DIO (Distribuido Interno Optico) com 24 portas - 1U - 19"] = value[0]
    dict_quantificacao[
        "Bandeja para emenda de fibra no DIO - (comporta ate 12 emendas)"] = value[1]
    dict_quantificacao[
        "Terminador Optico para 8 fibras"] = value[6]
    dict_quantificacao[
        f"Acoplador optico {carac_fib.nucleo} x 125um - {carac_fib.modo} - LC - duplo"] = \
    value[2]
    dict_quantificacao[
        f"Cordao Optico {carac_fib.nucleo} x 125um - {carac_fib.modo} - 3m - duplo - conector LC"] = \
    value[3]
    dict_quantificacao[
        f"Pig tail {carac_fib.nucleo} x 125um - {carac_fib.modo} - 1,5m - simples - conector LC"] = \
    value[4]
    dict_quantificacao[
        f"Pig tail {carac_fib.nucleo} x 125um - {carac_fib.modo} - 3,0m - duplo - conector LC"] = \
    value[5]

    return dict_quantificacao


def _calcular_quantificacao_projeto_simples(entrada) -> list:
    sala_equipamento = entrada.seq.quantificacao_equipamentos_de_fibra_seq
    salas_telecom = entrada.seq.quantificacao_equipamentos_de_fibra_sets

    dict_seq = criar_dicionario(sala_equipamento,
                                entrada.caracteristicas_seq_secundaria)
    dict_sets = criar_dicionario(salas_telecom, entrada.caracteristicas_set)
    dict_total = juntar_dicionarios(dict_seq, dict_sets)

    list_result = [dict_total, None, dict_seq, dict_sets]
    return list_result


def _calcular_quantificacao_total_projeto_complexo(entrada) -> list:
    sala_equipamento_primaria = entrada.seq.quantificacao_equipamentos_de_fibra_seq_primaria
    salas_equipamentos = entrada.seq.quantificacao_equipamentos_de_fibra_seqs_secundarias

    dict_seq = criar_dicionario(sala_equipamento_primaria,
                                entrada.caracteristicas_seq_primaria)
    dict_seqs = criar_dicionario(salas_equipamentos,
                                 entrada.caracteristicas_seq_secundaria)
    dict_total = juntar_dicionarios(dict_seq, dict_seqs)

    list_result = [dict_total, dict_seq, dict_seqs, None]
    return list_result


def _calcular_quantificacao_projeto(
        entrada: CleanedInput
) -> dict[str, dict[str, str]]:
    quantificacao_fibra = {}
    if entrada.backbone_primario:
        list_quantificacaoes = _calcular_quantificacao_total_projeto_complexo(entrada)
    else:
        list_quantificacaoes = _calcular_quantificacao_projeto_simples(entrada)

    quantificacao_fibra["Quantificacao total"] = list_quantificacaoes[0]
    quantificacao_fibra["Quantificacao SEQ primaria"] = list_quantificacaoes[1]
    quantificacao_fibra["Quantificacao SEQ secundaria"] = list_quantificacaoes[2]
    if list_quantificacaoes[3] is not None:
        quantificacao_fibra["Quantificacao SETs"] = list_quantificacaoes[3]
    else:
        quantificacao_fibra["Quantificacao SETs"] = {}

    return quantificacao_fibra


if __name__ == "__main__":

    carac_fibra1 = CaracteristicasFibra("SM", "9", "ID", "Tight Buffer")
    carac_fibra2 = CaracteristicasFibra("MM", "50", "IG", "Loose")

    sala_telecom1 = SET(2, [4])
    sala_telecom2 = SET(3, [4])
    sala_telecom3 = SET(4, [4])

    sala_equipamento1 = SEQSecundaria(4, 1, 5,
                                      [sala_telecom1, sala_telecom2, sala_telecom3])
    sala_equipamento2 = SEQSecundaria(4, 1, 5,
                                      [sala_telecom1, sala_telecom2, sala_telecom3])

    sala_equipamento_mestre = SEQPrimaria(8, 5, [sala_equipamento1, sala_equipamento2])

    # input = CleanedInput(sala_equipamento1, carac_fibra2, carac_fibra1, None, False, True)

    input = CleanedInput(sala_equipamento_mestre, carac_fibra2, carac_fibra1,
                         carac_fibra1, True, True)

    dicionario = _calcular_quantificacao_projeto(input)
    for key in dicionario.keys():
        print(
            "---------------------------------------------------------------------------------------------------------")
        print(key)
        print(
            "---------------------------------------------------------------------------------------------------------")
        for i in dicionario[key]:
            if dicionario[key][i] != 0:
                print(f"{i} : {dicionario[key][i]}")
