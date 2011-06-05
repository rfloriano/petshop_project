#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.db import models
from pessoas.models import Fornecedor
from atendimento.models import AtendimentoAbstrato,Atendimento
from animais.models import Animal

class Produto(models.Model):
    nome=models.CharField("Nome", max_length=255, help_text="Nome completo do produto.")
    descricao=models.TextField(u"Descrição", max_length=255, help_text=u"Descrição livre.", null=True, blank=True)
    preco=models.DecimalField(u"Preço",max_digits=20, decimal_places=2, blank=True, null=True)
    fornecedor=models.ForeignKey(Fornecedor)

    class Meta:
        verbose_name=u"Produto"
        verbose_name_plural=u"Produtos"

    def __unicode__(self):
        return unicode(self.nome)+" | R$="+unicode(self.preco)

class Venda(AtendimentoAbstrato):
    periodicidade = models.IntegerField("Periodicidade", help_text="Digite a periodicidade dessa venda. Em dias. Ex: 15 ou 30", blank=True, null=True)
    atendimento = models.ForeignKey(Atendimento, blank=True, null=True)

    class Meta:
        verbose_name=u"Venda"
        verbose_name_plural=u"Vendas"

    def valor_total(self):
        produtos = self.produtos
        total = 0
        for produto in produtos:
            total += produto.valor
        return total
    
    def save(self):
        if self.atendimento:
            self.cliente = self.atendimento.cliente
            self.data = self.atendimento.data
            self.animal = self.atendimento.animal
        super(Venda, self).save()

class ItemVenda(models.Model):
    animal = models.ForeignKey(Animal, blank=True, null=True)
    qntd=models.IntegerField(u"Quantidade",default="1")
    produto = models.ForeignKey(Produto)
    atendimento=models.ForeignKey(Atendimento, blank=True, null=True)
    venda=models.ForeignKey(Venda, blank=True, null=True)

    class Meta:
        verbose_name=u"Item Venda"
        verbose_name_plural=u"Itens Venda"

    def __unicode__(self):
        return unicode(self.qntd)+" x "+unicode(self.produto.nome)

    def save(self):
        if self.venda:
            if self.venda.animal:
                self.animal = self.venda.animal
        super(ItemVenda, self).save()
