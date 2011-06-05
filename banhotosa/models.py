#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.db import models
from atendimento.models import AtendimentoAbstrato,Atendimento
from animais.models import Animal

class ServicoBanhoTosa(models.Model):
    nome=models.CharField("Nome", max_length=255, help_text="Nome completo do serviço. Ex: Banho, Banho e Tosa, Banho e Tosa Higiênica")
    descricao=models.TextField(u"Descrição", max_length=255, help_text=u"Descrição livre.", null=True, blank=True)
    preco=models.DecimalField(u"Preço",max_digits=20, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name=u"Serviço Banho e Tosa"
        verbose_name_plural=u"Serviços Banho e Tosa"

    def __unicode__(self):
        return unicode(self.nome)+" | R$="+unicode(self.preco)

class AtendimentoBanhoTosa(AtendimentoAbstrato):
    atendimento = models.ForeignKey(Atendimento, blank=True, null=True)

    class Meta:
        verbose_name=u"Atendimento Banho e Tosa"
        verbose_name_plural=u"Atendimentos Banho e Tosa"

    def valor_total(self):
        servicos = self.servicos
        total = 0
        for servico in servicos:
            total += servico.valor
        return total
    
    def __unicode__(self):
        return unicode(self.cliente)+" | "+unicode(self.data)
    
    def save(self):
        if self.atendimento:
            self.cliente = self.atendimento.cliente
            self.data = self.atendimento.data
            self.animal = self.atendimento.animal
        super(AtendimentoBanhoTosa, self).save()

class ItemAtendimentoBanhoTosa(models.Model):
    animal = models.ForeignKey(Animal, blank=True, null=True)
    qntd=models.IntegerField(u"Quantidade",default="1")
    servico = models.ForeignKey(ServicoBanhoTosa)
    atendimento=models.ForeignKey(Atendimento, blank=True, null=True)
    banhoTosa=models.ForeignKey(AtendimentoBanhoTosa, blank=True, null=True)

    class Meta:
        verbose_name=u"Item Atendimento Banho e Tosa"
        verbose_name_plural=u"Itens Atendimento Banho e Tosa"

    def __unicode__(self):
        return unicode(self.qntd)+" x "+unicode(self.servico.nome)

    def save(self):
        if self.banhoTosa:
            self.animal = self.banhoTosa.animal
        super(ItemAtendimentoBanhoTosa, self).save()
