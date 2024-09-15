from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from .forms_quantificacao import FormConfig, FormSEQPrimaria, FormSEQSecundaria, FormSET

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
        print(request.POST)
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
