from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class QuantificacaoDeEquipamentosDeFibra:
    dios: int
    caixas_de_emenda: int
    conectores_lc_duplo: int
    acopladores_lc_duplo: int
    cordao_optico: int
    pig_tails_simples: int
    pig_tails_duplos: int
    terminadores_opticos: int

    @classmethod
    def get_zero(cls):
        return QuantificacaoDeEquipamentosDeFibra(0, 0, 0, 0, 0, 0, 0, 0)

    def __add__(
            self, other: 'QuantificacaoDeEquipamentosDeFibra'
    ) -> 'QuantificacaoDeEquipamentosDeFibra':
        return QuantificacaoDeEquipamentosDeFibra(
            self.dios + other.dios,
            self.caixas_de_emenda + other.caixas_de_emenda,
            self.conectores_lc_duplo + other.conectores_lc_duplo,
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
            self.conectores_lc_duplo * k,
            self.acopladores_lc_duplo * k,
            self.cordao_optico * k,
            self.pig_tails_simples * k,
            self.pig_tails_duplos * k,
            self.terminadores_opticos * k
        )


class EquipamentoDeFibra(ABC):
    def __init__(self, disciplinas):
        self.disciplinas = disciplinas

    @abstractmethod
    @property
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
            conectores_lc_duplo=self._quantidade_de_conectores_lc_duplo,
            acopladores_lc_duplo=self._quantidade_de_acopladores_lc_duplo,
            cordao_optico=self._quantidade_de_cordoes_optico,
            pig_tails_simples=self._quantidade_de_pig_tails_simples,
            pig_tails_duplos=0,
            terminadores_opticos=0
        )

    @property
    def _quantidade_de_dios(self) -> int:
        raise NotImplemented

    @property
    def _quantidade_de_caixas_de_emenda(self) -> int:
        raise NotImplemented

    @property
    def _quantidade_de_conectores_lc_duplo(self) -> int:
        raise NotImplemented

    @property
    def _quantidade_de_pig_tails_simples(self) -> int:
        raise NotImplemented

    @property
    def _quantidade_de_cordoes_optico(self) -> int:
        raise NotImplemented

    @property
    def _quantidade_de_acopladores_lc_duplo(self) -> int:
        raise NotImplemented


class TO(EquipamentoDeFibra):
    def __init__(self, disciplinas):
        super().__init__(disciplinas)

    @property
    def quantificacao_de_equipamentos(self) -> QuantificacaoDeEquipamentosDeFibra:
        return QuantificacaoDeEquipamentosDeFibra(
            dios=0,
            caixas_de_emenda=0,
            conectores_lc_duplo=0,
            acopladores_lc_duplo=0,
            cordao_optico=0,
            pig_tails_simples=0,
            pig_tails_duplos=self._quantidade_de_pig_tails_duplos,
            terminadores_opticos=self._quantidade_de_terminadores_opticos
        )

    @property
    def _quantidade_de_terminadores_opticos(self) -> int:
        raise NotImplemented

    @property
    def _quantidade_de_pig_tails_duplos(self) -> int:
        raise NotImplemented
