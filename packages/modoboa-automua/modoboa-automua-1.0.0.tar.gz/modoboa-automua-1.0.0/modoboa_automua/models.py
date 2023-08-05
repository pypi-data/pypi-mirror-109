from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext as _
from django.utils.translation import ugettext_lazy


class DomainSettingsManager(models.Manager):
    def for_domain(self, domain):
        return self.get_or_create(domain=domain)[0]


class DomainSettings(models.Model):
    """MUA related settings for a domain."""

    domain = models.OneToOneField(
        'admin.Domain',
        on_delete=models.CASCADE,
        related_name='mua_settings',
    )
    server_name = models.CharField(
        max_length=253,
        blank=True,
        verbose_name=ugettext_lazy("Server name"),
        help_text=ugettext_lazy(
            "The server name to use for IMAP, POP and SMTP connections."
        ),
    )
    use_default = models.BooleanField(
        default=True,
        verbose_name=ugettext_lazy("Use default values"),
    )

    objects = DomainSettingsManager()

    @property
    def current_server_name(self) -> str:
        if self.use_default:
            return getattr(settings, 'AUTOMUA_DEFAULT_SERVER_NAME', None)
        return self.server_name or None

    def clean(self):
        if not self.use_default and not self.server_name:
            raise ValidationError(
                {
                    'server_name': ValidationError(
                        _(
                            "This field is required if default values are "
                            "not used."
                        ),
                        code='required',
                    )
                },
            )

    def save(self, *args, **kwargs):
        if self.use_default:
            self.server_name = ''
        super().save(*args, **kwargs)
