#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.contrib import admin
from models import *

class EspecieAdmin(admin.ModelAdmin):
    model = Especie
    
class RacaAdmin(admin.ModelAdmin):
    model = Raca

class FotoAnimalInline(admin.TabularInline):
    model = FotoAnimal
    extra = 1

class AnimalAdmin(admin.ModelAdmin):
    model = Animal
    inlines = [FotoAnimalInline]

admin.site.register(Animal,AnimalAdmin)
admin.site.register(Raca,RacaAdmin)
admin.site.register(Especie,EspecieAdmin)
