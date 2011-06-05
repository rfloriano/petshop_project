from django.forms.widgets import TextInput
from django.conf import settings

import os

class PhoneWidget(TextInput):
    """
    A PhoneWidget Widget for admin mask the field Eg.:(99)9999-9999
    """

    input_type = "text"

    class Media:
        js = [
            os.path.join(settings.MEDIA_URL, 'js/jquery.mask.min.js'),
            os.path.join(settings.MEDIA_URL, 'js/masks/phone-mask.js')
        ]

    def __init__(self, attrs={}):
        attrs.update({'class': 'vTextField vPhone'})
        super(PhoneWidget, self).__init__(attrs)

class ZipCodeWidget(TextInput):
    """
    A ZipCodeWidget Widget for admin mask the field Eg.:99999-999
    """

    input_type = "text"

    class Media:
        js = [os.path.join(settings.MEDIA_URL, 'js/jquery.mask.min.js'), os.path.join(settings.MEDIA_URL, 'js/masks/zipcode-mask.js')]

    def __init__(self, attrs={}):
        attrs.update({'class': 'vTextField vZipCode'})
        super(ZipCodeWidget, self).__init__(attrs)

class CPFWidget(TextInput):
    """
    A CPFWidget Widget for admin mask the field Eg.:999.999.999-99
    """

    input_type = "text"

    class Media:
        js = [os.path.join(settings.MEDIA_URL, 'js/jquery.mask.min.js'), os.path.join(settings.MEDIA_URL, 'js/masks/cpf-mask.js')]

    def __init__(self, attrs={}):
        attrs.update({'class': 'vTextField vCPF'})
        super(CPFWidget, self).__init__(attrs)

class CNPJWidget(TextInput):
    """
    A CNPJWidget Widget for admin mask the field Eg.:99.999.999/9999-99
    """

    input_type = "text"

    class Media:
        js = [os.path.join(settings.MEDIA_URL, 'js/jquery.mask.min.js'), os.path.join(settings.MEDIA_URL, 'js/masks/cnpj-mask.js')]

    def __init__(self, attrs={}):
        attrs.update({'class': 'vTextField vCNPJ'})
        super(CNPJWidget, self).__init__(attrs)
