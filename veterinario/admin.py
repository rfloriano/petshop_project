#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from models import *
from forms import AtendimentoVeterinarioForm

class ServicoVeterinarioAdmin(admin.ModelAdmin):
    model = ServicoVeterinario

class ItemAtedimentoVeterinarioInline(admin.TabularInline):
    model = ItemAtedimentoVeterinario
    extra=1
    exclude=["atendimento","animal"]

class AtendimentoVeterinarioAdmin(admin.ModelAdmin):
    model = AtendimentoVeterinario
    form = AtendimentoVeterinarioForm
    fieldsets=(
        (None, {'fields': ('cliente','animal','valor','buscar','horarioBuscar','entregar','horarioEntregar','data')}),
    )
    list_display=['cliente','animal','valor','deve_buscar','buscar_as','deve_entregar','entregar_as','data']
    list_filter=['buscar','entregar','data']
    inlines=[ItemAtedimentoVeterinarioInline]
    class Media:
        js = ["/media/js/atendimento.js","/media/js/servicos.js",]

admin.site.register(AtendimentoVeterinario,AtendimentoVeterinarioAdmin)
admin.site.register(ServicoVeterinario)
