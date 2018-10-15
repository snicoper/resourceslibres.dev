'use strict';

/**
 * Incrementa en el karma de los usuarios.
 * src/templates/accounts/_buttons_karma.html
 */
$(document).ready(function () {
  // Controla el voto del usuario para no poder incrementar o decrementar
  // mas de una vez.
  var favoriteVote = $('#favorite-vote').data('favorite-vote');

  /**
   * Prueba si puede votar en el botón.
   * Cambia el valor del favoriteVote a vote (no requiere cambiar el DOM).
   *
   * @param  {string} vote negative|positive
   * @return {bool} true en caso de poder votar, false en caso contrario.
   */
  function canVote(vote) {
    // Si es undefined, es que aun no ha votado.
    if (favoriteVote !== 'undefined' && favoriteVote === vote) {
      return false;
    }

    // Cambiar el valor de favoriteVote.
    favoriteVote = vote;

    return true;
  }

  $('.karma-vote-positive').on('click', function () {
    var self = $(this);
    var elementNegative = $('.karma-vote-negative');
    var url = self.data('url');
    var messageSuccess = self.data('message-success');
    var elementValuePositives = $('.karma-positive-value');
    var valuePositives = parseInt(elementValuePositives.html());
    var elementValueNegatives = $('.karma-negative-value');
    var valueNegatives = parseInt(elementValueNegatives.html());

    // Comprueba si puede votar.
    if (!canVote('positive')) {
      toastr.warning('Solo puedes un boto positivo.');
      return;
    }

    $.ajax({
      method: 'POST',
      url: url
    }).done(function (data) {
      if (data === 'OK') {
        // Asegurarse de quitar bg-danger en la class de negative.
        elementNegative.removeClass('btn-danger text-white');
        elementNegative.addClass('btn-outline-danger');
        self.removeClass('btn-outline-success');
        self.addClass('btn-success text-white');

        // Incrementar el contador en 1 en positive y decrementar en 1 en negative.
        if (valueNegatives > 0) {
          elementValueNegatives.html(valueNegatives - 1);
        }
        elementValuePositives.html(valuePositives + 1);

        // Mostrar mensaje.
        toastr.success(messageSuccess);
      }
    });
  });

  $('.karma-vote-negative').on('click', function () {
    var self = $(this);
    var elementPositive = $('.karma-vote-positive');
    var url = self.data('url');
    var messageSuccess = self.data('message-success');
    var elementValueNegatives = $('.karma-negative-value');
    var valueNegatives = parseInt(elementValueNegatives.html());
    var elementValuePositives = $('.karma-positive-value');
    var valuePositives = parseInt(elementValuePositives.html());

    // Comprueba si puede votar.
    if (!canVote('negative')) {
      toastr.warning('Solo puedes un boto negativo.');
      return;
    }

    $.ajax({
      method: 'POST',
      url: url
    }).done(function (data) {
      if (data === 'OK') {
        // Asegurarse de quitar bg-success en la class de positive.
        elementPositive.removeClass('btn-success text-white');
        elementPositive.addClass('btn-outline-success');
        self.removeClass('btn-outline-danger');
        self.addClass('btn-danger text-white');

        // Incrementar el contador en 1 en negative y decrementar en 1 en positive.
        if (valuePositives > 0) {
          elementValuePositives.html(valuePositives - 1);
        }
        elementValueNegatives.html(valueNegatives + 1);

        // Mostrar mensaje.
        toastr.success(messageSuccess);
      }
    });
  });
});

$(document).ready(function () {
  /**
   * Añade un resource a favoritos via AJAX.
   *
   * src/templates/favorites/_heart_favorite.html
   */
  $('.add-resource-favorite').on('click', function () {
    var self = $(this);
    var resourceId = self.data('resource-id');
    var url = self.data('url');
    var messageSuccess = self.data('message-success');

    $.ajax({
      method: 'POST',
      url: url,
      data: { 'resource_id': resourceId }
    }).done(function (data) {
      if (data === 'OK') {
        toastr.success(messageSuccess);
        self.toggleClass('hidden');
        self.siblings().toggleClass('hidden');
      }
    });
  });

  /**
   * Elimina un resource de favoritos via AJAX.
   *
   * src/templates/favorites/_heart_favorite.html
   */
  $('.remove-resource-favorite').on('click', function () {
    var self = $(this);
    var resourceId = self.data('resource-id');
    var url = self.data('url');
    var messageSuccess = self.data('message-success');

    $.ajax({
      method: 'POST',
      url: url,
      data: { 'resource_id': resourceId }
    }).done(function (data) {
      if (data === 'OK') {
        toastr.success(messageSuccess);
        self.toggleClass('hidden');
        self.siblings().toggleClass('hidden');
      }
    });
  });
});

/**
 * Carga una imagen de un input type file para mostrarla
 * en un elemento <img>
 * @param  {str} $idTagImage id en la etiqueta <img id=""> con formato Jquery #my-id-tag
 * @param  {str} input       Elemento del input
 *
 * $("#id_avatar").change(function(){
 *   readImagePreview('#img-avatar', this);
 * });
 *
 * #id_avatar es el campo type field.
 * #img-avatar es el id del elemento <img>
 */
function readImagePreview($idTagImage, input) {
  // eslint-disable-line no-unused-vars
  var reader = new FileReader();

  if (input.files && input.files[0]) {
    reader.onload = function (e) {
      $($idTagImage).attr('src', e.target.result);
    };
    reader.readAsDataURL(input.files[0]);
  }
}

$(document).ready(function () {
  // CSRF TOKEN DJANGO
  $.ajaxSetup({
    beforeSend: function beforeSend(xhr, settings) {
      // eslint-disable-line no-unused-vars
      xhr.setRequestHeader('X-CSRFToken', Cookies.get('csrftoken'));
    }
  });

  // tooltip por defecto.
  $(function () {
    $('[data-toggle="tooltip"]').tooltip();
  });
});

/**
 * Estrellas con el ratio del resource.
 */
$(function () {
  $('.anuncio-rating-stars').each(function (index, value) {
    var self = $(this);
    var readonly = self.data('readonly') === 1;
    var url = self.data('url');
    var messageText = self.data('message-text');
    var messageSuccess = self.data('message-success');

    // En Spanish por ejemplo, separa los decimales con comas.
    value = self.data('value').replace(',', '.');

    // El valor por defecto en caso de no tener votos, es de -1 para que no
    // muestre ninguna estrella.
    if (value === 0) {
      value = -1;
    }

    self.barrating({
      theme: 'fontawesome-stars-o',
      initialRating: value,
      readonly: readonly,
      showSelectedRating: true,

      onSelect: function onSelect(value, text, event) {
        if (typeof event !== 'undefined') {
          $.ajax({
            url: url,
            data: { score: value },
            success: function success(data) {
              data = parseFloat(data);
              if (data > 0) {
                var htmlElement = $('.anuncio-user-score');
                var content = messageText + ' ' + value + ' <i class="material-icons">star</i>';

                // Actualizar el ratio.
                self.barrating('set', data);
                toastr.success(messageSuccess);

                // Actualizar el score del usuario.
                htmlElement.html(content);
                htmlElement.removeClass('hide');
              }
            }
          });
        }
      }
    });
  });
});

/**
 * Un usuario marca un recurso como leído/no leído.
 * src/templates/read/_resource_read_unread.html
 */
$(document).ready(function () {
  $('.resource-user-read').on('click', function () {
    var self = $(this);
    var url = self.data('url');
    var hasRead = self.data('user-has-read');
    var messageSuccess = self.data('message-success');
    var elementHide = void 0;

    $.ajax({
      method: 'POST',
      url: url
    }).done(function (data) {
      if (data === 'OK') {
        self.addClass('hidden');

        if (hasRead === true) {
          elementHide = '.mark-has-unread';
        } else {
          elementHide = '.mark-has-read';
        }

        self.parent('.resource-read-unread').children(elementHide).removeClass('hidden');
        toastr.success(messageSuccess);
      }
    });
  });
});

$(document).ready(function () {
  /**
   * Selects de categorías y tags, cuando cambia el valor,
   * la pagina redirecciona al la cat/tag seleccionadas.
   *
   * src/templates/resources/_nav_list.html
   */
  // categories
  $('#id_select_category').change(function () {
    var redirectTo = $(this).find(':selected').data('redirect-to');
    if (redirectTo) {
      window.location.href = redirectTo;
    }
  });

  // Tags
  $('#id_select_tag').change(function () {
    var redirectTo = $(this).find(':selected').data('redirect-to');
    if (redirectTo) {
      window.location.href = redirectTo;
    }
  });

  /**
   * Marcar un link de resource como roto.
   *
   * src/templates/resources/details.html
   */
  $('#resource-broken-link').on('click', function () {
    var self = $(this);
    var url = self.data('url');
    var messageSuccess = self.data('message-success');

    $.ajax({
      type: 'POST',
      url: url,

      success: function success(data) {
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
  $('#resource-spam-link').on('click', function () {
    var self = $(this);
    var url = self.data('url');
    var messageSuccess = self.data('message-success');

    $.ajax({
      type: 'POST',
      url: url,

      success: function success(data) {
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
  $('.owner-broken-soluciona').on('click', function () {
    var self = $(this);
    var url = self.data('resource-url');
    var messageSuccess = self.data('message-success');

    $.ajax({
      method: 'POST',
      url: url,

      success: function success(data) {
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
  $('.superuser-spam-soluciona').on('click', function () {
    var self = $(this);
    var url = self.data('resource-url');
    var messageSuccess = self.data('message-success');

    $.ajax({
      method: 'POST',
      url: url,

      success: function success(data) {
        if (data === 'OK') {
          self.remove();
          $('.resouces-broken-count').html(0);
          toastr.success(messageSuccess);
        }
      }
    });
  });
});

// to-top
(function () {
  var offset = 220;
  var duration = 500;

  jQuery(window).scroll(function () {
    if (jQuery(this).scrollTop() > offset) {
      jQuery('.to-top').fadeIn(duration);
    } else {
      jQuery('.to-top').fadeOut(duration);
    }
  });

  jQuery('.to-top').click(function (event) {
    event.preventDefault();
    jQuery('html, body').animate({ scrollTop: 0 }, duration);
    return false;
  });
})();
//# sourceMappingURL=main.js.map
