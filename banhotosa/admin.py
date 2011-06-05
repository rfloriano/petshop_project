#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from models import *
from forms import AtendimentoBanhoTosaForm

class ItemAtendimentoBanhoTosaInline(admin.TabularInline):
    model = ItemAtendimentoBanhoTosa
    extra=1
    exclude=["atendimento","animal"]

class AtendimentoBanhoTosaAdmin(admin.ModelAdmin):
    model = AtendimentoBanhoTosa
    form = AtendimentoBanhoTosaForm
    fieldsets=(
        (None, {'fields': ('cliente','animal','valor','buscar','horarioBuscar','entregar','horarioEntregar','data')}),
    )
    list_display=['cliente','animal','valor','deve_buscar','buscar_as','deve_entregar','entregar_as','data']
    list_filter=['buscar','entregar','data']
    inlines=[ItemAtendimentoBanhoTosaInline,]
    class Media:
        js = ["/media/js/atendimento.js","/media/js/servicos.js",]

admin.site.register(AtendimentoBanhoTosa,AtendimentoBanhoTosaAdmin)
admin.site.register(ServicoBanhoTosa)
