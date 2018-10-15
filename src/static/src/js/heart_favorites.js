$(document).ready(function() {
  /**
   * Añade un resource a favoritos via AJAX.
   *
   * src/templates/favorites/_heart_favorite.html
   */
  $('.add-resource-favorite').on('click', function() {
    const self = $(this);
    const resourceId = self.data('resource-id');
    const url = self.data('url');
    const messageSuccess = self.data('message-success');

    $.ajax({
      method: 'POST',
      url: url,
      data: {'resource_id': resourceId}
    })
    .done(function(data) {
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
  $('.remove-resource-favorite').on('click', function() {
    const self = $(this);
    const resourceId = self.data('resource-id');
    const url = self.data('url');
    const messageSuccess = self.data('message-success');

    $.ajax({
      method: 'POST',
      url: url,
      data: {'resource_id': resourceId}
    })
    .done(function(data) {
      if (data === 'OK') {
        toastr.success(messageSuccess);
        self.toggleClass('hidden');
        self.siblings().toggleClass('hidden');
      }
    });
  });
});
