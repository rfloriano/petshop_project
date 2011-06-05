from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.db.models.fields import Field, CharField
from django.contrib.localflavor.br.br_states import STATE_CHOICES
from django.core import validators
from django.utils.encoding import smart_unicode

class BaseField(Field):
    def get_internal_type(self):
        return "TextField"

    def to_python(self, value):
        if isinstance(value, basestring) or value is None:
            return value
        return smart_unicode(value)

    def get_prep_value(self, value):
        return self.to_python(value)

class StateField(CharField):
    description = _("Brazilians states (two uppercase letters)")

    def __init__(self, *args, **kwargs):
        kwargs['choices'] = STATE_CHOICES
        kwargs['max_length'] = 2
        super(StateField, self).__init__(*args, **kwargs)

class StateChoiceField(Field):
    description = _("Brazilians states (two uppercase letters)")

    def formfield(self, **kwargs):
        from forms import StateChoiceField as StateField
        defaults = {'form_class': StateField}
        defaults.update(kwargs)
        return super(StateChoiceField, self).formfield(**defaults)

class PhoneNumberField(BaseField):
    description = _("Phone number")

    def __init__(self, verbose_name=None, mask='(99)9999-9999', max_length=13, *args, **kwargs):
        kwargs['verbose_name']=verbose_name
        super(PhoneNumberField, self).__init__(*args, **kwargs)
        kwargs['max_length'] = max_length
        self.mask = mask

    def formfield(self, **kwargs):
        from forms import BRPhoneNumberField
        defaults = {'form_class': BRPhoneNumberField, 'max_length': self.max_length, 'mask': self.mask}
        defaults.update(kwargs)
        return super(PhoneNumberField, self).formfield(**defaults)

class ZipCodeField(BaseField):
    description = _("Zip Code")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 9
        super(ZipCodeField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        from forms import ZipCodeField as ZCField
        defaults = {'form_class': ZCField}
        defaults.update(kwargs)
        return super(ZipCodeField, self).formfield(**defaults)

class CpfField(BaseField):
    description = _("CPF")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 14
        super(CpfField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        from forms import BRCPFField
        defaults = {'form_class': BRCPFField}
        defaults.update(kwargs)
        return super(CpfField, self).formfield(**defaults)

class CnpjField(BaseField):
    description = _("CNPJ")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 18
        super(CnpjField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        from forms import BRCNPJField
        defaults = {'form_class': BRCNPJField}
        defaults.update(kwargs)
        return super(CnpjField, self).formfield(**defaults)

class CnpjCpfField(CharField):
    description = _("CNPJ/CPF")

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 18
        super(CnpjCpfField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        from forms import BRCnpjCpfField
        defaults = {'form_class': BRCnpjCpfField}
        defaults.update(kwargs)
        return super(CnpjCpfField, self).formfield(**defaults)
