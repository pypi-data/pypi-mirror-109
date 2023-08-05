from django.utils.translation import ugettext_lazy

from modoboa.core.extensions import ModoExtension, exts_pool

from . import __version__


class AutoMUA(ModoExtension):
    """AutoMUA extension class."""

    name = 'modoboa_automua'
    label = 'automua'
    description = ugettext_lazy("Autoconfigure mail clients")
    version = __version__


exts_pool.register_extension(AutoMUA)
