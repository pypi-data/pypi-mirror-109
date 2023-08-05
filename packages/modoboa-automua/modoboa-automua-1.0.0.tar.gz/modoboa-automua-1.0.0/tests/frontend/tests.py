from pathlib import Path
from xml.dom import minidom

from modoboa.admin.factories import DomainFactory
from modoboa.lib.tests import ModoTestCase

from tests.factories import DomainSettingsFactory

DATA_DIR = Path(__file__).parent / 'data'


def response_to_string(response):
    return response.content.decode(response.charset)


class AutoconfigViewTests(ModoTestCase):
    url = '/mail/config-v1.1.xml'

    def get(self, *args, **kwargs):
        return self.client.get(self.url, *args, **kwargs)

    def test_invalid_email_address(self):
        self.assertContains(
            self.get(), 'Missing email address', status_code=400
        )

        self.assertContains(
            self.get({'emailaddress': 'pouet'}), 'Invalid', status_code=400
        )

    def test_no_configuration(self):
        data = {'emailaddress': 'user@example.org'}

        self.assertContains(self.get(data), 'No configuration', status_code=404)

        domain = DomainFactory(name='example.org', enabled=False)
        domain_settings = DomainSettingsFactory(domain=domain)

        with self.settings(AUTOMUA_DEFAULT_SERVER_NAME='mx.example.org'):
            self.assertContains(
                self.get(data), 'No configuration', status_code=404
            )

        domain.enabled = True
        domain.save()

        self.assertContains(self.get(data), 'No configuration', status_code=404)

        domain_settings.use_default = False
        domain_settings.server_name = ''
        domain_settings.save()

        self.assertContains(self.get(data), 'No configuration', status_code=404)

    def test_response(self):
        DomainSettingsFactory(
            domain__name='example.org',
            server_name='mail.example.org',
            use_default=False,
        )
        data = {'emailaddress': 'user@example.org'}

        response = self.get(data)
        self.assertEqual(response.status_code, 200)
        with (DATA_DIR / 'autoconfig.xml').open() as f:
            xml_tree = minidom.parseString(response_to_string(response))
            self.assertXMLEqual(xml_tree.toprettyxml(), f.read())


class AutodiscoverViewTests(ModoTestCase):
    url = '/autodiscover/autodiscover.xml'

    @property
    def request_payload(self):
        return """
<Autodiscover xmlns="http://schemas.microsoft.com/exchange/autodiscover/outlook/requestschema/2006">
  <Request>
    <EMailAddress>user@example.org</EMailAddress>
    <AcceptableResponseSchema>http://schemas.microsoft.com/exchange/autodiscover/outlook/responseschema/2006a</AcceptableResponseSchema>
  </Request>
 </Autodiscover>
"""  # noqa: E501

    def post(self, *args, **kwargs):
        kwargs.setdefault('content_type', 'text/xml')
        return self.client.post(self.url, *args, **kwargs)

    def assertErrorResponse(self, response, message, code=400):
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/xml')
        content = response_to_string(response)
        self.assertInHTML(f'<ErrorCode>{code}</ErrorCode>', content)
        self.assertInHTML(f'<Message>{message}</Message>', content)

    def test_invalid_request(self):
        self.assertErrorResponse(
            self.client.post(self.url), 'Invalid content type'
        )

        self.assertErrorResponse(
            self.post('<invalid xml>'), 'Unable to parse request'
        )

        data = self.request_payload.replace('2006a', '2030')
        self.assertErrorResponse(
            self.post(data), 'Unsupported acceptable response schema'
        )

        data = self.request_payload.replace('EMailAddress', 'EMail')
        self.assertErrorResponse(
            self.post(data), 'Missing email address from the request'
        )

    def test_response(self):
        DomainSettingsFactory(
            domain__name='example.org',
            server_name='mail.example.org',
            use_default=False,
        )

        response = self.post(self.request_payload)
        self.assertEqual(response.status_code, 200)
        with (DATA_DIR / 'autodiscover.xml').open() as f:
            xml_tree = minidom.parseString(response_to_string(response))
            self.assertXMLEqual(xml_tree.toprettyxml(), f.read())
