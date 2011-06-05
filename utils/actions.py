#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.http import HttpResponse
from django.shortcuts import render_to_response

import csv
import codecs
import os

def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, header=True):
    """
    This function returns an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row
    """
    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/
        """
        opts = modeladmin.model._meta
        field_names = set([field.name for field in opts.fields])
        if fields:
            fieldset = set(fields)
            field_names = field_names & fieldset
        elif exclude:
            excludeset = set(exclude)
            field_names = field_names - excludeset

        response = HttpResponse(mimetype='text/csv')
        response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

        writer = csv.writer(response)
        if header:
            writer.writerow(field_names)
        for obj in queryset:
            writer.writerow([unicode(getattr(obj, field)) for field in field_names])
        return response
    export_as_csv.short_description = description
    return export_as_csv

def mail_export(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

    writer = csv.writer(response)
    writer.writerow([u"'%(name)s' <%(mail)s>" % {"name": obj.nome, "mail": obj.email} for obj in queryset])
    return response
mail_export.short_description = "Exportar emails selecionados em arquivo CSV"

def mail_export_to_newsletter(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % unicode(opts).replace('.', '_')

    writer = csv.writer(response)
    writer.writerow([u"'%(mail)s" % {"mail": obj.email} for obj in queryset])
    return response
mail_export.short_description = "Exportar emails em arquivo CSV"
mail_export_to_newsletter.short_description = "Exportar e-mails selecionados em arquivo CSV"
