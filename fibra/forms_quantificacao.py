from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field


class FormConfig(forms.Form):
    modo_fibra_seq_primaria = forms.CharField(label="Modo da Fibra na SEQPrincipal")
    nucleo_fibra_seq_primaria = forms.CharField(label="Núcleo da Fibra na SEQPrincipal")
    indice_fibra_seq_primaria = forms.CharField(label="Índice da Fibra na SEQPrincipal")
    categoria_fibra_seq_primaria = forms.CharField(label="Categoria da Fibra na SEQPrincipal")

    modo_fibra_seq_secundaria = forms.CharField(label="Modo da Fibra na SEQSecundaria")
    nucleo_fibra_seq_secundaria = forms.CharField(label="Núcleo da Fibra na SEQSecundaria")
    indice_fibra_seq_secundaria = forms.CharField(label="Índice da Fibra na SEQSecundaria")
    categoria_fibra_seq_secundaria = forms.CharField(label="Categoria da Fibra na SEQSecundaria")

    modo_fibra_set = forms.CharField(label="Modo da Fibra na SET")
    nucleo_fibra_set = forms.CharField(label="Núcleo da Fibra na SET")
    indice_fibra_set = forms.CharField(label="Índice da Fibra na SET")
    categoria_fibra_set = forms.CharField(label="Categoria da Fibra na SET")

    backbone_primario = forms.BooleanField(label="Backbone Primário", required=False)
    backbone_secundario = forms.BooleanField(label="Backbone Secundário", required=False)


class FormSEQPrimaria(forms.Form):
    medida_basica_seq_primaria = forms.FloatField(label="Medida Básica SEQPrimaria", required=False)
    disciplinas_seq_primaria = forms.IntegerField(label="Disciplinas SEQPrimaria", required=False)


class FormSEQSecundaria(forms.Form):
    andar = forms.CharField(label="Andar")
    medida_basica_seq_secundaria = forms.FloatField(label="Medida Básica SEQSecundaria", required=False)
    disciplinas_seq_secundaria = forms.IntegerField(label="Disciplinas SEQSecundaria", required=False)

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
    andar = forms.CharField(label="Andar")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('andar', css_class='andar_set'),
        )
