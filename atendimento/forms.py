#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django import forms
from django.forms.util import ErrorList
from models import Atendimento
from veterinario.models import ItemAtedimentoVeterinario
from banhotosa.models import ItemAtendimentoBanhoTosa

class AtendimentoAbstractForm(forms.models.ModelForm):
    class Meta:
        model = Atendimento
        
    def clean(self):
        if self.cleaned_data.get("cliente") is None:
            msg = u"Por favor preencha este campo obrigatório."
            self._errors["cliente"] = ErrorList([msg])
        return self.cleaned_data

class ItemAtedimentoVeterinarioForm(forms.models.ModelForm):
    class Meta:
        model = ItemAtedimentoVeterinario
        
    def clean(self):
        if self.cleaned_data.get("animal") is None:
            msg = u"Por favor preencha este campo obrigatório."
            self._errors["animal"] = ErrorList([msg])
        return self.cleaned_data

class ItemAtendimentoBanhoTosaForm(forms.models.ModelForm):
    class Meta:
        model = ItemAtendimentoBanhoTosa
        
    def clean(self):
        if self.cleaned_data.get("animal") is None:
            msg = u"Por favor preencha este campo obrigatório."
            self._errors["animal"] = ErrorList([msg])
        return self.cleaned_data
