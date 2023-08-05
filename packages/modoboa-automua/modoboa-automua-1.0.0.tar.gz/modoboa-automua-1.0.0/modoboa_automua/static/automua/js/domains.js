function initDomainSettingsForm() {
  const useDefaultCheckbox = document.getElementById('id_use_default');
  const customSettings = document.getElementById('mua_domain_settings');

  function toggleCustomSettings(enabled) {
    if (enabled) {
      customSettings.removeAttribute('disabled');
    } else {
      customSettings.setAttribute('disabled', '');
    }
  }

  useDefaultCheckbox.addEventListener('click', function () {
    toggleCustomSettings(!useDefaultCheckbox.checked);
  });

  toggleCustomSettings(!useDefaultCheckbox.checked);
}

$(document).ready(function () {
  $(this).bind('domwizard_init', initDomainSettingsForm);
  $(this).bind('domform_init', initDomainSettingsForm);
});
