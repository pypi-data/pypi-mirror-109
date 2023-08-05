from django import forms

from modoboa.lib.form_utils import WizardStep

from .models import DomainSettings


class MUADomainWizardStep(WizardStep):
    def check_access(self, wizard):
        return wizard.steps[0].form.cleaned_data['type'] == 'domain'


class DomainSettingsForm(forms.ModelForm):
    """Form to create or edit MUA related settings for a domain."""

    class Meta:
        model = DomainSettings
        fields = ('server_name', 'use_default')

    def save(self, *args, domain, **kwargs):
        self.instance.domain = domain
        return super().save()
