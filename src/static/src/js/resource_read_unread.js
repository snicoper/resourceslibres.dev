/**
 * Un usuario marca un recurso como leído/no leído.
 * src/templates/read/_resource_read_unread.html
 */
$(document).ready(function() {
  $('.resource-user-read').on('click', function() {
    const self = $(this);
    const url = self.data('url');
    const hasRead = self.data('user-has-read');
    const messageSuccess = self.data('message-success');
    let elementHide;

    $.ajax({
      method: 'POST',
      url: url
    }).done(function(data) {
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
