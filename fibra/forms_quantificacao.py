from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, HTML
from django.contrib.admin.utils import help_text_for_field


class FormConfig(forms.Form):
    backbone_primario = forms.BooleanField(
        label="Quantificar Backbone Primário",
        required=False,
        help_text='Implica em quantificar SEQ primária e secundária'
    )
    backbone_secundario = forms.BooleanField(
        label="Backbone Secundário",
        required=False,
        help_text='Implica em quantificar SEQ secundária e SETs'
    )

    modo_fibra_seq_primaria = forms.CharField(label="Modo da Fibra na SEQ primária", required=False,
                                              help_text="SM ou MM")
    nucleo_fibra_seq_primaria = forms.CharField(label="Núcleo da Fibra na SEQ primária", required=False,
                                                help_text="Valor inteiro, 9, 50, ...")
    indice_fibra_seq_primaria = forms.CharField(label="Índice da Fibra na SEQ primária", required=False,
                                                help_text="IG, ID, ...")
    categoria_fibra_seq_primaria = forms.CharField(label="Categoria da Fibra na SEQ primária", required=False,
                                                   help_text='Loose, tight buffer, ...')

    modo_fibra_seq_secundaria = forms.CharField(label="Modo da Fibra nas SEQs secundárias",
                                              help_text="SM ou MM")
    nucleo_fibra_seq_secundaria = forms.CharField(label="Núcleo da Fibra nas SEQs secundárias",
                                                help_text="Valor inteiro, 9, 50, ...")
    indice_fibra_seq_secundaria = forms.CharField(label="Índice da Fibra nas SEQs secundárias",
                                                help_text="IG, ID, ...")
    categoria_fibra_seq_secundaria = forms.CharField(label="Categoria da Fibra nas SEQs secundárias",
                                                   help_text='Loose, tight buffer, ...')

    modo_fibra_set = forms.CharField(label="Modo da Fibra nas SETs", required=False,
                                              help_text="SM ou MM")
    nucleo_fibra_set = forms.CharField(label="Núcleo da Fibra nas SETs", required=False,
                                                help_text="Valor inteiro, 9, 50, ...")
    indice_fibra_set = forms.CharField(label="Índice da Fibra nas SETs", required=False,
                                                help_text="IG, ID, ...")
    categoria_fibra_set = forms.CharField(label="Categoria da Fibra nas SETs", required=False,
                                                   help_text='Loose, tight buffer, ...')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            HTML('<h2>Backbones à serem quantificados</h2>'),
            Field('backbone_primario'),
            Field('backbone_secundario'),
            HTML('<p class="form-text">Ao menos um deve ser selecionado, se ambos forem'
                 ' serão quantificadas a SEQ primária, SEQs secundárias e SETs</p>'),
            HTML('<h2>Dados da fibra chegando na SEQ primária</h2>'),
            Field('modo_fibra_seq_primaria'),
            Field('nucleo_fibra_seq_primaria'),
            Field('indice_fibra_seq_primaria'),
            Field('categoria_fibra_seq_primaria'),
            HTML('<p class="form-text">Podem, preferencialmente devem, estar vazios no '
                 'caso de não estar quantificando Backbones Primário</p>'),
            HTML('<h2>Dados das fibras chegando nas SEQs secundárias</h2>'),
            Field('modo_fibra_seq_secundaria'),
            Field('nucleo_fibra_seq_secundaria'),
            Field('indice_fibra_seq_secundaria'),
            Field('categoria_fibra_seq_secundaria'),
            HTML('<p class="form-text">Deve ser preenchido em qualquer tipo de '
                 'quantificação</p>'),
            HTML('<p class="form-text">Essa configuração é aplicada para todas as '
                 'fibras em SEQs secundárias</p>'),
            HTML('<h2>Dados das fibras chegando nas SETs</h2>'),
            Field('modo_fibra_set'),
            Field('nucleo_fibra_set'),
            Field('indice_fibra_set'),
            Field('categoria_fibra_set'),
            HTML('<p class="form-text">Podem, preferencialmente devem, estar vazios no '
                 'caso de não estar especificando Backbones Secundários</p>'),
            HTML('<p class="form-text">Essa configuração é aplicada para todas as '
                 'fibras em SETs</p>'),
        )


class FormSEQPrimaria(forms.Form):
    medida_basica_seq_primaria = forms.FloatField(label="Distância média das SEQs secundárias à SEQ primária", required=False)
    disciplinas_seq_primaria = forms.IntegerField(label="Disciplinas chegando na SEQ primária", required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            HTML('<h2>Dados SEQ primária</h2>'),
            Field('medida_basica_seq_primaria'),
            Field('disciplinas_seq_primaria'),
            HTML('<p class="form-text">Só devem ser preenchido no caso de estar especificando o backbone principal</p>'),
        )


class FormSEQSecundaria(forms.Form):
    andar = forms.CharField(label="Andar")
    medida_basica_seq_secundaria = forms.FloatField(label="Pé direito SEQ secundária")
    disciplinas_seq_secundaria = forms.IntegerField(label="Disciplinas chegando na SEQ secundária")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('andar', css_class='andar_seq_secundaria'),
            Field('medida_basica_seq_secundaria', css_class='medida_basica_seq_secundaria'),
            Field('disciplinas_seq_secundaria', css_class='disciplinas_seq_secundaria'),
            HTML('<p class="form-text">Uma ou mais devem ser preenchidas no caso de estar quantificando o backbone'
                 ' principal. Caso esteja sendo especificado somente o backbone secundário, deve ser especificado somente'
                 ' uma SEQ secundária</p>'),
        )


class FormSET(forms.Form):
    andar = forms.CharField(label="Andar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('andar', css_class='andar_set'),
        )
