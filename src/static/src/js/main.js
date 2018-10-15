$(document).ready(function() {
  // CSRF TOKEN DJANGO
  $.ajaxSetup({
    beforeSend: function(xhr, settings) { // eslint-disable-line no-unused-vars
      xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
    }
  });

  // tooltip por defecto.
  $(function() {
    $('[data-toggle="tooltip"]').tooltip();
  });
});
