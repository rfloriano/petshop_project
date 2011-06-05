#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from models import *
from forms import VendaForm

class ItemVendaInline(admin.TabularInline):
    model = ItemVenda
    extra=1
    exclude=["atendimento","animal"]

class ProdutoAdmin(admin.ModelAdmin):
    model = Produto

class VendaAdmin(admin.ModelAdmin):
    model = Venda
    form = VendaForm
    fieldsets=(
        (None, {'fields': ('cliente','animal','valor','entregar','horarioEntregar','data')}),
    )
    list_display=['cliente','animal','valor','deve_entregar','entregar_as','data']
    list_filter=['entregar','data']
    inlines=[ItemVendaInline,]
    class Media:
        js = ["/media/js/atendimento.js",]

admin.site.register(Venda,VendaAdmin)
admin.site.register(Produto,ProdutoAdmin)
