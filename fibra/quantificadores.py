import os

import pandas

from fibra.equipamentos_de_fibra import QuantificacaoDeEquipamentosDeFibra
from .sala_de_telecomunicacoes import SET
from .salas_de_equipamentos import SEQPrimaria, SEQSecundaria
from dataclasses import dataclass, field
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


class QuantificacaoBlock:
    def __init__(self, quantificacao: dict[str, int | float] = None) -> None:
        quantificacao = quantificacao or {}
        self.quantificacao: dict[str, int | float] = quantificacao

    def clean(self) -> 'QuantificacaoBlock':
        self.quantificacao = remove_blank(self.quantificacao)
        return self

    def __add__(self, other: 'QuantificacaoBlock') -> 'QuantificacaoBlock':
        added = self.quantificacao.copy()
        for key, value in other.quantificacao.items():
            if key in added:
                added[key] += value
            else:
                added[key] = value
        return self.__class__(added)


class QuantificacaoEquipamentosBlock(QuantificacaoBlock):
    def __init__(self, quantificacao: QuantificacaoDeEquipamentosDeFibra | dict[str, int | float] = None,
                 carac_fib: CaracteristicasFibra = None) -> None:
        if isinstance(quantificacao, dict):
            super().__init__(quantificacao)
            return
        if carac_fib is None:
            raise ValueError
        super().__init__(
            {
                "Chassi DIO (Distribuido Interno Optico) com 24 portas - 1U - 19": quantificacao.dios,
                "Bandeja para emenda de fibra no DIO - (comporta ate 12 emendas)": quantificacao.caixas_de_emenda,
                "Terminador Optico para 8 fibras": quantificacao.terminadores_opticos,
                f"Acoplador optico {carac_fib.nucleo} x 125um - {carac_fib.modo} - LC - duplo": quantificacao.acopladores_lc_duplo,
                f"Cordao Optico {carac_fib.nucleo} x 125um - {carac_fib.modo} - 3m - duplo - conector LC": quantificacao.cordao_optico,
                f"Pig tail {carac_fib.nucleo} x 125um - {carac_fib.modo} - 1,5m - simples - conector LC": quantificacao.pig_tails_simples,
                f"Pig tail {carac_fib.nucleo} x 125um - {carac_fib.modo} - 3,0m - duplo - conector LC": quantificacao.pig_tails_duplos
            }
        )


class QuantificacaoBackboneBlock(QuantificacaoBlock):
    def __init__(self, carac_fib: CaracteristicasFibra | dict[str, int | float] = None,
                 fibras: dict[int, float] = None) -> None:
        if isinstance(carac_fib, dict) or carac_fib is None:
            super().__init__(carac_fib)
            return
        fibras = fibras or {}
        super().__init__(
            {
                f"Cabo de Fibra Optica {carac_fib.categoria} (FO{carac_fib.modo}{carac_fib.indice}) {carac_fib.nucleo} x 125um - com {key * 2} fibras": quantidade
                for key, quantidade in fibras.items()
            }
        )


@dataclass
class Quantificacao:
    total: QuantificacaoBlock
    seq_primaria: QuantificacaoBlock = field(default=QuantificacaoBlock())
    seqs_secundarias: QuantificacaoBlock = field(default=QuantificacaoBlock())
    sets: QuantificacaoBlock = field(default=QuantificacaoBlock())
    backbone_primario: QuantificacaoBlock = field(default=QuantificacaoBlock())
    backbone_secundarios: QuantificacaoBlock = field(default=QuantificacaoBlock())

    def to_dict(self) -> dict[str, dict[str, int | float]]:
        ret = {
            "Quantificação total": self.total.quantificacao,
            "Quantificação SEQ primaria": self.seq_primaria.quantificacao,
            "Quantificação SEQ(s) secundaria(s)": self.seqs_secundarias.quantificacao,
            "Quantificação SETs": self.sets.quantificacao,
            "Quantificação Backbone de primeiro nível": self.backbone_primario.quantificacao,
            "Quantificação Backbone de secundo nível": self.backbone_secundarios.quantificacao
        }

        return remove_blank(ret)


def dicts_to_xlsx(outer_dict: dict[str, dict]) -> bytes:
    quantification = pd.DataFrame()
    start = 0

    for inner_dict_str in outer_dict:
        space = pd.Series([''] * (1000 - len(outer_dict[inner_dict_str])))
        space_full = pd.Series([''] * 1000)

        quantification.insert(
            start,
            f'{inner_dict_str} - Material',
            pd.concat([pd.Series(outer_dict[inner_dict_str].keys()), space],
                      ignore_index=True)
        )
        quantification.insert(
            start + 1,
            f'{inner_dict_str} - Quantidade',
            pd.concat([pd.Series(outer_dict[inner_dict_str].values()), space],
                      ignore_index=True),
            allow_duplicates=True
        )
        quantification.insert(start + 2, ' ', space_full, allow_duplicates=True)

        start += 3

    return get_xls(quantification)


def get_xls(df: pandas.DataFrame) -> bytes:
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, 'quantificacao.xlsx')
        df.to_excel(file_path, index=False)
        with open(file_path, 'rb') as f:
            return f.read()


def remove_blank(d: dict) -> dict:
    keys_to_remove = [key for key, value in d.items() if not value]
    for key in keys_to_remove:
        del d[key]
    return d


def _calcular_quantificacao_projeto_simples(clean_input: CleanedInput) -> Quantificacao:
    seq_secundaria: SEQSecundaria =  clean_input.seq

    quantificacao_backboenes_secundarios = QuantificacaoBackboneBlock(
        clean_input.caracteristicas_set,
        seq_secundaria.quantificacao_backbones_de_segundo_nivel_por_disciplina
    ).clean()

    quantificacao_total = (
        QuantificacaoEquipamentosBlock(
            seq_secundaria.quantificacao_equipamentos_de_fibra_sets,
            clean_input.caracteristicas_set
        ).clean()
        + QuantificacaoEquipamentosBlock(
            seq_secundaria.quantificacao_equipamentos_de_fibra_seq,
            clean_input.caracteristicas_seq_secundaria
        ).clean()
        + quantificacao_backboenes_secundarios
    ).clean()

    quantificacao_sets = QuantificacaoEquipamentosBlock(
        seq_secundaria.pure_quantificacao_equipamentos_de_fibra_sets,
        clean_input.caracteristicas_set
    ).clean()

    quantificacao_seq_secundaria = (
        QuantificacaoEquipamentosBlock(
            seq_secundaria.quantificacao_equipamentos_de_fibra_do_tipo_set_na_seq,
            clean_input.caracteristicas_set
        ).clean()
        + QuantificacaoEquipamentosBlock(
            seq_secundaria.quantificacao_equipamentos_de_fibra_seq,
            clean_input.caracteristicas_seq_secundaria
        ).clean()
    ).clean()

    return Quantificacao(
        total=quantificacao_total,
        seqs_secundarias=quantificacao_seq_secundaria,
        sets=quantificacao_sets,
        backbone_secundarios=quantificacao_backboenes_secundarios
    )


def _calcular_quantificacao_total_projeto_complexo(clean_input: CleanedInput) -> Quantificacao:
    seq_primaria: SEQPrimaria = clean_input.seq

    quantificacao_backboenes_primarios = QuantificacaoBackboneBlock(
        clean_input.caracteristicas_seq_secundaria,
        seq_primaria.quantificacao_backbones_de_primeiro_nivel_por_disciplina
    ).clean()

    quantificacao_backboenes_secundarios = QuantificacaoBackboneBlock(
        clean_input.caracteristicas_set,
        seq_primaria.quantificacao_backbones_de_segundo_nivel_por_disciplina
    ).clean()

    quantificacao_total = (
        QuantificacaoEquipamentosBlock(
            seq_primaria.quantificacao_equipamentos_de_fibra_sets,
            clean_input.caracteristicas_set
        ).clean()
        + QuantificacaoEquipamentosBlock(
            seq_primaria.quantificacao_equipamentos_de_fibra_seqs_secundarias,
            clean_input.caracteristicas_seq_secundaria
        ).clean()
        + QuantificacaoEquipamentosBlock(
            seq_primaria.quantificacao_equipamentos_de_fibra_seq_primaria,
            clean_input.caracteristicas_seq_primaria
        ).clean()
        + quantificacao_backboenes_primarios
        + quantificacao_backboenes_secundarios
    ).clean()

    quantificacao_sets = QuantificacaoEquipamentosBlock(
        seq_primaria.pure_quantificacao_equipamentos_de_fibra_sets,
        clean_input.caracteristicas_set
    ).clean()

    quantificacao_seqs_secundarias = (
        QuantificacaoEquipamentosBlock(
            seq_primaria.pure_quantificacao_equipamentos_de_fibra_seqs_secundarias,
            clean_input.caracteristicas_seq_secundaria
        ).clean()
        + QuantificacaoEquipamentosBlock(
            seq_primaria.quantificacao_equipamentos_de_fibra_do_tipo_set_seqs_secundarias,
            clean_input.caracteristicas_set
        ).clean()
    ).clean()

    quantificacao_seq_primaria = (
        QuantificacaoEquipamentosBlock(
            seq_primaria.quantificacao_equipamentos_de_fibra_seq_primaria,
            clean_input.caracteristicas_seq_primaria
        ).clean()
        + QuantificacaoEquipamentosBlock(
            seq_primaria.quantificacao_equipamentos_de_fibra_do_tipo_seq_secondaria_na_seq_primaria,
            clean_input.caracteristicas_seq_secundaria
        ).clean()
    ).clean()

    return Quantificacao(
        total=quantificacao_total,
        seq_primaria=quantificacao_seq_primaria,
        seqs_secundarias=quantificacao_seqs_secundarias,
        sets=quantificacao_sets,
        backbone_primario=quantificacao_backboenes_primarios,
        backbone_secundarios=quantificacao_backboenes_secundarios
    )


def _calcular_quantificacao_projeto(
        clean_input: CleanedInput
) -> dict[str, dict[str, int | float]]:
    return (
        _calcular_quantificacao_total_projeto_complexo(clean_input)
        if clean_input.backbone_primario else
        _calcular_quantificacao_projeto_simples(clean_input)
    ).to_dict()


if __name__ == "__main__":
    def main():
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
                print(f"{i} : {dicionario[key][i]}")
    main()
