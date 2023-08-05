#!/usr/bin/env python
import os
import sys

import django

sys.stdout.write(
    "Using Python version {0} from {1}\n".format(
        sys.version[:5], sys.executable
    )
)
sys.stdout.write(
    "Using Django version {0} from {1}\n\n".format(
        django.__version__, os.path.dirname(os.path.abspath(django.__file__))
    )
)


def run_tests(test_label, reset=False):
    if reset:
        from importlib import reload

        import django.apps
        import django.conf

        reload(django.apps)
        reload(django.conf)

    import django
    from django.core.management import call_command

    django.setup()
    call_command('test', *list(sys.argv[1:] + [test_label]))


if __name__ == '__main__':
    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
    run_tests('tests')

    sys.stdout.write("\nRunning frontend tests in standalone...\n")

    os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.frontend.settings'
    run_tests('tests.frontend', reset=True)
