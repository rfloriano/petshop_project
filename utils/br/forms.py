"""
BR-specific Form helpers
"""

from django.core.validators import EMPTY_VALUES
from django import forms
from django.forms import ValidationError
from django.forms.fields import Field, RegexField, Select, CharField, Select
from django.utils.encoding import smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.contrib.localflavor.br.br_states import STATE_CHOICES
import re

from widgets import ZipCodeWidget, PhoneWidget, CPFWidget, CNPJWidget

phone_digits_re = re.compile(r'^(\d{2})[-\.]?(\d{4})[-\.]?(\d{4})$')
phone_ddi_digits_re = re.compile(r'^[+\.](\d{2})?(\d{2})[-\.]?(\d{4})[-\.]?(\d{4})$')
zipcode_digits_re = re.compile(r'^(\d{5})[-\.]?(\d{3})$')
cpf_digits = re.compile(r'^(\d{3})[.\.]?(\d{3})[.\.]?(\d{3})[-\.]?(\d{2})$')
cnpj_digits = re.compile(r'^(\d{2})[.\.]?(\d{3})[.\.]?(\d{3})[/.]?(\d{4})[-\.]?(\d{2})$')

class ZipCodeField(Field):
    widget = ZipCodeWidget
    default_error_messages = {
        'invalid': _('Enter a zip code in the format XXXXX-XXX.'),
    }

    def __init__(self, max_length=9, *args, **kwargs):
        self.max_length = max_length
        super(ZipCodeField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(ZipCodeField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        value = re.sub('(\(|\)|\s+)', '', smart_unicode(value))
        m = zipcode_digits_re.search(value)
        if m:
            return u'%s-%s' % (m.group(1), m.group(2))
        raise ValidationError(self.error_messages['invalid'])

    def widget_attrs(self, widget):
        return {'maxlength': str(self.max_length)}

class BRPhoneNumberField(Field):
    widget = PhoneWidget
    default_error_messages = {
        'invalid': _('Phone numbers must be in (XX)XXXX-XXXX format.'),
        'invalid_ddi': _('Phone numbers must be in +XX(XX)XXXX-XXXX format.'),
    }

    def __init__(self, max_length=13, mask='(99)9999-9999', *args, **kwargs):
        self.max_length = max_length
        self.mask = mask
        super(BRPhoneNumberField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(BRPhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        value = re.sub('(\(|\)|\s+)', '', smart_unicode(value))
        format = None
        if len(value) > 11:
            # phone with DDI
            m = phone_ddi_digits_re.search(value)
            if m:
                return '+%s(%s)%s-%s' % (m.group(1), m.group(2), m.group(3), m.group(4))
            raise ValidationError(self.error_messages['invalid_ddi'])
        else:
            m = phone_digits_re.search(value)
            if m:
                return '(%s)%s-%s' % (m.group(1), m.group(2), m.group(3))
            raise ValidationError(self.error_messages['invalid'])

    def widget_attrs(self, widget):
        return {'maxlength': str(self.max_length), 'rel': self.mask}

class StateSelect(Select):
    """
    A Select widget that uses a list of Brazilian states/territories
    as its choices.
    """
    def __init__(self, attrs=None):
        super(BRStateSelect, self).__init__(attrs, choices=STATE_CHOICES)

class StateChoiceField(Field):
    """
    A choice field that uses a list of Brazilian states as its choices.
    """
    widget = Select
    default_error_messages = {
        'invalid': _(u'Select a valid brazilian state. That state is not one of the available states.'),
    }

    def __init__(self, required=True, widget=None, label=None,
                 initial=None, help_text=None):
        super(StateChoiceField, self).__init__(required, widget, label,
                                                 initial, help_text)
        self.widget.choices = STATE_CHOICES

    def clean(self, value):
        value = super(StateChoiceField, self).clean(value)
        if value in EMPTY_VALUES:
            value = u''
        value = smart_unicode(value)
        if value == u'':
            return value
        valid_values = set([smart_unicode(k) for k, v in self.widget.choices])
        if value not in valid_values:
            raise ValidationError(self.error_messages['invalid'])
        return value

class BRCPFField(Field):
    widget = CPFWidget
    default_error_messages = {
        'invalid': _('CPF numbers must be in xxx.xxx.xxx-xx format.'),
        'max_digits': _("This field requires at most 11 digits or 14 characters."),
        'digits_only': _("This field requires only numbers."),
        'fake': _("This CPF does not exist."),
    }

    def __init__(self, max_length=14, *args, **kwargs):
        self.max_length = max_length
        super(BRCPFField, self).__init__(*args, **kwargs)

    def clean(self, value):
        super(BRCPFField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        value = self.is_valid(value)
        if value:
            return value
        raise ValidationError(self.error_messages['invalid'])

    def is_valid(self, value):
        return CPF(value, self.default_error_messages).is_valid()

    def widget_attrs(self, widget):
        return {'maxlength': str(self.max_length)}

class BRCNPJField(Field):
    widget = CNPJWidget
    default_error_messages = {
        'invalid': _("Invalid CNPJ number."),
        'digits_only': _("This field requires only numbers."),
        'max_digits': _("This field requires at least 14 digits"),
        'fake': _("This CNPJ does not exist."),
    }

    def __init__(self, max_length=18, *args, **kwargs):
        self.max_length = max_length
        super(BRCNPJField, self).__init__(*args, **kwargs)

    def widget_attrs(self, widget):
        return {'maxlength': str(self.max_length)}

    def clean(self, value):
        """
        Value can be either a string in the format XX.XXX.XXX/XXXX-XX or a
        group of 14 characters.
        """
        value = super(BRCNPJField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        value = self.is_valid(value)
        if value:
            return value
        raise ValidationError(self.error_messages['invalid'])

    def is_valid(self, value):
        return CNPJ(value, self.default_error_messages).is_valid()

class BRCnpjCpfField(CharField):
    default_error_messages = {
        'invalid': _("Invalid CNPJ or CPF. CPF or CNPJ numbers must be in XXX.XXX.XXX-XX or XX.XXX.XXX/XXXX-XX"),
        'digits_only': _("This field requires only numbers."),
        'max_digits': _("This field requires at least 11 digits"),
        'fake': _("This CNPJ/CPF does not exist."),
    }

    def clean(self, value):
        """
        Value can be either a string in the format XX.XXX.XXX/XXXX-XX or XXX.XXX.XXX-XX and
        group of least 11 digits.
        """
        value = super(BRCnpjCpfField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        value = self.is_valid(value)
        if value:
            return value[0]
        raise ValidationError(self.error_messages['invalid'])

    def is_valid(self, value):
        try:
            return CPF(value, self.default_error_messages).is_valid(), 'CPF'
        except:
            pass

        try:
            return CNPJ(value, self.default_error_messages).is_valid(), 'CNPJ'
        except:
            return None
        return None

class CPF(object):
    def __init__(self, value, default_error_messages):
        self.value = value
        self.error_messages = default_error_messages

    def is_valid(self):
        invalids = ['11111111111', '22222222222', '33333333333',
                    '44444444444', '55555555555', '66666666666',
                    '77777777777', '88888888888', '99999999999',
                    '00000000000']
        self.value = re.sub('(\.|-)', '', smart_unicode(self.value))
        # validating value
        if len(self.value) < 11:
            #return (False, 'max_digits')
            raise ValidationError(self.error_messages['max_digits'])
        if self.value in invalids:
            #return (False, 'fake')
            raise ValidationError(self.error_messages['fake'])
        # get only 9 first digits of value and generate 2 last
        try:
            integers = map(int, self.value)
        except ValueError:
            #return (False, 'digits_only')
            raise ValidationError(self.error_messages['digits_only'])
        new = integers[:9]

        while len(new) < 11:
            r = sum([(len(new)+1-i)*v for i,v in enumerate(new)]) % 11
            if r > 1:
                f = 11 - r
            else:
                f = 0
            new.append(f)

        # if generated number is different of original number, CPF is invalid
        if new != integers:
            #return (False, 'fake')
            raise ValidationError(self.error_messages['fake'])
        # end validation
        m = cpf_digits.search(self.value)
        if m:
            return u'%s.%s.%s-%s' % (m.group(1), m.group(2), m.group(3), m.group(4))
        raise ValidationError(self.error_messages['invalid'])

class CNPJ(object):
    def __init__(self, value, default_error_messages):
        self.value = value
        self.error_messages = default_error_messages

    def is_valid(self):
        self.value = re.sub('(\.|-|/)', '', smart_unicode(self.value))
        # validating value
        if len(self.value) < 14:
            raise ValidationError(self.error_messages['max_digits'])
        try:
            integers = map(int, self.value)
        except ValueError:
            raise ValidationError(self.error_messages['digits_only'])
        # get only 12 first digits of value and generate 2 last
        new = integers[:12]

        prod = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        while len(new) < 14:
            r = sum([x*y for (x, y) in zip(new, prod)]) % 11
            if r > 1:
                f = 11 - r
            else:
                f = 0
            new.append(f)
            prod.insert(0, 6)

        # if generated number is different of original number, CNPJ is invalid
        if new != integers:
            raise ValidationError(self.error_messages['fake'])
        # end validation
        m = cnpj_digits.search(self.value)
        if m:
            return u'%s.%s.%s/%s-%s' % (m.group(1), m.group(2), m.group(3), m.group(4), m.group(5))
        raise ValidationError(self.error_messages['invalid'])
