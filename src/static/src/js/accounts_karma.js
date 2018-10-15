/**
 * Incrementa en el karma de los usuarios.
 * src/templates/accounts/_buttons_karma.html
 */
$(document).ready(function() {
  // Controla el voto del usuario para no poder incrementar o decrementar
  // mas de una vez.
  let favoriteVote = $('#favorite-vote').data('favorite-vote');

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

  $('.karma-vote-positive').on('click', function() {
    const self = $(this);
    const elementNegative = $('.karma-vote-negative');
    const url = self.data('url');
    const messageSuccess = self.data('message-success');
    const elementValuePositives = $('.karma-positive-value');
    const valuePositives = parseInt(elementValuePositives.html());
    const elementValueNegatives = $('.karma-negative-value');
    const valueNegatives = parseInt(elementValueNegatives.html());

    // Comprueba si puede votar.
    if (!canVote('positive')) {
      toastr.warning('Solo puedes un boto positivo.');
      return;
    }

    $.ajax({
      method: 'POST',
      url: url
    }).done(function(data) {
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

  $('.karma-vote-negative').on('click', function() {
    const self = $(this);
    const elementPositive = $('.karma-vote-positive');
    const url = self.data('url');
    const messageSuccess = self.data('message-success');
    const elementValueNegatives = $('.karma-negative-value');
    const valueNegatives = parseInt(elementValueNegatives.html());
    const elementValuePositives = $('.karma-positive-value');
    const valuePositives = parseInt(elementValuePositives.html());

    // Comprueba si puede votar.
    if (!canVote('negative')) {
      toastr.warning('Solo puedes un boto negativo.');
      return;
    }

    $.ajax({
      method: 'POST',
      url: url
    }).done(function(data) {
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
