from django.conf import settings
from django.dispatch import receiver
from django.templatetags.static import static
from django.utils.translation import ugettext as _

from modoboa.admin import signals as admin_signals
from modoboa.core import signals as core_signals

from .forms import DomainSettingsForm, MUADomainWizardStep
from .models import DomainSettings


@receiver(admin_signals.extra_domain_forms)
def extra_domain_form(sender, user, domain, **kwargs):
    """Return MUA settings for the domain edition."""
    if not domain or domain.type != 'domain':
        return []
    return [
        {
            'id': 'mua',
            'title': _("MUA"),
            'cls': DomainSettingsForm,
            'formtpl': 'automua/domain_settings_form.html',
        }
    ]


@receiver(admin_signals.get_domain_form_instances)
def fill_domain_instances(sender, user, domain, **kwargs):
    """Pass the current instance to the form."""
    if domain.type != 'domain':
        return {}
    return {
        'mua': getattr(
            domain,
            'mua_settings',
            DomainSettings.objects.for_domain(domain),
        ),
    }


@receiver(admin_signals.extra_domain_wizard_steps)
def extra_wizard_step(sender, **kwargs):
    """Return a step to configure the servers."""
    return [
        MUADomainWizardStep(
            'mua',
            DomainSettingsForm,
            _("MUA"),
            'automua/domain_settings_form.html',
        )
    ]


@receiver(admin_signals.extra_domain_dashboard_widgets)
def display_domain_servers(sender, user, domain, **kwargs):
    """Display server names for the domain."""
    if domain.type != 'domain' or not hasattr(domain, 'mua_settings'):
        return []
    return [
        {
            'column': 'right',
            'template': 'automua/domain_mua_widget.html',
            'context': {
                'use_default': domain.mua_settings.use_default,
                'server_name': (
                    domain.mua_settings.server_name
                    if not domain.mua_settings.use_default
                    else getattr(settings, 'AUTOMUA_DEFAULT_SERVER_NAME', '–')
                ),
            },
        }
    ]


@receiver(core_signals.extra_static_content)
def get_static_content(sender, caller, st_type, user, **kwargs):
    if caller != 'domains' or st_type != 'js':
        return ''
    return '<script src="{}" type="text/javascript"></script>'.format(
        static('automua/js/domains.js')
    )


@receiver(core_signals.extra_uprefs_routes)
def add_extra_routes(sender, **kwargs):
    if not getattr(settings, 'AUTOMUA_SERVE_FRONTEND_ROUTES', True):
        return []

    from .frontend.urls import urlpatterns

    return urlpatterns
