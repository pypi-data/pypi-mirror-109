from http import HTTPStatus
from xml.etree.ElementTree import ParseError

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import validate_email
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from defusedxml.ElementTree import parse as parse_xml

from ..models import DomainSettings
from .formatters import AutoconfigFormatter, AutodiscoverFormatter


class EmailResponseMixin:
    """
    Provide facilities for an autoconfiguration view to respond to a request
    for a given email address.
    """

    #: A BaseFormatter derived class to use for formatting the response.
    formatter_class = None

    def response_for_email(self, email: str) -> HttpResponse:
        """Validate the email address and return the relevant response."""
        try:
            validate_email(email)
        except ValidationError:
            return self.error_response('Invalid email address')

        domain_name = email.rsplit('@', 1)[1].lower()
        server_name = self.get_server_name_for_domain(domain_name)

        if not server_name:
            return self.error_response(
                'No configuration found for the domain', HTTPStatus.NOT_FOUND
            )

        formatter = self.formatter_class(email, domain_name, server_name)
        return HttpResponse(formatter.response, formatter.content_type)

    def error_response(
        self, message: str, status_code: HTTPStatus = HTTPStatus.BAD_REQUEST
    ) -> HttpResponse:
        """Return the relevant response for the given error."""
        return HttpResponse(message, status=status_code)

    def get_server_name_for_domain(self, domain_name: str) -> str:
        """Return the server name to use for the given domain name."""
        try:
            domain_settings = DomainSettings.objects.get(
                domain__name=domain_name, domain__enabled=True
            )
        except ObjectDoesNotExist:
            return None
        return domain_settings.current_server_name


class AutoconfigView(EmailResponseMixin, View):
    formatter_class = AutoconfigFormatter

    def get(self, request):
        try:
            email = request.GET['emailaddress']
        except KeyError:
            return self.error_response(
                'Missing email address from query string'
            )
        return self.response_for_email(email)


@method_decorator(csrf_exempt, name='dispatch')
class AutodiscoverView(EmailResponseMixin, View):
    formatter_class = AutodiscoverFormatter

    def post(self, request):
        if request.content_type not in {'application/xml', 'text/xml'}:
            return self.error_response('Invalid content type')
        try:
            email = self.formatter_class.get_email_from_request(
                parse_xml(request)
            )
        except ParseError:
            return self.error_response('Unable to parse request')
        except ValueError as e:
            return self.error_response(str(e))
        return self.response_for_email(email)

    def error_response(
        self, message: str, status_code: HTTPStatus = HTTPStatus.BAD_REQUEST
    ) -> HttpResponse:
        content = self.formatter_class.response_for_error(
            message, status_code.value
        )
        return HttpResponse(content, 'text/xml')
