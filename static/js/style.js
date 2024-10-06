// fixer le menu lors du defilement
window.addEventListener('scroll', function() {
    var mainNavbar = document.getElementById('mainNavbar');
    var spacer = document.querySelector('.spacer');
    if (window.scrollY > mainNavbar.offsetTop) {
      mainNavbar.classList.add('fixed-navbar');
      spacer.style.display = 'block'; // Ensure spacer is visible
    } else {
      mainNavbar.classList.remove('fixed-navbar');
      spacer.style.display = 'none'; // Hide spacer when not needed
    }
  });

// SLIDE IMAGE MINIATURE CATEGORY
const track = document.querySelector('.carousel-track');
const cards = Array.from(track.children);
const nextButton = document.querySelector('.carousel-button.right');
const prevButton = document.querySelector('.carousel-button.left');
const cardWidth = cards[0].getBoundingClientRect().width + 20; // Include margin
const visibleCards = 4; // Number of visible cards
let currentIndex = 0;

function moveToCard(index) {
    const amountToMove = cardWidth * index;
    track.style.transition = 'transform 0.5s ease-in-out';
    track.style.transform = `translateX(-${amountToMove}px)`;
}

function autoSlide() {
    currentIndex++;
    if (currentIndex > cards.length - visibleCards) {
        setTimeout(() => {
            track.style.transition = 'none';
            track.style.transform = 'translateX(0)';
            currentIndex = 0;
        }, 500); // Match the duration of the transition
    } else {
        moveToCard(currentIndex);
    }
}

nextButton.addEventListener('click', autoSlide);

prevButton.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + cards.length) % cards.length;
    moveToCard(currentIndex);
});

// Auto slide every 3 seconds
setInterval(autoSlide, 3000);
// END SLIDE IMAGE MINIATURE CATEGORY
// SCRIPT JS PARTY GOOGLE MPAS 
    function initMap() {
        var sellerLocation = { lat: 48.8566, lng: 2.3522 }; // Coordinates for Paris
        var map = new google.maps.Map(document.getElementById('map'), {
            zoom: 14,
            center: sellerLocation
        });
        var marker = new google.maps.Marker({
            position: sellerLocation,
            map: map
        });
    }
    
    // PRODUCT FAVORITE PARTY 
      

// CAROUSEL IMAGE CATEGORIE DEFILEMENT HORIZONTAL

function scrollCarousel(direction) {
  const container = document.querySelector('.carousel-container');
  const scrollAmount = 200; // Ajustez la quantité de défilement si nécessaire
  container.scrollBy({
    left: direction * scrollAmount,
    behavior: 'smooth'
  });
}
