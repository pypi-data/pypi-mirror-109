from django.urls import Resolver404, clear_url_caches, resolve, reverse

from modoboa.admin.factories import DomainFactory
from modoboa.admin.models import Domain
from modoboa.lib.tests import ModoTestCase

from modoboa_automua.models import DomainSettings

from .factories import DomainSettingsFactory


class DomainAdminViewsTests(ModoTestCase):
    domain_add_url = reverse('admin:domain_add')
    widget_panel_title = '<h3 class="panel-title">MUA</h3>'

    def test_extra_js_content(self):
        script = '<script src="/sitestatic/automua/js/domains.js" '
        response = self.client.get(reverse('admin:domain_list'))
        self.assertContains(response, script, msg_prefix='domain_list')
        response = self.client.get(reverse('admin:identity_list'))
        self.assertNotContains(response, script, msg_prefix='identity_list')

    def test_create_domain_with_server_name(self):
        domain_name = 'example.org'
        server_name = 'mail.example.org'
        data = {
            'name': domain_name,
            'type': 'domain',
            'quota': 0,
            'default_mailbox_quota': 0,
            'enabled': True,
            'service': 'relay',
            'use_default': False,
            'server_name': server_name,
            'create_dom_admin': False,
            'stepid': 'step4',
        }
        self.ajax_post(self.domain_add_url, data, status=200)

        domain = Domain.objects.get(name=domain_name)
        self.assertFalse(domain.mua_settings.use_default)
        self.assertEqual(domain.mua_settings.server_name, server_name)

    def test_create_domain_with_default(self):
        domain_name = 'example.org'
        data = {
            'name': domain_name,
            'type': 'domain',
            'quota': 0,
            'default_mailbox_quota': 0,
            'enabled': True,
            'service': 'relay',
            'use_default': True,
            'server_name': 'not-used.example.org',
            'create_dom_admin': False,
            'stepid': 'step4',
        }
        self.ajax_post(self.domain_add_url, data, status=200)

        domain = Domain.objects.get(name=domain_name)
        self.assertTrue(domain.mua_settings.use_default)
        self.assertEqual(domain.mua_settings.server_name, '')

    def test_detail_domain_mua_widget_with_default(self):
        domain = DomainSettingsFactory(use_default=True).domain
        detail_url = reverse('admin:domain_detail', args=[domain.id])

        response = self.client.get(detail_url)
        self.assertContains(response, self.widget_panel_title)
        self.assertContains(response, '<td>–</td>')

        with self.settings(AUTOMUA_DEFAULT_SERVER_NAME='mx.example.org'):
            response = self.client.get(detail_url)
            self.assertContains(response, '<td>mx.example.org</td>')

    def test_detail_domain_mua_widget_with_server_name(self):
        domain = DomainSettingsFactory(
            use_default=False, server_name='mail.example.org'
        ).domain
        detail_url = reverse('admin:domain_detail', args=[domain.id])
        response = self.client.get(detail_url)
        self.assertContains(response, '<td>mail.example.org</td>')

    def test_detail_domain_mua_widget_without_settings(self):
        domain = DomainFactory(name='example.org')
        detail_url = reverse('admin:domain_detail', args=[domain.id])
        response = self.client.get(detail_url)
        self.assertNotContains(response, self.widget_panel_title)

    def test_detail_relaydomain_no_mua_widget(self):
        domain = DomainFactory(name='example.org', type='relaydomain')
        detail_url = reverse('admin:domain_detail', args=[domain.id])

        response = self.client.get(detail_url)
        self.assertNotContains(response, self.widget_panel_title)

    def test_edit_domain_default_to_server_name(self):
        mua_settings = DomainSettingsFactory(use_default=True)
        edit_url = reverse('admin:domain_change', args=[mua_settings.domain.id])

        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        servers_tab = response.context['tabs'].forms[1]
        self.assertEqual(servers_tab['id'], 'mua')
        self.assertEqual(servers_tab['instance'].instance, mua_settings)

        data = {
            'name': mua_settings.domain.name,
            'type': 'domain',
            'quota': 0,
            'default_mailbox_quota': 0,
            'enabled': True,
            'service': 'relay',
            'use_default': False,
            'server_name': '',
        }
        response = self.ajax_post(edit_url, data, status=400)
        self.assertEqual(response['form_errors'].keys(), {'server_name'})

        data['server_name'] = 'mail.example.org'
        self.ajax_post(edit_url, data)

        mua_settings.refresh_from_db()
        self.assertFalse(mua_settings.use_default)
        self.assertEqual(mua_settings.server_name, 'mail.example.org')

    def test_edit_domain_without_settings(self):
        domain = DomainFactory()
        edit_url = reverse('admin:domain_change', args=[domain.id])

        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        instance = response.context['tabs'].forms[1]['instance'].instance
        self.assertIsNotNone(instance.pk)
        self.assertEqual(instance.domain, domain)

    def test_edit_domain_to_relaydomain(self):
        domain = DomainSettingsFactory().domain
        edit_url = reverse('admin:domain_change', args=[domain.id])

        data = {
            'name': domain.name,
            'type': 'relaydomain',
            'quota': 0,
            'default_mailbox_quota': 0,
            'enabled': True,
            'use_default': True,
            'server_name': '',
        }
        self.ajax_post(edit_url, data)

        response = self.client.get(edit_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['tabs'].forms), 2)
        self.assertEqual(response.context['tabs'].forms[1]['id'], 'relaydomain')

    def test_delete_domain(self):
        domain = DomainSettingsFactory().domain
        self.ajax_post(reverse('admin:domain_delete', args=[domain.id]))
        self.assertFalse(
            DomainSettings.objects.filter(domain__name=domain.name).exists()
        )


class ServeFrontendRoutesTests(ModoTestCase):
    url = '/mail/config-v1.1.xml'

    def tearDown(self):
        self.clear_url_caches()

    def clear_url_caches(self):
        from importlib import reload

        import modoboa.urls

        import tests.urls

        reload(modoboa.urls)
        reload(tests.urls)

        clear_url_caches()

    def test_served(self):
        with self.settings(AUTOMUA_SERVE_FRONTEND_ROUTES=True):
            self.clear_url_caches()

            resolve(self.url)

    def test_not_served(self):
        with self.settings(AUTOMUA_SERVE_FRONTEND_ROUTES=False):
            self.clear_url_caches()

            with self.assertRaises(Resolver404):
                resolve(self.url)
