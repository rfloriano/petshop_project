#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.db import models
from atendimento.models import AtendimentoAbstrato,Atendimento
from animais.models import Animal

class ServicoVeterinario(models.Model):
    nome=models.CharField("Nome", max_length=255, help_text="Nome completo do serviço. Ex: Hemograma, Raio-X")
    descricao=models.TextField(u"Descrição", max_length=255, help_text=u"Descrição livre.", null=True, blank=True)
    preco=models.DecimalField(u"Preço",max_digits=20, decimal_places=2, blank=True, null=True)

    class Meta:
        verbose_name=u"Serviço Veterinário"
        verbose_name_plural=u"Serviços Veterinário"

    def __unicode__(self):
        return unicode(self.nome)+" | R$="+unicode(self.preco)

class AtendimentoVeterinario(AtendimentoAbstrato):
    atendimento = models.ForeignKey(Atendimento, blank=True, null=True)

    class Meta:
        verbose_name=u"Atendimento Veterinário"
        verbose_name_plural=u"Atendimentos Veterinário"

    def valor_total(self):
        servicos = self.servicos
        total = 0
        for servico in servicos:
            total += servico.valor
        return total
    
    def save(self):
        if self.atendimento:
            self.cliente = self.atendimento.cliente
            self.data = self.atendimento.data
            self.animal = self.atendimento.animal
        super(AtendimentoVeterinario, self).save()

class ItemAtedimentoVeterinario(models.Model):
    animal = models.ForeignKey(Animal, blank=True, null=True)
    qntd=models.IntegerField(u"Quantidade",default="1")
    servico = models.ForeignKey(ServicoVeterinario)
    atendimento=models.ForeignKey(Atendimento, blank=True, null=True)
    veterinario=models.ForeignKey(AtendimentoVeterinario, blank=True, null=True)

    class Meta:
        verbose_name=u"Item Atedimento Veterinario"
        verbose_name_plural=u"Itens Atedimento Veterinario"

    def __unicode__(self):
        return unicode(self.qntd)+" x "+unicode(self.servico.nome)
    
    def save(self):
        if self.veterinario:
            self.animal = self.veterinario.animal
        super(ItemAtedimentoVeterinario, self).save()
