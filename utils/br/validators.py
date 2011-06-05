# Python imports
import re

# Django imports
from django.core.validators import RegexValidator, BaseValidator
from django.core.validators import EMPTY_VALUES
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from django.forms import ValidationError

#class BRPhoneNumberValidator(RegexValidator):
    #PHONE_DIGITS_RE = re.compile(r'^(\d{2})[-\.]?(\d{4})[-\.]?(\d{4})$')
    #PHONE_DDI_DIGITS_RE = re.compile(r'^[+\.](\d{2})?(\d{2})[-\.]?(\d{4})[-\.]?(\d{4})$')

    #message = _('Phone numbers must be in (XX)XXXX-XXXX format.')
    #message_ddi = _('Phone numbers must be in +XX(XX)XXXX-XXXX format.')
    #code = 'invalid'
    #code_ddi = 'invalid_ddi'

    #def __init__(self, ddi=None):
        #if ddi is not None:
            #self.ddi = ddi

        #if self.ddi:
            #print "--------ddi"
            #return super(BRPhoneNumberValidator, self).__init__(
                #self.PHONE_DDI_DIGITS_RE, self.message_ddi, self.code_ddi)
        #else:
            #print "--------no ddi"
            #return super(BRPhoneNumberValidator, self).__init__(
                #self.PHONE_DIGITS_RE, self.message, self.code)

    #def __call__(self, value):
        #cleaned = self.clean(value)
        #super(BRPhoneNumberValidator, self).__call__(value)
        ##params = {'limit_value': self.limit_value, 'show_value': cleaned}
        ##if self.compare(cleaned, self.limit_value):
            ##raise ValidationError(
                ##self.message % params,
                ##code=self.code,
                ##params=params,
            ##)

    #def clean(self, value):
        #print "cleaneed ----"
        #value = re.sub('(\(|\)|\s+)', '', smart_unicode(value))

        #if self.ddi:
            #data = self.PHONE_DDI_DIGITS_RE.search(value)
            #return '+%s(%s)%s-%s' % (data.group(1), data.group(2), data.group(3), data.group(4))
        #else:
            #data = self.PHONE_DIGITS_RE.search(value)
            #return '(%s)%s-%s' % (data.group(1), data.group(2), data.group(3))


class BRPhoneNumberValidator(BaseValidator):
    #regex = re.compile(
        #r'^(\d{2})[-\.]?(\d{4})[-\.]?(\d{4})$' # (99)9999-9999
        #r'^[+\.](\d{2})?(\d{2})[-\.]?(\d{4})[-\.]?(\d{4})$', # +99(99)9999-9999
        #re.IGNORECASE)

    PHONE_DIGITS_RE = re.compile(r'^(\d{2})[-\.]?(\d{4})[-\.]?(\d{4})$')
    PHONE_DDI_DIGITS_RE = re.compile(r'^[+\.](\d{2})?(\d{2})[-\.]?(\d{4})[-\.]?(\d{4})$')

    message = _('Phone numbers must be in (XX)XXXX-XXXX format.')
    #message_ddi = _('Phone numbers must be in +XX(XX)XXXX-XXXX format.')
    code = 'invalid'
    #code_ddi = 'invalid_ddi'

    def clean(self, value):
        value = re.sub('(\(|\)|_|-|\s+)', '', smart_unicode(value))

        if value in EMPTY_VALUES:
            return u''

        print "-----------", value

        if len(value) > 11:
            print "-------DDI----", value
            data = self.PHONE_DDI_DIGITS_RE.search(value)
            if data:
                '+%s(%s)%s-%s' % (data.group(1), data.group(2), data.group(3), data.group(4))
        else:
            print "-------NO DDI----"
            data = self.PHONE_DIGITS_RE.search(value)
            if data:
                '(%s)%s-%s' % (data.group(1), data.group(2), data.group(3))
        raise ValidationError(self.message, code=self.code)


    #def clean(self, value):
        #super(BRPhoneNumberField, self).clean(value)
        #if value in EMPTY_VALUES:
            #return u''
        #value = re.sub('(\(|\)|\s+)', '', smart_unicode(value))
        #format = None
        #if len(value) > 11:
            ## phone with DDI
            #m = phone_ddi_digits_re.search(value)
            #if m:
                #return '+%s(%s)%s-%s' % (m.group(1), m.group(2), m.group(3), m.group(4))
            #raise ValidationError(self.error_messages['invalid_ddi'])
        #else:
            #m = phone_digits_re.search(value)
            #if m:
                #return '(%s)%s-%s' % (m.group(1), m.group(2), m.group(3))
            #raise ValidationError(self.error_messages['invalid'])
