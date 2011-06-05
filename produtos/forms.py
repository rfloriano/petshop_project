#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from django.forms.util import ErrorList
from models import Venda

class VendaForm(forms.models.ModelForm):
    class Meta:
        model = Venda

    def clean(self):
        if self.cleaned_data.get("cliente") is None:
            msg = u"Por favor preencha este campo obrigatório."
            self._errors["cliente"] = ErrorList([msg])
        return self.cleaned_data
