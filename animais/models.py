#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.db import models
from utils.br import models as br_models
from pessoas.models import Cliente, Fornecedor

class Especie(models.Model):
    nome=models.CharField("Nome", max_length=255, help_text=u"Nome da espécia.")

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = u"Espécie"
        verbose_name_plural = u"Espécies"

class Raca(models.Model):
    nome=models.CharField("Nome", max_length=255, help_text=u"Nome da raça.")
    descricao=models.TextField(u"Descrição", max_length=255, help_text=u"Descrição livre.", null=True, blank=True)
    foto=models.ImageField("Foto", upload_to='upload/images/racas/', help_text=u"Imagem que representa esta raça", null=True, blank=True)
    especie=models.ForeignKey(Especie)

    class Meta:
        verbose_name = u"Raça"
        verbose_name_plural = u"Raças"

    def __unicode__(self):
        return self.nome

class Animal(models.Model):
    nome=models.CharField("Nome", max_length=255, help_text=u"Nome do animal.")
    raca=models.ForeignKey(Raca)
    cliente=models.ForeignKey(Cliente)
    fornecedor=models.ForeignKey(Fornecedor, blank=True, null=True)

    def __unicode__(self):
        return unicode(self.nome) + " | " + unicode(self.cliente)

class FotoAbstrata(models.Model):
    nome=models.CharField(max_length=50, help_text=u"Este texto\
             deve descrever brevemente a imagem, pois será\
             utilizado como texto alternativo caso a\
             imagem não possa ser carregada")
    ordem = models.IntegerField("Ordem",help_text=u"Ordene como se fosse uma fila. Números menores são os primeiros a serem mostrados.", blank=True, null=True)
    class Meta:
        abstract=True
        ordering=["-ordem"]

    def __unicode__(self):
        return self.nome

class FotoAnimal(FotoAbstrata):
    foto=models.ImageField("Foto", upload_to='upload/images/animais/fotos/', help_text="Imagem do animal")
    animal = models.ForeignKey(Animal)
    
    class Meta:
        verbose_name=u"Foto do animal"
        verbose_name_plural=u"Fotos do animal"
