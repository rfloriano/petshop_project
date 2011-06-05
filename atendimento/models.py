#!/usr/bin/env python
#-*- coding:utf-8 -*-
from datetime import date
from django.db import models
from pessoas.models import Cliente
from animais.models import Animal

class AtendimentoAbstrato(models.Model):
    cliente = models.ForeignKey(Cliente, blank=True, null=True)
    animal = models.ForeignKey(Animal, blank=True, null=True)
    data = models.DateField("Data", help_text=u"Data do atendimento.", default=date.today())
    valor=models.DecimalField(u"Valor cobrado",max_digits=20, decimal_places=2, blank=True, null=True)
    buscar = models.BooleanField("Buscar")
    horarioBuscar = models.DateTimeField(u"Buscar", help_text="Buscar no dia e hora definidos acima.", blank=True, null=True)
    entregar=models.BooleanField("Entregar", blank=True)
    horarioEntregar = models.DateTimeField(u"Entregar", help_text="Entregar no dia e hora definidos acima.", blank=True, null=True)

    class Meta:
        abstract=True

    def __unicode__(self):
        return unicode(self.id)+" | "+unicode(self.cliente)

    def deve_buscar(self):
        if self.buscar: 
            return """ <img alt="True" src="/media/img/admin/icon-yes.gif"/> """ 
        else: 
            return """ <img alt="False" src="/media/img/admin/icon-no.gif"/> """       
    deve_buscar.allow_tags = True 

    def buscar_as(self):
        if self.buscar: 
            return """ <img alt="True" src="/media/img/admin/icon-yes.gif"/> """ 
        else: 
            return """ <img alt="False" src="/media/img/admin/icon-no.gif"/> """       
    buscar_as.allow_tags = True 

    def deve_entregar(self):
        if self.entregar: 
            return """ <img alt="True" src="/media/img/admin/icon-yes.gif"/> """ 
        else: 
            return """ <img alt="False" src="/media/img/admin/icon-no.gif"/> """       
    deve_entregar.allow_tags = True

    def entregar_as(self):
        if self.buscar: 
            return """ <img alt="True" src="/media/img/admin/icon-yes.gif"/> """ 
        else: 
            return """ <img alt="False" src="/media/img/admin/icon-no.gif"/> """       
    entregar_as.allow_tags = True 

class Atendimento(AtendimentoAbstrato):
    class Meta:
        verbose_name=u"Atendimento Completo"
        verbose_name_plural=u"Atendimentos Completos"
