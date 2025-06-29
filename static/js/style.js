
    // Get the button
    let mybutton = document.getElementById("myBtn");
    
    // When the user scrolls down 20px from the top of the document, show the button
    window.onscroll = function() {scrollFunction()};
    
    function scrollFunction() {
      if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
        mybutton.style.display = "block";
      } else {
        mybutton.style.display = "none";
      }
    }
    
    // When the user clicks on the button, scroll to the top of the document
    function topFunction() {
      document.body.scrollTop = 0;
      document.documentElement.scrollTop = 0;
    }
    
    
    document.addEventListener("DOMContentLoaded", function() {
      const articleButtons = document.querySelectorAll(".read-article-btn");
  
      articleButtons.forEach(button => {
          button.addEventListener("click", function(event) {
              event.preventDefault();
              const articleId = this.getAttribute("data-article-id");
  
              // Fetch article content via AJAX (Using Django URL pattern)
              fetch(`/get-article-content/${articleId}/`)
                  .then(response => response.json())
                  .then(data => {
                      // Update the Featured Article section with the clicked article's content
                      document.getElementById("featured-article-img").src = data.photo_url;
                      document.getElementById("featured-article-title").innerText = data.title;
                      document.getElementById("featured-article-text").innerText = data.truncated_content;
                      document.getElementById("featured-article-full-content").innerHTML = `<p>${data.full_content}</p>`;
                  })
                  .catch(error => console.error("Error fetching article content:", error));
          });
      });
  });
    
//tel
const input = document.querySelector("#telephone");
    window.intlTelInput(input, {
      initialCountry: "auto",
      geoIpLookup: function (callback) {
        fetch("https://ipapi.co/json")
          .then((res) => res.json())
          .then((data) => callback(data.country_code))
          .catch(() => callback("bf")); // fallback Burkina Faso
      },
      utilsScript:
        "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.19/js/utils.js",
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