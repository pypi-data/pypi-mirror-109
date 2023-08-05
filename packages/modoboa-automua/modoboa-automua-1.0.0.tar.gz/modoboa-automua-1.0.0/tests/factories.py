from modoboa.admin.factories import DomainFactory

import factory

from modoboa_automua.models import DomainSettings


class DomainSettingsFactory(factory.DjangoModelFactory):
    domain = factory.SubFactory(DomainFactory)

    class Meta:
        model = DomainSettings
