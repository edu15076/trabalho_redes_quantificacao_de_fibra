from dataclasses import dataclass
from abc import ABC, abstractmethod
import math

@dataclass
class QuantificacaoDeEquipamentosDeFibra:
    dios: int = 0
    caixas_de_emenda: int = 0
    acopladores_lc_duplo: int = 0
    cordao_optico: int = 0
    pig_tails_simples: int = 0
    pig_tails_duplos: int = 0
    terminadores_opticos: int = 0

    @classmethod
    def get_zero(cls):
        return QuantificacaoDeEquipamentosDeFibra()

    def __add__(
            self, other: 'QuantificacaoDeEquipamentosDeFibra'
    ) -> 'QuantificacaoDeEquipamentosDeFibra':
        return QuantificacaoDeEquipamentosDeFibra(
            self.dios + other.dios,
            self.caixas_de_emenda + other.caixas_de_emenda,
            self.acopladores_lc_duplo + other.acopladores_lc_duplo,
            self.cordao_optico + other.cordao_optico,
            self.pig_tails_simples + other.pig_tails_simples,
            self.pig_tails_duplos + other.pig_tails_duplos,
            self.terminadores_opticos + other.terminadores_opticos
        )

    def __mul__(self, k: int | float) -> 'QuantificacaoDeEquipamentosDeFibra':
        return QuantificacaoDeEquipamentosDeFibra(
            self.dios * k,
            self.caixas_de_emenda * k,
            self.acopladores_lc_duplo * k,
            self.cordao_optico * k,
            self.pig_tails_simples * k,
            self.pig_tails_duplos * k,
            self.terminadores_opticos * k
        )


class EquipamentoDeFibra(ABC):
    def __init__(self, disciplinas):
        self.disciplinas = disciplinas


    @property
    @abstractmethod
    def quantificacao_de_equipamentos(self) -> QuantificacaoDeEquipamentosDeFibra:
        raise NotImplemented


class DIO(EquipamentoDeFibra):
    def __init__(self, disciplinas):
        super().__init__(disciplinas)

    @property
    def quantificacao_de_equipamentos(self) -> QuantificacaoDeEquipamentosDeFibra:
        return QuantificacaoDeEquipamentosDeFibra(
            dios=self._quantidade_de_dios,
            caixas_de_emenda=self._quantidade_de_caixas_de_emenda,
            acopladores_lc_duplo=self._quantidade_de_acopladores_lc_duplo,
            cordao_optico=self._quantidade_de_cordoes_optico,
            pig_tails_simples=self._quantidade_de_pig_tails_simples,
            pig_tails_duplos=0,
            terminadores_opticos=0
        )

    @property
    def _quantidade_de_dios(self) -> int:
        return math.ceil(self.disciplinas / 12)
    
    @property
    def _quantidade_de_caixas_de_emenda(self) -> int:
        return math.ceil(self.disciplinas / 6)

    @property
    def _quantidade_de_pig_tails_simples(self) -> int:
        return self.disciplinas * 2 

    @property
    def _quantidade_de_cordoes_optico(self) -> int:
        return self.disciplinas

    @property
    def _quantidade_de_acopladores_lc_duplo(self) -> int:
        return self.disciplinas


class TO(EquipamentoDeFibra):
    def __init__(self, disciplinas):
        super().__init__(disciplinas)

    @property
    def quantificacao_de_equipamentos(self) -> QuantificacaoDeEquipamentosDeFibra:
        return QuantificacaoDeEquipamentosDeFibra(
            dios=0,
            caixas_de_emenda=0,
            acopladores_lc_duplo=0,
            cordao_optico=0,
            pig_tails_simples=0,
            pig_tails_duplos=self._quantidade_de_pig_tails_duplos,
            terminadores_opticos=self._quantidade_de_terminadores_opticos
        )

    @property
    def _quantidade_de_terminadores_opticos(self) -> int:
        return math.ceil(self.disciplinas / 4)
    
    @property
    def _quantidade_de_pig_tails_duplos(self) -> int:
        return self._quantidade_de_terminadores_opticos * 4

if __name__ == "__main__":
    dio_interno = DIO(12)
    dio_externo = DIO(4)
    to_set = TO(4)
    print(f"DIO INTERNO: {dio_interno.quantificacao_de_equipamentos}")
    print(f"DIO EXTERNO: {dio_externo.quantificacao_de_equipamentos + dio_interno.quantificacao_de_equipamentos}")
    print(f"TO SET: {to_set.quantificacao_de_equipamentos}")

    print(f"Exercicio do adelson {dio_interno.quantificacao_de_equipamentos + dio_externo.quantificacao_de_equipamentos + to_set.quantificacao_de_equipamentos * 3}")