#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from models import *
from forms import AtendimentoAbstractForm, ItemAtedimentoVeterinarioForm, ItemAtendimentoBanhoTosaForm
from produtos.models import Venda,ItemVenda
from veterinario.models import AtendimentoVeterinario, ItemAtedimentoVeterinario
from banhotosa.models import AtendimentoBanhoTosa,ItemAtendimentoBanhoTosa

class ItemVendaInline(admin.StackedInline):
    model = ItemVenda
    extra=1
    exclude=["venda",]
class ItemAtedimentoVeterinarioInline(admin.StackedInline):
    model = ItemAtedimentoVeterinario
    extra=1
    form = ItemAtedimentoVeterinarioForm
    exclude=["veterinario",]
class ItemAtendimentoBanhoTosaInline(admin.StackedInline):
    model = ItemAtendimentoBanhoTosa
    extra=1
    form = ItemAtendimentoBanhoTosaForm
    exclude=["banhoTosa",]

#class VendaInline(admin.StackedInline):
#    model = Venda
#    exclude=['cliente','animal','data']
#    max_num = 1
#    extra=1
#    fieldsets=(
#        (None, {'fields': ( 'valor','periodicidade','entregar')}),
#    )
#class AtendimentoVeterinarioInline(admin.StackedInline):
#    model = AtendimentoVeterinario
#    exclude=['cliente','animal','data']
#    max_num = 1
#    extra=1
#    filter_horizontal = ['servicos']
#    fieldsets=(
#        (None, {'fields': ('servicos', 'valor','buscar','horario','entregar',)}),
#    )
#class AtendimentoBanhoTosaInline(admin.StackedInline):
#    model = AtendimentoBanhoTosa
#    exclude=['cliente','animal','data']
#    max_num = 1
#    extra=1
#    filter_horizontal = ['servicos']
#    fieldsets=(
#        (None, {'fields': ('servicos', 'valor','buscar','horario','entregar',)}),
#    )
class AtendimentoAdmin(admin.ModelAdmin):
    model = Atendimento
    form = AtendimentoAbstractForm
    inlines = [ItemVendaInline,ItemAtedimentoVeterinarioInline,ItemAtendimentoBanhoTosaInline]
    fieldsets=(
        (None, {'fields': ('cliente','valor','buscar','horarioBuscar','entregar','horarioEntregar','data')}),
    )
    list_display=['cliente','animal','valor','buscar','horarioBuscar','entregar','horarioEntregar','data']
    list_filter=['buscar','entregar','data']
    class Media:
        js = ["/media/js/atendimento.js",]
        css = {"screen, projection": ["/media/css/atendimento.css"],}

admin.site.register(Atendimento,AtendimentoAdmin)
