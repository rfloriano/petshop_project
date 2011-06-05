#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from models import *
from utils.admin import OneEntry

class ClienteAdmin(admin.ModelAdmin):
    model = Cliente

class FornecedorAdmin(admin.ModelAdmin):
    model = Fornecedor

class FuncionarioAdmin(admin.ModelAdmin):
    model = Funcionario

admin.site.register(Cliente,ClienteAdmin)
admin.site.register(Funcionario,FuncionarioAdmin)
admin.site.register(Fornecedor,FornecedorAdmin)
