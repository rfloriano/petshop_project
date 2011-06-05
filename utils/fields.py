#!/usr/bin/env python
#-*- coding:utf-8 -*-

from django.db import models
from django import forms
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.template.defaultfilters import filesizeformat
from django.contrib.localflavor.br.br_states import STATE_CHOICES

import os
import re

from bombinhas_project.utils.widgets import AdminImageWidget

class ImagePathField(forms.CharField):
    def __init__(self, path, match=None, recursive=False, required=True,
                 widget=None, label=None, initial=None, help_text=None,
                 *args, **kwargs):
        self.path, self.match, self.recursive = path, match, recursive
        if kwargs.has_key("multiple"):
            self.multiple = kwargs["multiple"]
            kwargs.pop("multiple")
        super(ImagePathField, self).__init__(required=required,
            widget=widget, label=label, initial=initial, help_text=help_text,
            *args, **kwargs)

        self.choices = []

        if self.match is not None:
            self.match_re = re.compile(self.match)

        self.path_media = self.path
        self.path = os.path.join(settings.MEDIA_ROOT, self.path)

        if recursive:
            for root, dirs, files in os.walk(self.path):
                for f in files:
                    if self.match is None or self.match_re.search(f):
                        f = os.path.join(root, f)
                        self.choices.append((f, f.replace(path, "", 1)))
        else:
            try:
                for f in os.listdir(self.path):
                    full_file = os.path.join(self.path, f)
                    if os.path.isfile(full_file) and (self.match is None or self.match_re.search(f)):
                        path_file = os.path.join(self.path_media, f)
                        self.choices.append((path_file, f))
            except OSError:
                pass

        self.widget.multiple = self.multiple
        self.widget.choices = self.choices

class ImageChoiceField(models.Field):
    __metaclass__ = models.SubfieldBase
    description = _("ImageChoiceField object")

    def __init__(self, path="", extensions=[], multiple=False, verbose_name=None, name=None, recursive=False, **kwargs):
        self.path, self.recursive, self.multiple = path, recursive, multiple
        self.match = ""
        for ext in extensions:
            if self.match:
                self.match += "|"
            self.match += "(.*)\.%s" % ext
        models.Field.__init__(self,verbose_name=verbose_name, name=name, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'path': self.path,
            'match': self.match,
            'recursive': self.recursive,
            'form_class': ImagePathField,
            'multiple': self.multiple,
            'widget': AdminImageWidget,
        }
        defaults.update(kwargs)
        return super(ImageChoiceField, self).formfield(**defaults)

    def to_python(self, value):
        "Normalize data to a list of strings."

        # Return an empty list if no input was given.
        if not value:
            return []
        elif isinstance(value, basestring):
            return value.split(',')[:-1]
        return value

    def get_prep_value(self, value):
        if not value:
            return ""
        elif isinstance(value, basestring):
            return value
        value = ",".join(value)
        if value and not value.endswith(","):
            value += ","
        return value

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_prep_value(value)

    def clean(self, value, model_instance):
        value = super(self.__class__, self).clean(value, model_instance)
        return self.get_prep_value(value)

    def get_internal_type(self):
        return "TextField"

class ContentTypeRestrictedFileField(models.FileField):
    """
    Same as FileField, but you can specify:
        * content_types - list containing allowed content_types. Example: ['application/pdf', 'image/jpeg']
        * max_upload_size - a number indicating the maximum file size allowed for upload.
            2.5MB - 2621440
            5MB - 5242880
            10MB - 10485760
            20MB - 20971520
            50MB - 5242880
            100MB 104857600
            250MB - 214958080
            500MB - 429916160
    """
    def __init__(self, *args, **kwargs):
        self.content_types = kwargs.pop("content_types")
        self.max_upload_size = kwargs.pop("max_upload_size")

        super(ContentTypeRestrictedFileField, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        data = super(ContentTypeRestrictedFileField, self).clean(*args, **kwargs)

        file = data.file
        try:
            content_type = file.content_type
            if content_type in self.content_types:
                if file._size > self.max_upload_size:
                    raise forms.ValidationError('O tamanho do arquivo não deve ultrapassar %s, o arquivo enviado possui %s. Por favor, corrija este erro.' % (filesizeformat(self.max_upload_size), filesizeformat(file._size)))
            else:
                raise forms.ValidationError('Tipo de arquivo não suportado.')
        except AttributeError:
            pass

        return data
