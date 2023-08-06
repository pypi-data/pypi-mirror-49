# -*- coding: utf-8 -*-
#
# This file is part of django-ca (https://github.com/mathiasertl/django-ca).
#
# django-ca is free software: you can redistribute it and/or modify it under the terms of the GNU
# General Public License as published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# django-ca is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without
# even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with django-ca.  If not,
# see <http://www.gnu.org/licenses/>.

import json

from django.forms import widgets
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _

from . import ca_settings
from .utils import LazyEncoder


class LabeledCheckboxInput(widgets.CheckboxInput):
    """CheckboxInput widget that adds a label and wraps everything in a <span />.

    This is necessary because widgets in MultiValueFields don't render with a label."""

    template_name = 'django_ca/forms/widgets/labeledcheckboxinput.html'

    def __init__(self, label, *args, **kwargs):
        self.label = label
        super(LabeledCheckboxInput, self).__init__(*args, **kwargs)

    def get_context(self, *args, **kwargs):
        ctx = super(LabeledCheckboxInput, self).get_context(*args, **kwargs)
        ctx['widget']['label'] = self.label
        return ctx

    def render(self, name, value, attrs=None, renderer=None):  # pragma: no cover - <= Django 1.11
        html = super(LabeledCheckboxInput, self).render(name, value, attrs=attrs, renderer=renderer)
        label = '<label for="%s">%s</label>' % (attrs.get('id'), self.label)
        html = '<span class="critical-widget-wrapper">%s%s</span>' % (html, label)
        return html

    class Media:
        css = {
            'all': ('django_ca/admin/css/labeledcheckboxinput.css', ),
        }


class LabeledTextInput(widgets.TextInput):
    """CheckboxInput widget that adds a label and wraps everything in a <span />.

    This is necessary because widgets in MultiValueFields don't render with a label."""

    template_name = 'django_ca/forms/widgets/labeledtextinput.html'

    def __init__(self, label, *args, **kwargs):
        self.label = label
        super(LabeledTextInput, self).__init__(*args, **kwargs)

    def get_context(self, *args, **kwargs):
        ctx = super(LabeledTextInput, self).get_context(*args, **kwargs)
        ctx['widget']['label'] = self.label
        ctx['widget']['cssid'] = self.label.lower().replace(' ', '-')
        return ctx

    def render_wrapped(self, name, value, attrs, renderer):  # pragma: no cover - <= Django 1.11
        html = super(LabeledTextInput, self).render(name, value, attrs=attrs, renderer=renderer)
        required = ''
        if self.attrs.get('required', False):
            required = 'class="required" '

        html += '<label %sfor="%s">%s</label>' % (required, attrs.get('id'), self.label)

        return html

    def render(self, name, value, attrs=None, renderer=None):  # pragma: no cover - <= Django 1.11
        html = self.render_wrapped(name, value, attrs, renderer=renderer)
        cssid = self.label.lower().replace(' ', '-')
        html = '<span id="%s" class="labeled-text-multiwidget">%s</span>' % (cssid, html)
        return html

    class Media:
        css = {
            'all': ('django_ca/admin/css/labeledtextinput.css', ),
        }


class SubjectTextInput(LabeledTextInput):
    template_name = 'django_ca/forms/widgets/subjecttextinput.html'

    def render_wrapped(self, name, value, attrs, renderer):  # pragma: no cover - <= Django 1.11
        html = super(SubjectTextInput, self).render_wrapped(name, value, attrs, renderer=renderer)
        html += '<span class="from-csr">%s <span></span></span>' % _('from CSR:')
        return html


class ProfileWidget(widgets.Select):
    def render(self, name, value, attrs=None, renderer=None):  # pragma: no cover - <= Django 1.11
        html = super(ProfileWidget, self).render(name, value, attrs=attrs, renderer=renderer)
        html += '''<script type="text/javascript">
            var ca_profiles = %s;
        </script>''' % json.dumps(ca_settings.CA_PROFILES, cls=LazyEncoder)
        html += '<p class="help profile-desc">%s</p>' % force_text(
            ca_settings.CA_PROFILES[ca_settings.CA_DEFAULT_PROFILE]['desc'])
        return html

    class Media:
        js = (
            'django_ca/admin/js/profilewidget.js',
        )


class CustomMultiWidget(widgets.MultiWidget):
    """Wraps the multi widget into a <p> element."""

    template_name = 'django_ca/forms/widgets/custommultiwidget.html'

    def format_output(self, rendered_widgets):  # pragma: no cover - <= Django 1.11
        # NOTE: We use a <p> because djangos stock forms.css takes care of indent this way.
        rendered_widgets.insert(0, '<p class="multi-widget">')
        rendered_widgets.append('</p>')
        return ''.join(rendered_widgets)


class SubjectWidget(CustomMultiWidget):
    def __init__(self, attrs=None):
        _widgets = (
            SubjectTextInput(label=_('Country'), attrs={'placeholder': '2 character country code'}),
            SubjectTextInput(label=_('State')),
            SubjectTextInput(label=_('Location')),
            SubjectTextInput(label=_('Organization')),
            SubjectTextInput(label=_('Organizational Unit')),
            SubjectTextInput(label=_('CommonName'), attrs={'required': True}),
            SubjectTextInput(label=_('E-Mail')),
        )
        super(SubjectWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value is None:  # pragma: no cover
            return ('', '', '', '', '', '')

        # Multiple OUs are not supported in webinterface
        ou = value.get('OU', '')
        if isinstance(ou, list) and ou:
            ou = ou[0]

        # Used e.g. for initial form data (e.g. resigning a cert)
        return [
            value.get('C', ''),
            value.get('ST', ''),
            value.get('L', ''),
            value.get('O', ''),
            ou,
            value.get('CN', ''),
            value.get('emailAddress', ''),
        ]


class SubjectAltNameWidget(CustomMultiWidget):
    def __init__(self, attrs=None):
        _widgets = (
            widgets.TextInput(),
            LabeledCheckboxInput(label="Include CommonName")
        )
        super(SubjectAltNameWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):  # pragma: no cover
        if value:
            return value
        return ('', True)


class MultiValueExtensionWidget(CustomMultiWidget):
    def __init__(self, choices, attrs=None):
        _widgets = (
            widgets.SelectMultiple(choices=choices, attrs=attrs),
            LabeledCheckboxInput(label=_('critical')),
        )
        super(MultiValueExtensionWidget, self).__init__(_widgets, attrs)

    def decompress(self, value):
        if value:
            return value.value, value.critical
        return ([], False)
