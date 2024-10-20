from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML

MODOS_FIBRA = [
    ('', 'Não selecionado'),
    ('MM', 'Multimodo'),
    ('SM', 'Monomodo'),
]

CATEGORIAS_FIBRA = [
    ('', 'Não selecionado'),
    ('Loose', 'Loose Buffer'),
    ('Tight', 'Tight Buffer'),
    ('Loose Auto Sustentável', 'Loose Auto Sustentável'),
]

INDICES_FIBRA = [
    ('', 'Não selecionado'),
    ('IG', 'Índice Gradual'),
    ('ID', 'Índice Degrau'),
]

NUCLEOS_FIBRA = [
    ('', 'Não selecionado'),
    ('9', '9µm'),
    ('50', '50µm'),
    ('62.5', '62.5µm'),
]

FIBRA_INTERFACE = [
    ('', 'Não selecionado'),
    ('MM50', 'Multimodo 50µm'),
    ('MM62.5', 'Multimodo 62.5µm'),
    ('SM9', 'Monomodo 9µm'),
]

TIPO_QUANTIFICACAO_INTERFACE = [
    ('CAMPUS', 'Campus'),
    ('PREDIO', 'Prédio'),
]


class FormChoicesInterface(forms.Form):
    tipo_quantificacao = forms.ChoiceField(
        choices=TIPO_QUANTIFICACAO_INTERFACE,
        widget=forms.RadioSelect,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            HTML('<h2>Tipo de quantificação</h2>'),
            Field('tipo_quantificacao'),
        )


class FormConfigCampusInterface(forms.Form):
    modo_fibra_seq_primaria = forms.ChoiceField(
        label="Fibra na SEQ primária",
        choices=FIBRA_INTERFACE,
    )
    modo_fibra_seq_secundaria = forms.ChoiceField(
        label="Fibra nas SEQs secundárias",
        choices=FIBRA_INTERFACE,
    )
    modo_fibra_set = forms.ChoiceField(
        label="Fibra nas SETs",
        choices=FIBRA_INTERFACE,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            HTML('<h2>Tipos de fibra</h2>'),
            Field('modo_fibra_seq_primaria'),
            Field('modo_fibra_seq_secundaria'),
            Field('modo_fibra_set'),
        )


class FormConfigPredioInterface(forms.Form):
    modo_fibra_seq_primaria = forms.ChoiceField(
        label="Fibra na SEQ",
        choices=FIBRA_INTERFACE,
    )
    modo_fibra_set = forms.ChoiceField(
        label="Fibra nas SETs",
        choices=FIBRA_INTERFACE,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            HTML('<h2>Tipos de fibra</h2>'),
            Field('modo_fibra_seq_primaria'),
            Field('modo_fibra_set'),
        )


class FormSEQPrimaria(forms.Form):
    medida_basica_seq_primaria = forms.FloatField(
        label="Distância média das SEQs secundárias à SEQ primária",
        widget=forms.NumberInput(attrs={'min': '0', 'step': '0.1'})
    )
    disciplinas_seq_primaria = forms.IntegerField(
        label="Disciplinas chegando à SEQ primária",
        widget=forms.NumberInput(attrs={'min': '1', 'step': '1'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('medida_basica_seq_primaria'),
            Field('disciplinas_seq_primaria'),
        )


class FormSEQSecundaria(forms.Form):
    andar = forms.IntegerField(
        label="Andar"
    )
    medida_basica_seq_secundaria = forms.FloatField(
        label="Pé direito",
        widget=forms.NumberInput(attrs={'min': '0', 'step': '0.1'})
    )
    disciplinas_seq_secundaria = forms.IntegerField(
        label="Disciplinas chegando na SEQ",
        widget=forms.NumberInput(attrs={'min': '1', 'step': '1'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('andar', css_class='andar_seq_secundaria'),
            Field('medida_basica_seq_secundaria', css_class='medida_basica_seq_secundaria'),
            Field('disciplinas_seq_secundaria', css_class='disciplinas_seq_secundaria'),
        )


class FormSET(forms.Form):
    andar = forms.IntegerField(label="Andar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('andar', css_class='andar_set'),
        )
