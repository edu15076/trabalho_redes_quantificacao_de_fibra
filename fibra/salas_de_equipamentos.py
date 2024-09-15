from fibra.equipamentos_de_fibra import QuantificacaoDeEquipamentosDeFibra, DIO
from fibra.sala_de_telecomunicacoes import SET


class SEQSecundaria:
    def __init__(
            self, disciplinas: int, andar: int, medida_basica: float,
            sets: list[SET] = None
    ):
        self.disciplinas = disciplinas
        self.andar = andar
        self.medida_basica = medida_basica
        self.dio_externo = DIO(self.disciplinas)
        self.sets: list[SET] = sets if sets else []
        self.dio_interno = DIO(self._quantidade_total_de_pares_de_fibra_sets)

    def _calcular_tamanho_da_fibra(self, andar: int) -> float:
        if andar > self.andar:
            return (andar - self.andar + 2) * self.medida_basica
        return (self.andar - andar) * self.medida_basica

    @property
    def quantificacao_backbones_de_segundo_nivel_por_disciplina(self) -> dict[int, float]:
        quantificacao: dict[int, float] = {}
        for sala in self.sets:
            dist = self._calcular_tamanho_da_fibra(sala.andar)
            for disciplinas, qtd in sala.quantificacao_de_fibras_por_disciplinas.items():
                if disciplinas not in quantificacao:
                    quantificacao[disciplinas] = dist * qtd * 1.2
                else:
                    quantificacao[disciplinas] += dist * qtd * 1.2
        return quantificacao

    @property
    def quantificacao_equipamentos_de_fibra_sets(
            self) -> QuantificacaoDeEquipamentosDeFibra:
        quantificacao = QuantificacaoDeEquipamentosDeFibra.get_zero()
        for sala in self.sets:
            quantificacao += sala.quantificacao_de_equipamentos_de_fibra
        # o dio interno aparece aqui por usar as mesmas características de fibra das sets
        return quantificacao + self.dio_interno.quantificacao_de_equipamentos

    @property
    def quantificacao_equipamentos_de_fibra_seq(
            self) -> QuantificacaoDeEquipamentosDeFibra:
        return self.dio_externo.quantificacao_de_equipamentos

    @property
    def _quantidade_total_de_pares_de_fibra_sets(self) -> int:
        return sum(sala.quantidade_total_de_disciplinas for sala in self.sets)


class SEQPrimaria:
    def __init__(self, disciplinas: int, medida_basica: float,
                 seqs_secundaria: list[SEQSecundaria] = None):
        self.disciplinas = disciplinas
        self.medida_basica = medida_basica
        self.dio_externo = DIO(self.disciplinas)
        self.seqs_secundaria = seqs_secundaria if seqs_secundaria else []
        self.dio_interno = DIO(self._quantidade_total_de_pares_de_fibra_seqs_secundarias)

    @property
    def quantificacao_backbones_de_segundo_nivel_por_disciplina(self) -> dict[int, float]:
        quantificacao_total: dict[int, float] = {}
        for seq in self.seqs_secundaria:
            for disciplina, valor in seq.quantificacao_backbones_de_segundo_nivel_por_disciplina.items():
                if disciplina not in quantificacao_total:
                    quantificacao_total[disciplina] = valor
                else:
                    quantificacao_total[disciplina] += valor
        return quantificacao_total

    @property
    def quantificacao_equipamentos_de_fibra_seq_primaria(self) -> QuantificacaoDeEquipamentosDeFibra:
        return self.dio_externo.quantificacao_de_equipamentos

    @property
    def quantificacao_equipamentos_de_fibra_seqs_secundarias(self) -> QuantificacaoDeEquipamentosDeFibra:
        return sum(
            (seq.quantificacao_equipamentos_de_fibra_seq for seq in self.seqs_secundaria),
            QuantificacaoDeEquipamentosDeFibra.get_zero()
        ) + self.dio_interno.quantificacao_de_equipamentos

    @property
    def quantificacao_equipamentos_de_fibra_sets(self) -> QuantificacaoDeEquipamentosDeFibra:
        zero = QuantificacaoDeEquipamentosDeFibra.get_zero()
        return sum((seq.quantificacao_equipamentos_de_fibra_sets for seq in self.seqs_secundaria), zero)

    @property
    def quantificacao_backbones_de_primeiro_nivel_por_disciplina(self) -> dict[int, float]:
        quantificacao_total: dict[int, float] = {}
        for seq in self.seqs_secundaria:
            if seq.disciplinas not in quantificacao_total:
                quantificacao_total[seq.disciplinas] = self.medida_basica * 1.2
            else:
                quantificacao_total[seq.disciplinas] += self.medida_basica * 1.2
        return quantificacao_total

    @property
    def _quantidade_total_de_pares_de_fibra_seqs_secundarias(self) -> int:
        return sum(sala.disciplinas for sala in self.seqs_secundaria)
