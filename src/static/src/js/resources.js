$(document).ready(function() {
  /**
   * Selects de categorías y tags, cuando cambia el valor,
   * la pagina redirecciona al la cat/tag seleccionadas.
   *
   * src/templates/resources/_nav_list.html
   */
  // categories
  $('#id_select_category').change(function() {
    const redirectTo = $(this).find(':selected').data('redirect-to');
    if (redirectTo) {
      window.location.href = redirectTo;
    }
  });

  // Tags
  $('#id_select_tag').change(function() {
    const redirectTo = $(this).find(':selected').data('redirect-to');
    if (redirectTo) {
      window.location.href = redirectTo;
    }
  });

  /**
   * Marcar un link de resource como roto.
   *
   * src/templates/resources/details.html
   */
  $('#resource-broken-link').on('click', function() {
    const self = $(this);
    const url = self.data('url');
    const messageSuccess = self.data('message-success');

    $.ajax({
      type: 'POST',
      url: url,

      success: function(data) {
        if (data === 'OK') {
          toastr.success(messageSuccess);
        }
      }
    });
  });

  /**
   * Marcar un link de resource como spam.
   *
   * src/templates/resources/details.html
   */
  $('#resource-spam-link').on('click', function() {
    const self = $(this);
    const url = self.data('url');
    const messageSuccess = self.data('message-success');

    $.ajax({
      type: 'POST',
      url: url,

      success: function(data) {
        if (data === 'OK') {
          toastr.success(messageSuccess);
        }
      }
    });
  });

  /**
   * El owner de un Resource limpia los links marcados como rotos.
   *
   * src/templates/resources/_resource_owner_info.html
   */
  $('.owner-broken-soluciona').on('click', function() {
    const self = $(this);
    const url = self.data('resource-url');
    const messageSuccess = self.data('message-success');

    $.ajax({
      method: 'POST',
      url: url,

      success: function(data) {
        if (data === 'OK') {
          self.remove();
          $('.resouces-broken-count').html(0);
          toastr.success(messageSuccess);
        }
      }
    });
  });

  /**
   * El superuser limpia los links marcados como spam.
   *
   * src/templates/resources/list_spam_links.html
   */
  $('.superuser-spam-soluciona').on('click', function() {
    const self = $(this);
    const url = self.data('resource-url');
    const messageSuccess = self.data('message-success');

    $.ajax({
      method: 'POST',
      url: url,

      success: function(data) {
        if (data === 'OK') {
          self.remove();
          $('.resouces-broken-count').html(0);
          toastr.success(messageSuccess);
        }
      }
    });
  });
});
