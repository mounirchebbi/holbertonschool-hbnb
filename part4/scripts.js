document.addEventListener('DOMContentLoaded', () => {
    // Mock authentication state
    let isLoggedIn = false;

    // Function to get JWT token from cookie
    function getToken() {
        const cookies = document.cookie.split(';').reduce((acc, cookie) => {
            const [key, value] = cookie.trim().split('=');
            acc[key] = value;
            return acc;
        }, {});
        return cookies.token || null;
    }

    // Function to fetch places from the API
    async function fetchPlaces() {
        try {
            const response = await fetch('http://127.0.0.1:5000/api/v1/places', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (!response.ok) {
                throw new Error('Failed to fetch places');
            }
            const places = await response.json();
            return places;
        } catch (error) {
            console.error('Error fetching places:', error);
            alert('Failed to load places. Please try again.');
            return [];
        }
    }

    // Function to fetch place details by ID
    async function fetchPlaceDetails(placeId) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (!response.ok) {
                throw new Error('Failed to fetch place details');
            }
            const place = await response.json();
            return place;
        } catch (error) {
            console.error('Error fetching place details:', error);
            return null;
        }
    }

    // Function to fetch reviews for a place by ID
    async function fetchPlaceReviews(placeId) {
        try {
            const response = await fetch(`http://127.0.0.1:5000/api/v1/places/${placeId}/reviews`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            if (!response.ok) {
                throw new Error('Failed to fetch reviews');
            }
            const reviews = await response.json();
            return reviews;
        } catch (error) {
            console.error('Error fetching reviews:', error);
            return [];
        }
    }

    // Function to render places with client-side price filtering
    function renderPlaces(places, maxPrice = Infinity) {
        const placesList = document.getElementById('places-list');
        if (!placesList) return;

        placesList.innerHTML = ''; // Clear existing content
        places
            .filter(place => place.price <= maxPrice)
            .forEach(place => {
                const placeCard = document.createElement('div');
                placeCard.className = 'place-card';
                placeCard.innerHTML = `
                    <h3>${place.title}</h3>
                    <p>$${place.price}/night</p>
                    <a href="place.html?id=${place.id}" class="details-button">View Details</a>
                `;
                placesList.appendChild(placeCard);
            });
    }

    // Function to render place details
    function renderPlaceDetails(place) {
        const placeDetails = document.getElementById('place-details');
        if (!placeDetails) return;

        const placeInfo = placeDetails.querySelector('.place-info');
        if (place) {
            placeInfo.innerHTML = `
                <h2>${place.title}</h2>
                <p>Host: ${place.owner.first_name} ${place.owner.last_name}</p>
                <p>Price: $${place.price}/night</p>
                <p>Description: ${place.description || 'No description available'}</p>
                <p>Amenities: ${place.amenities.length ? place.amenities.map(a => a.name).join(', ') : 'None'}</p>
            `;
        } else {
            placeInfo.innerHTML = '<p>Place not found.</p>';
        }
    }

    // Function to render reviews
    function renderReviews(reviews) {
        const reviewsContainer = document.getElementById('reviews');
        if (!reviewsContainer) return;

        reviewsContainer.innerHTML = ''; // Clear existing content
        if (reviews.length === 0) {
            reviewsContainer.innerHTML = '<p>No reviews yet.</p>';
            return;
        }
        reviews.forEach(review => {
            const reviewCard = document.createElement('div');
            reviewCard.className = 'review-card';
            reviewCard.innerHTML = `
                <p>${review.text}</p>
                <p>User: ${review.user_id}</p>
                <p class="rating">Rating: ${review.rating} Stars</p>
            `;
            reviewsContainer.appendChild(reviewCard);
        });
    }

    // Populate places list on index.html
    const placesList = document.getElementById('places-list');
    if (placesList) {
        fetchPlaces().then(places => {
            renderPlaces(places); // Initial render with all places
        });
    }

    // Populate place details and reviews on place.html
    const placeDetails = document.getElementById('place-details');
    const reviewsContainer = document.getElementById('reviews');
    const addReviewSection = document.getElementById('add-review');
    if (placeDetails && reviewsContainer && addReviewSection) {
        const urlParams = new URLSearchParams(window.location.search);
        const placeId = urlParams.get('id');

        if (placeId) {
            // Fetch and render place details
            fetchPlaceDetails(placeId).then(place => {
                renderPlaceDetails(place);
            });
            // Fetch and render reviews
            fetchPlaceReviews(placeId).then(reviews => {
                renderReviews(reviews);
            });
        } else {
            placeDetails.querySelector('.place-info').innerHTML = '<p>No place ID provided.</p>';
        }

        // Show/hide add review form based on login status
        if (!getToken()) {
            isLoggedIn = false;
            addReviewSection.innerHTML = '<p>Please <a href="login.html">log in</a> to add a review.</p>';
        } else {
            isLoggedIn = true;
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
        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (!isLoggedIn) {
                alert('Please log in to submit a review.');
                window.location.href = 'login.html';
                return;
            }
            const reviewText = reviewForm.querySelector('#review, #review-text').value;
            const rating = reviewForm.querySelector('#rating').value;
            const placeId = reviewForm.querySelector('#place-id')?.value || new URLSearchParams(window.location.search).get('id');

            try {
                const token = getToken();
                const response = await fetch(`http://127.0.0.1:5000/api/v1/reviews`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        text: reviewText,
                        rating: parseInt(rating),
                        place_id: placeId,
                        user_id: 'current_user_id' // Note: This should ideally be fetched from the JWT token
                    })
                });

                if (response.ok) {
                    alert('Review submitted!');
                    reviewForm.reset();
                    // Refresh reviews
                    fetchPlaceReviews(placeId).then(reviews => {
                        renderReviews(reviews);
                    });
                } else {
                    const errorData = await response.json();
                    alert(`Failed to submit review: ${errorData.error || 'Unknown error'}`);
                }
            } catch (error) {
                console.error('Error submitting review:', error);
                alert('An error occurred while submitting the review. Please try again.');
            }
        });
    }

    // Handle price filter
    const priceFilter = document.getElementById('price-filter');
    if (priceFilter) {
        priceFilter.addEventListener('change', async (e) => {
            const maxPrice = parseInt(e.target.value) || Infinity;
            const places = await fetchPlaces(); // Fetch fresh data
            renderPlaces(places, maxPrice); // Render with filter
        });
    }
});
