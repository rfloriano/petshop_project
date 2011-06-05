#!/usr/bin/env python
#-*- coding:utf-8 -*-

from threading import Thread

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image
import os
from cStringIO import StringIO

def resizeImage(size, path, pathToSave=None):
    path = os.path.join(settings.MEDIA_ROOT, path)

    if pathToSave is None:
        saveAt = path
        media = path
    else:
        name = path.split("/")[-1]
        saveAt = os.path.join(settings.MEDIA_ROOT, pathToSave, name)
        media = os.path.join(pathToSave, name)

    image = Image.open(path)
    image.thumbnail(size, Image.ANTIALIAS)

    if image.format.lower() == "gif":
        image.save(saveAt, image.format)
    else:
        try:
            image.save(saveAt, image.format, quality=75, optimize=1)
        except:
            image.save(saveAt, image.format, quality=75)

    return media

class ResizeIt(Thread):
    def __init__(self, size, path, pathToSave=None):
        Thread.__init__(self)
        self.size = size
        self.path = path
        self.pathToSave = pathToSave
        self.start()

    def run(self):
        size = self.size
        path = os.path.join(self.path) #self.image.field.upload_to
        return resizeImage(self.size, self.path, self.pathToSave)

def generate_thumbnail(size, field_from, field_to):
    # Open original photo which we want to thumbnail using PIL's Image
    # object
    #path = os.path.join(settings.MEDIA_ROOT, field_from.field.upload_to, field_from.name)
    image = Image.open(field_from.name)

    # Convert to RGB if necessary
    # Thanks to Limodou on DjangoSnippets.org
    # http://www.djangosnippets.org/snippets/20/
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')

    # We use our PIL Image object to create the thumbnail, which already
    # has a thumbnail() convenience method that contrains proportions.
    # Additionally, we use Image.ANTIALIAS to make the image look better.
    # Without antialiasing the image pattern artifacts may result.
    image.thumbnail(size, Image.ANTIALIAS)

    # Save the thumbnail
    temp_handle = StringIO()
    print "handle =====", temp_handle
    image.save(temp_handle, image.format)
    temp_handle.seek(0)

    # Save to the thumbnail field

    suf = SimpleUploadedFile(os.path.split(field_from.name)[-1],
            temp_handle.read())
    return field_to.save(suf.name+"."+format, suf, save=False)
    #return (suf, image.format)
