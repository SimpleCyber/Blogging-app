const promo = document.querySelector('.promo');
const popup = document.getElementById('popup');
const closePopup = document.getElementById('close-popup');

// Toggle the popup visibility on promo click
promo.addEventListener('click', () => {
  if (popup.style.display === 'block') {
    popup.style.display = 'none';
  } else {
    popup.style.display = 'block';
  }
});





