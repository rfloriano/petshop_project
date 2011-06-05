#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from django.forms.util import ErrorList
from models import AtendimentoBanhoTosa

class AtendimentoBanhoTosaForm(forms.models.ModelForm):
    class Meta:
        model = AtendimentoBanhoTosa

    def clean(self):
        if self.cleaned_data.get("cliente") is None:
            msg = u"Por favor preencha este campo obrigatório."
            self._errors["cliente"] = ErrorList([msg])
        if self.cleaned_data.get("animal") is None:
            msg = u"Por favor preencha este campo obrigatório."
            self._errors["animal"] = ErrorList([msg])
        return self.cleaned_data
