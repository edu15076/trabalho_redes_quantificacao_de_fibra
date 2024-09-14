from dataclasses import dataclass

from fibra.equipamentos_de_fibra import QuantificacaoDeEquipamentosDeFibra, DIO
from fibra.sala_de_telecomunicacoes import SET


@dataclass
class CaracteristicaFibra:
    modo: str
    nucleo: str
    indice: str
    categoria: str


class SEQSecundaria:
    def __init__(
            self, disciplinas: int, andar: int, medida_basica: float,
            caracteristicas: CaracteristicaFibra,
            disciplinas_por_backbones_por_andar: dict[int, list[int]] = None
    ):
        self.disciplinas = disciplinas
        self.andar = andar
        self.medida_basica = medida_basica
        self.caracteristicas = caracteristicas
        self.dio_externo = DIO(self.disciplinas)

        if disciplinas_por_backbones_por_andar is not None:
            self.sets: list[SET] = [
                SET(andar, disciplinas_por_backbones)
                for andar, disciplinas_por_backbones in
                    disciplinas_por_backbones_por_andar.items()
            ]
            self.dio_interno = DIO(self._quantidade_total_de_disciplinas_sets)
        else:
            self.sets: list[SET] = []
            self.dio_interno = DIO(0)

    def _calcular_tamanho_da_fibra(self, andar: int) -> float:
        if andar > self.andar:
            return (andar - self.andar + 2) * self.medida_basica
        return (self.andar - andar) * self.medida_basica

    @property
    def _quantificacao_fibras_sets(self) -> dict[int, float]:
        quantificacao: dict[int, float] = {}
        for sala in self.sets:
            dist = self._calcular_tamanho_da_fibra(sala.andar)
            for disciplinas, qtd in sala.quantificacao_de_fibras_por_disciplinas.items():
                if disciplinas not in quantificacao:
                    quantificacao[disciplinas] = dist * qtd
                else:
                    quantificacao[disciplinas] += dist * qtd
        return quantificacao

    @property
    def _quantificacao_equipamentos_de_fibra_sets(
            self) -> QuantificacaoDeEquipamentosDeFibra:
        quantificacao = QuantificacaoDeEquipamentosDeFibra.get_zero()
        for sala in self.sets:
            quantificacao += sala.quantificacao_de_equipamentos_de_fibra
        return quantificacao

    @property
    def _quantificacao_equipamentos_de_fibra_seq(
            self) -> QuantificacaoDeEquipamentosDeFibra:
        return (self.dio_interno.quantificacao_de_equipamentos
                + self.dio_externo.quantificacao_de_equipamentos)

    @property
    def _quantidade_total_de_disciplinas_sets(self) -> int:
        return sum(sala.quantidade_total_de_disciplinas for sala in self.sets)

    @property
    def quantificacao_equipamentos_de_fibra(self):
        return (self._quantificacao_equipamentos_de_fibra_sets
                + self._quantificacao_equipamentos_de_fibra_seq)

    @property
    def quantificacao_fibras_por_disciplina(self) -> dict[int, float]:
        return self._quantificacao_fibras_sets


class SEQPrimaria:
    pass
