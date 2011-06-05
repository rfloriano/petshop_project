#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.db import models
from utils.br import models as br_models

class Pessoa(models.Model):
    nome=models.CharField("Nome", max_length=255, help_text="Nome completo.")
    telefone = br_models.PhoneNumberField("Telefone", help_text=u"O telefone será apresentado acima do formulário de contato na página de contato.", null=True, blank=True)
    dataNascimento = models.DateField("Data nascimento", help_text=u"Data de nascimento da pessoa.", blank=True, null=True)
    email = models.EmailField("E-mail", help_text=u"E-mail para contato.", blank=True, null=True)
#    TODO add campos abaixo
    enderecoCobranca=models.CharField(u"Endereço Cobrança", max_length=255, help_text="Endereço completo.", blank=True, null=True)
    enderecoEntrega=models.CharField(u"Endereço Entrega", max_length=255, help_text="Endereço completo.", blank=True, null=True)

    class Meta:
        abstract=True

    def __unicode__(self):
        return self.nome

class Fornecedor(Pessoa):
    cpf = br_models.CpfField("CPF", null=True, blank=True)
    cnpj = br_models.CnpjField("CNPJ", null=True, blank=True)

    class Meta:
        verbose_name = u"Fornecedor"
        verbose_name_plural = u"Fornecedores"

    def pegar_animais(self):
        return Animal.objects.filter(cliente=self)

class Cliente(Pessoa):
    cpf = br_models.CpfField("CPF", null=True, blank=True)

    class Meta:
        verbose_name = u"Cliente"
        verbose_name_plural = u"Clientes"

    def pegar_animais(self):
        return Animal.objects.filter(cliente=self)

class Funcionario(Pessoa):
    cpf = br_models.CpfField("CPF", null=True, blank=True)

    class Meta:
        verbose_name = u"Funcionário"
        verbose_name_plural = u"Funcionários"
