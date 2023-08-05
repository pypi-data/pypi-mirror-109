from dataclasses import dataclass
from enum import Enum

from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:  # pragma: no cover
    # package is not installed
    pass

default_app_config = 'modoboa_automua.apps.ModoboaAutoMUAConfig'


class ServiceType(Enum):
    POP = 'POP3'
    IMAP = 'IMAP'
    SMTP = 'SMTP'


class ServiceSecurity(Enum):
    SSL = 'SSL'
    STARTTLS = 'STARTTLS'


@dataclass(frozen=True)
class Service:
    type: ServiceType
    port: int
    security: ServiceSecurity


"""The default mail services which will be annouced for each domain."""
DEFAULT_SERVER_SERVICES = (
    Service(ServiceType.POP, 995, ServiceSecurity.SSL),
    Service(ServiceType.POP, 110, ServiceSecurity.STARTTLS),
    Service(ServiceType.IMAP, 993, ServiceSecurity.SSL),
    Service(ServiceType.IMAP, 143, ServiceSecurity.STARTTLS),
    Service(ServiceType.SMTP, 465, ServiceSecurity.SSL),
    Service(ServiceType.SMTP, 587, ServiceSecurity.STARTTLS),
)
