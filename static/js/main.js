/* PetDiary — дневник питомца: поведение страниц */
(function () {
  'use strict';

  // Плавная прокрутка к активному уведомлению (если такое есть)
  document.addEventListener('DOMContentLoaded', function () {
    var msgs = document.querySelectorAll('.messages .alert');
    if (msgs.length) {
      var last = msgs[msgs.length - 1];
      last.scrollIntoView({ behavior: 'smooth', block: 'center' });
      setTimeout(function () { last.classList.add('alert-shown'); }, 1500);
    }
    // Пометить карточки питомцев нажатием
    var petCards = document.querySelectorAll('a.card-link[href*="pets_detail"]');
    petCards.forEach(function (el) {
      el.addEventListener('click', function () { sessionStorage.setItem('pet_last_viewed', el.getAttribute('href')); });
    });
    // Фокус на поле формы
    var firstField = document.querySelector('.form .form-group input, .form .form-group select, .form .form-group textarea');
    if (firstField && firstField.type !== 'submit') { firstField.focus(); }
  });
})();
