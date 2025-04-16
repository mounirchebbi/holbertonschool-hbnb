document.addEventListener('DOMContentLoaded', () => {
    // Mock data for places
    const places = [
        { id: 1, name: 'Cozy Cabin', price: 120, host: 'John Doe', description: 'A cozy cabin in the woods.', amenities: ['WiFi', 'Parking'] },
        { id: 2, name: 'Beach House', price: 200, host: 'Jane Smith', description: 'A luxurious beach house.', amenities: ['Pool', 'WiFi'] }
    ];

    // Mock reviews
    const reviews = [
        { placeId: 1, user: 'Alice', comment: 'Great stay!', rating: 5 },
        { placeId: 1, user: 'Bob', comment: 'Very cozy.', rating: 4 }
    ];

    // Mock authentication state
    let isLoggedIn = false;

    // Populate places list on index.html
    const placesList = document.getElementById('places-list');
    if (placesList) {
        places.forEach(place => {
            const placeCard = document.createElement('div');
            placeCard.className = 'place-card';
            placeCard.innerHTML = `
                <h3>${place.name}</h3>
                <p>$${place.price}/night</p>
                <a href="place.html?id=${place.id}" class="details-button">View Details</a>
            `;
            placesList.appendChild(placeCard);
        });
    }

    // Populate place details and reviews on place.html
    const placeDetails = document.getElementById('place-details');
    const reviewsContainer = document.getElementById('reviews');
    const addReviewSection = document.getElementById('add-review');
    if (placeDetails && reviewsContainer && addReviewSection) {
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = parseInt(urlParams.get('id'));
        const place = places.find(p => p.id === placeId);

        if (place) {
            placeDetails.querySelector('.place-info').innerHTML = `
                <h2>${place.name}</h2>
                <p>Host: ${place.host}</p>
                <p>Price: $${place.price}/night</p>
                <p>Description: ${place.description}</p>
                <p>Amenities: ${place.amenities.join(', ')}</p>
            `;
        }

        const placeReviews = reviews.filter(r => r.placeId === placeId);
        placeReviews.forEach(review => {
            const reviewCard = document.createElement('div');
            reviewCard.className = 'review-card';
            reviewCard.innerHTML = `
                <p>${review.comment}</p>
                <p>User: ${review.user}</p>
                <p class="rating">Rating: ${review.rating} Stars</p>
            `;
            reviewsContainer.appendChild(reviewCard);
        });

        // Show/hide add review form based on login status
        if (!isLoggedIn) {
            addReviewSection.innerHTML = '<p>Please <a href="login.html">log in</a> to add a review.</p>';
        }
    }

    // Handle login form submission
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault(); // Prevent default form submission

            // Get email and password from form inputs
            const email = loginForm.querySelector('#email').value;
            const password = loginForm.querySelector('#password').value;

            try {
                // Make AJAX request to login endpoint
                const response = await fetch('http://127.0.0.1:5000/api/v1/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                // Handle API response
                if (response.ok) {
                    const data = await response.json();
                    // Store JWT token in a cookie
                    document.cookie = `token=${data.access_token}; path=/; Secure; SameSite=Strict`;
                    isLoggedIn = true; // Update login state
                    window.location.href = 'index.html'; // Redirect to main page
                } else {
                    // Handle error response
                    const errorData = await response.json();
                    alert(`Login failed: ${errorData.error || 'Invalid credentials'}`);
                }
            } catch (error) {
                // Handle network or other errors
                alert('An error occurred during login. Please try again.');
                console.error('Login error:', error);
            }
        });
    }

    // Handle review form submission
    const reviewForm = document.getElementById('review-form');
    if (reviewForm) {
        reviewForm.addEventListener('submit', (e) => {
            e.preventDefault();
            if (!isLoggedIn) {
                alert('Please log in to submit a review.');
                window.location.href = 'login.html';
                return;
            }
            const reviewText = reviewForm.querySelector('#review, #review-text').value;
            const rating = reviewForm.querySelector('#rating').value;
            const placeId = reviewForm.querySelector('#place-id')?.value || new URLSearchParams(window.location.search).get('id');
            console.log('New Review:', { placeId, reviewText, rating });
            alert('Review submitted!');
            reviewForm.reset();
        });
    }

    // Handle price filter
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', (e) => {
            const maxPrice = parseInt(e.target.value) || Infinity;
            placesList.innerHTML = '';
            places
                .filter(place => place.price <= maxPrice)
                .forEach(place => {
                    const placeCard = document.createElement('div');
                    placeCard.className = 'place-card';
                    placeCard.innerHTML = `
                        <h3>${place.name}</h3>
                        <p>$${place.price}/night</p>
                        <a href="place.html?id=${place.id}" class="details-button">View Details</a>
                    `;
                    placesList.appendChild(placeCard);
                });
        });
    }
});
