import io
from abc import ABCMeta, abstractmethod
from xml.etree.ElementTree import Element, ElementTree, SubElement

from django.conf import settings
from django.utils.functional import cached_property
from django.utils.timezone import now

from .. import DEFAULT_SERVER_SERVICES, Service, ServiceSecurity, ServiceType

SERVER_SERVICES = getattr(
    settings, 'AUTOMUA_SERVER_SERVICES', DEFAULT_SERVER_SERVICES
)


def xml_to_string(element: Element) -> bytes:
    # The xml_declaration parameter is only added to the tostring method in
    # Python 3.8. To keep compatibility with 3.7, we mimic its behaviour here.
    stream = io.BytesIO()
    ElementTree(element).write(stream, 'utf-8', xml_declaration=True)
    return stream.getvalue()


class BaseFormatter(metaclass=ABCMeta):
    """
    Base class for an autoconfiguration response's formatter. As of now, it
    only provides facilities for an XML response.
    """

    content_type = 'text/xml'

    def __init__(self, user_email, domain_name, server_name):
        self.user_email = user_email
        self.domain_name = domain_name
        self.server_name = server_name

    @cached_property
    def response(self) -> str:
        return xml_to_string(self.get_xml_root_element())

    @abstractmethod
    def get_xml_root_element(self) -> Element:
        pass  # pragma: no cover


class AutoconfigFormatter(BaseFormatter):
    """Formatter for the configuration file of Mozilla.

    For documentation, see
    https://developer.mozilla.org/en-US/docs/Mozilla/Thunderbird/Autoconfiguration
    """

    def get_xml_root_element(self) -> Element:
        client_config = Element('clientConfig', attrib={'version': '1.1'})
        email_provider = SubElement(
            client_config, 'emailProvider', attrib={'id': self.domain_name}
        )

        SubElement(email_provider, 'domain').text = self.domain_name
        # FIXME: Are displayName and displayShortName mandatory?

        for server_service in SERVER_SERVICES:
            self.add_server_service_element(email_provider, server_service)

        return client_config

    def add_server_service_element(self, parent: Element, service: Service):
        tag = (
            'outgoingServer'
            if service.type == ServiceType.SMTP
            else 'incomingServer'
        )
        element = SubElement(
            parent, tag, attrib={'type': service.type.value.lower()}
        )
        SubElement(element, 'hostname').text = self.server_name
        SubElement(element, 'port').text = str(service.port)
        SubElement(element, 'socketType').text = service.security.value
        SubElement(element, 'authentication').text = 'password-cleartext'
        SubElement(element, 'username').text = '%EMAILADDRESS%'


class AutodiscoverFormatter(BaseFormatter):
    """Formatter for the POX Autodiscover service by Microsoft.

    For documentation, see
    https://docs.microsoft.com/en-us/exchange/client-developer/web-service-reference/pox-autodiscover-web-service-reference-for-exchange
    """

    NS_REQUEST = 'http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006'  # noqa: E501
    NS_RESPONSE = 'http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a'  # noqa: E501
    NS_RESPONSE_ROOT = 'http://schemas.microsoft.com/exchange/autodiscover/responseschema/2006'  # noqa: E501

    @classmethod
    def get_email_from_request(cls, root: Element) -> str:
        """Extract the email address from a POX Autodiscover request."""
        namespaces = {'ns': cls.NS_REQUEST}
        response_schema = root.find(
            f'ns:Request/[ns:AcceptableResponseSchema=\'{cls.NS_RESPONSE}\']',
            namespaces,
        )
        if response_schema is None:
            raise ValueError('Unsupported acceptable response schema')
        email_address = root.find('ns:Request/ns:EMailAddress', namespaces)
        if email_address is None:
            raise ValueError('Missing email address from the request')
        return email_address.text

    @classmethod
    def response_for_error(cls, message: str, code: int) -> str:
        """Generate the response content for an Autodiscover error."""
        autodiscover = Element(
            'Autodiscover', attrib={'xmlns': cls.NS_RESPONSE_ROOT}
        )
        response = SubElement(autodiscover, 'Response')

        error = SubElement(
            response, 'Error', attrib={'Time': now().strftime('%H:%M:%S.%f')}
        )
        SubElement(error, 'ErrorCode').text = str(code)
        SubElement(error, 'Message').text = message

        return xml_to_string(autodiscover)

    def get_xml_root_element(self) -> Element:
        autodiscover = Element(
            'Autodiscover', attrib={'xmlns': self.NS_RESPONSE_ROOT}
        )
        response = SubElement(
            autodiscover, 'Response', attrib={'xmlns': self.NS_RESPONSE}
        )

        user = SubElement(response, 'User')
        SubElement(user, 'DisplayName').text = self.user_email

        account = SubElement(response, 'Account')
        SubElement(account, 'AccountType').text = 'email'
        SubElement(account, 'Action').text = 'settings'

        for server_service in SERVER_SERVICES:
            self.add_account_protocol_element(account, server_service)

        return autodiscover

    def add_account_protocol_element(self, parent: Element, service: Service):
        element = SubElement(parent, 'Protocol')
        SubElement(element, 'Type').text = service.type.value
        SubElement(element, 'Server').text = self.server_name
        SubElement(element, 'Port').text = str(service.port)
        SubElement(element, 'LoginName').text = self.user_email
        SubElement(element, 'SPA').text = 'off'
        SubElement(element, 'SSL').text = (
            'on' if service.security == ServiceSecurity.SSL else 'off'
        )
