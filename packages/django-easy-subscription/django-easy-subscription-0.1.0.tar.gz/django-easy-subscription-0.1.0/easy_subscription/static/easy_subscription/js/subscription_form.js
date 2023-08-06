document.querySelector('#easy_subscription_btn').addEventListener('click', function(e) {
  e.preventDefault();
  document.querySelector('.popup-overlay[newsletter-form=""][active="false"]').setAttribute('active', 'true');
  return false;
});

document.querySelector('.popup-close-button[newsletter-form=""]').addEventListener('click', function(e) {
  e.preventDefault();
  document.querySelector('.popup-overlay[newsletter-form=""][active="true"]').setAttribute('active', 'false');
});

document.querySelector('.popup-overlay[newsletter-form=""]').addEventListener('click', function(e) {
  if (e.target === this && this.getAttribute('active') === 'true') {
    this.setAttribute('active', 'false');
  }
});

document.querySelector('.popup-form[newsletter-form=""]').addEventListener('submit', function(e) {
  e.preventDefault();
  var form_data = new FormData(this);
  var parts = ("; " + document.cookie).split("; csrftoken=");
  var csrf_token = parts.length === 2 ? parts.pop().split(";").shift():'';

  var xhr = new XMLHttpRequest();
  xhr.open('POST', this.action, true);
  xhr.setRequestHeader("X-CSRFToken", csrf_token);
  xhr.onload = function () {
    if (xhr.status === 200) {
      var response = JSON.parse(xhr.response);
      var message = response['message'].replace(/\n/g, "<br>");
      document.querySelector('.popup-form-body[newsletter-form=""]').innerHTML =
        '<div newsletter-form class="popup-form-body-row">' +
          '<p newsletter-form class="popup-form-success-message">' + message + '</p>' +
        '</div>'
      ;
    } else if (xhr.status === 400) {
      var errors = JSON.parse(xhr.response);
      if (errors.hasOwnProperty('first_name')) {
        document.querySelector('#id_first_name[newsletter-form=""]').nextElementSibling.innerHTML = errors['first_name'];
      }
      if (errors.hasOwnProperty('last_name')) {
        document.querySelector('#id_last_name[newsletter-form=""]').nextElementSibling.innerHTML = errors['last_name'];
      }
      if (errors.hasOwnProperty('email')) {
        document.querySelector('#id_email[newsletter-form=""]').nextElementSibling.innerHTML = errors['email'];
      }
    }
  };
  xhr.send(form_data);
  return false;
});
