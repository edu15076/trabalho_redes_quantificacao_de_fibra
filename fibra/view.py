from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views.generic import View
from .forms_quantificacao import FormConfig, FormSEQPrimaria, FormSEQSecundaria, FormSET
import json
from dataclasses import dataclass

from .sala_de_telecomunicacoes import SET
from .salas_de_equipamentos import SEQPrimaria, SEQSecundaria


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


class InputParser:
    def __init__(self, data):
        self.data = data
        self._backbone_primario = self.data['config']['backbone_primario']
        self._backbone_secundario = self.data['config']['backbone_secundario']

    def _parse_set(self, set_data: dict) -> SET:
        return SET(
            int(set_data['andar']),
            [int(disciplina) for disciplina in set_data['disciplinas_por_backbone']]
        )

    def _parse_seq_secundaria(self, seq_data: dict) -> SEQSecundaria:
        sets = (
            [self._parse_set(set) for set in seq_data['sets']]
            if self._backbone_secundario else None
        )
        return SEQSecundaria(
            int(seq_data['disciplinas']), int(seq_data['andar']), int(seq_data['medida_basica']), sets
        )

    def _parse_seq_primaria(self) -> SEQPrimaria:
        seq_data = self.data['seq_primaria']
        seqs_secundarias = [
            self._parse_seq_secundaria(seq) for seq in self.data['seqs_secundarias']
        ]
        return SEQPrimaria(
            int(seq_data['disciplinas']), int(seq_data['medida_basica']), seqs_secundarias
        )

    def _parse_caracteristicas(self) -> tuple:
        config = self.data['config']
        return (
            CaracteristicasFibra(
                modo=config['modo_set'],
                nucleo=config['nucleo_set'],
                indice=config['indice_set'],
                categoria=config['categoria_set']
            ),
            CaracteristicasFibra(
                modo=config['modo_seq_secundaria'],
                nucleo=config['nucleo_seq_secundaria'],
                indice=config['indice_seq_secundaria'],
                categoria=config['categoria_seq_secundaria']
            ),
            CaracteristicasFibra(
                modo=config['modo_seq_primaria'],
                nucleo=config['nucleo_seq_primaria'],
                indice=config['indice_seq_primaria'],
                categoria=config['categoria_seq_primaria']
            )
        )

    def parse(self) -> CleanedInput:
        (
            caracteristicas_set,
            caracteristicas_seq_secundaria,
            caracteristicas_seq_primaria
        ) = self._parse_caracteristicas()

        if self._backbone_primario:
            return CleanedInput(
                seq=self._parse_seq_primaria(),
                caracteristicas_set=caracteristicas_set,
                caracteristicas_seq_secundaria=caracteristicas_seq_secundaria,
                caracteristicas_seq_primaria=caracteristicas_seq_primaria,
                backbone_primario=self._backbone_primario,
                backbone_secundario=self._backbone_secundario
            )

        return CleanedInput(
            seq=self._parse_seq_secundaria(self.data['seqs_secundarias'][0]),
            caracteristicas_set=caracteristicas_set,
            caracteristicas_seq_secundaria=caracteristicas_seq_secundaria,
            caracteristicas_seq_primaria=caracteristicas_seq_primaria,
            backbone_primario=self._backbone_primario,
            backbone_secundario=self._backbone_secundario
        )


class QuantificacaoView(View):
    template_name = 'quantificacao_form.html'

    def get(self, request):
        form_config = FormConfig()
        form_seq_primaria = FormSEQPrimaria()
        form_seq_secundaria = FormSEQSecundaria()
        form_set = FormSET()
        return render(request, self.template_name, {
            'form_config': form_config,
            'form_seq_primaria': form_seq_primaria,
            'form_seq_secundaria': form_seq_secundaria,
            'form_set': form_set,
        })

    def post(self, request):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = json.load(request)
            print(data)
            parsed_data = InputParser(data).parse()
            print(parsed_data)
            # Process the JSON data
            # ...
            return JsonResponse({'message': 'Data saved successfully!'})
        else:
            form_config = FormConfig(request.POST)
            if form_config.is_valid():
                # Process the data
                # ...
                return HttpResponse("Data saved successfully!")
            else:
                return render(request, self.template_name, {
                    'form_config': form_config,
                    'form_seq_primaria': FormSEQPrimaria(),
                    'form_seq_secundaria': FormSEQSecundaria(),
                    'form_set': FormSET(),
                })