from collections import defaultdict

from fibra.equipamentos_de_fibra import EquipamentoDeFibra, TO, DIO, \
    QuantificacaoDeEquipamentosDeFibra


class SET:
    def __init__(self, andar: int, disciplinas_por_backbones: list[int]):
        self.andar = andar
        self.equipamentos_de_fibra: list[EquipamentoDeFibra] = (
            self._instanciar_equipamentos_por_backbone(disciplinas_por_backbones))

    def _instanciar_equipamentos_por_backbone(
            self, disciplinas_por_backbones: list[int]
    ) -> list[EquipamentoDeFibra]:
        return [
            TO(disciplinas) if disciplinas <= 4 else DIO(disciplinas)
            for disciplinas in disciplinas_por_backbones
        ]

    @property
    def quantificacao_de_equipamentos_de_fibra(
            self) -> QuantificacaoDeEquipamentosDeFibra:
        quantificacao = QuantificacaoDeEquipamentosDeFibra.get_zero()
        for equipamento_de_fibra in self.equipamentos_de_fibra:
            quantificacao += equipamento_de_fibra.quantificacao_de_equipamentos
        return quantificacao

    @property
    def quantificacao_de_fibras_por_disciplinas(self) -> dict[int, int]:
        quantificacao = {}
        for equipamento_de_fibra in self.equipamentos_de_fibra:
            if equipamento_de_fibra.disciplinas in quantificacao:
                quantificacao[equipamento_de_fibra.disciplinas] += 1
            else:
                quantificacao[equipamento_de_fibra.disciplinas] = 1
        return quantificacao

    @property
    def quantidade_total_de_disciplinas(self) -> int:
        return sum(equipamento_fibra.disciplinas
                   for equipamento_fibra in self.equipamentos_de_fibra)
