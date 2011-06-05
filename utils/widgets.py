from django.forms.widgets import Widget
from django.utils.safestring import mark_safe
from django.forms.util import flatatt
from django.utils.encoding import force_unicode
from django.conf import settings

import os

class AdminImageWidget(Widget):
    """
    A ImageField Widget for admin that shows a thumbnail.
    """

    input_type = "hidden"

    class Media:
        js = [ os.path.join(settings.MEDIA_URL, 'js/image-choice.js'), ]
        css = {
            'all': [os.path.join(settings.MEDIA_URL, 'css/image-choice.css')]
        }

    def __init__(self, attrs={}):
        attrs.update({'class': 'custom-imagefield'})
        super(AdminImageWidget, self).__init__(attrs)

    def render(self, name, value, attrs=None):
        if value is None: value = ''
        valuestring = ",".join(value)
        if valuestring and not valuestring.endswith(","):
            valuestring += ","
        attrs = {"name":name, "value":valuestring, "id": "id_"+name}
        final_attrs = self.build_attrs(attrs, type=self.input_type, name=name)
        if valuestring:
            final_attrs["value"] = force_unicode(valuestring)
        html = u'<input%s />\n' % flatatt(final_attrs)
        attrs = {"id":"custom-widget-imagechoice","class": "custom-widget-imagechoice"}
        if self.multiple:
            attrs["class"] += " multiple"
        html += '<div%s>' % flatatt(attrs)
        for f in self.choices:
            val = f[0]
            attrs_temp = {"url": os.path.join(settings.MEDIA_URL, f[0]), "val": val, "name": name, "class": 'class="selected"' if val in value else ""}
            temp =  """<div name="%(val)s" class="option">
<img src="%(url)s" title="%(name)s" alt="%(name)s" %(class)s/>
</div>"""
            html += temp % attrs_temp
        html += '</div>'
        return mark_safe(html)

