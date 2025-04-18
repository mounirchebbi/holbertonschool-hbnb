document.addEventListener('DOMContentLoaded', () => {
    // === Utility Functions ===
    // Extract JWT token from browser cookies
    function getToken() {
        const cookies = document.cookie.split(';').reduce((acc, cookie) => {
            const [key, value] = cookie.trim().split('=');
            acc[key] = value;
            return acc;
        }, {});
        return cookies.token || null;
    }

    // Decode JWT payload to extract user ID
    function getUserIdFromToken(token) {
        try {
            // JWT structure: header.payload.signature
            const payload = JSON.parse(atob(token.split('.')[1]));
            console.log('Decoded JWT payload:', payload);

            // Handle possible shapes of payload keys
            if (typeof payload.user_id === 'string') return payload.user_id;
            if (typeof payload.user_id === 'object' && payload.user_id.id) return payload.user_id.id;
            if (typeof payload.sub === 'string') return payload.sub;
            if (typeof payload.sub === 'object' && payload.sub.id) return payload.sub.id;

            console.warn('Could not find user ID in token payload:', payload);
            return null;
        } catch (e) {
            console.error('Failed to decode token:', e);
            return null;
        }
    }

    // Retrieve auth token and determine login state
    const token = getToken();
    const isLoggedIn = Boolean(token);

    // === Login/Logout Link Toggle ===
    const loginLink = document.getElementById('login-link');
    const logoutLink = document.getElementById('logout-link');

    // Show login or logout links based on auth state
    if (loginLink)  loginLink.style.display  = isLoggedIn ? 'none' : 'inline-block';
    if (logoutLink) logoutLink.style.display = isLoggedIn ? 'inline-block' : 'none';

    // Logout click handler: clear token and redirect to home
    if (logoutLink) {
        logoutLink.addEventListener('click', (e) => {
            e.preventDefault();
            document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
            window.location.href = 'index.html';
        });
    }

    // === Login Form Handling ===
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const email    = loginForm.querySelector('#email').value;
            const password = loginForm.querySelector('#password').value;

            try {
                // Send credentials to API
                const response = await fetch('http://127.0.0.1:5000/api/v1/login', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ email, password })
                });

                const data = await response.json();
                if (response.ok) {
                    // Save token in secure cookie and redirect
                    document.cookie = `token=${data.access_token}; path=/; Secure; SameSite=Strict`;
                    window.location.href = 'index.html';
                } else {
                    // Show error message
                    alert(`Login failed: ${data.error || 'Invalid credentials'}`);
                }
            } catch (err) {
                alert('Login error. Please try again.');
                console.error(err);
            }
        });
    }

    // === API Fetch Helpers ===
    // Fetch list of places
    async function fetchPlaces() {
        try {
            const res = await fetch('http://127.0.0.1:5000/api/v1/places');
            if (!res.ok) throw new Error('Failed to fetch places');
            return await res.json();
        } catch (err) {
            console.error(err);
            alert('Could not load places.');
            return [];
        }
    }

    // Fetch details for a single place by ID
    async function fetchPlaceDetails(id) {
        try {
            const res = await fetch(`http://127.0.0.1:5000/api/v1/places/${id}`);
            if (!res.ok) throw new Error('Failed to fetch place details');
            return await res.json();
        } catch (err) {
            console.error(err);
            return null;
        }
    }

    // Fetch reviews for a place
    async function fetchPlaceReviews(id) {
        try {
            const res = await fetch(`http://127.0.0.1:5000/api/v1/places/${id}/reviews`);
            if (!res.ok) throw new Error('Failed to fetch reviews');
            return await res.json();
        } catch (err) {
            console.error(err);
            return [];
        }
    }

    // === Rendering Helpers ===
    // Render a list of place cards, with optional price filter
    function renderPlaces(places, maxPrice = Infinity) {
        const container = document.getElementById('places-list');
        if (!container) return;

        container.innerHTML = '';
        places
            .filter(place => place.price <= maxPrice)
            .forEach(place => {
                const card = document.createElement('div');
                card.className = 'place-card';
                card.innerHTML = `
                    <h3>${place.title}</h3>
                    <p>$${place.price}/night</p>
                    <a href="place.html?id=${place.id}" class="details-button">View Details</a>
                `;
                container.appendChild(card);
            });
    }

    // Populate details section on place page
    function renderPlaceDetails(place) {
        const info = document.querySelector('#place-details .place-info');
        if (!info) return;

        if (!place) {
            info.innerHTML = '<p>Place not found.</p>';
        } else {
            info.innerHTML = `
                <h2>${place.title}</h2>
                <p>Host: ${place.owner.first_name} ${place.owner.last_name}</p>
                <p>Price: $${place.price}/night</p>
                <p>Description: ${place.description || 'No description available'}</p>
                <p>Amenities: ${place.amenities.map(a => a.name).join(', ') || 'None'}</p>
            `;
        }
    }

    // Fetch a user's name by user ID
    async function fetchUserName(userId) {
        try {
            const res = await fetch(`http://127.0.0.1:5000/api/v1/users/${userId}`);
            if (!res.ok) throw new Error('Failed to fetch user name');
            const data = await res.json();
            return `${data.first_name} ${data.last_name}`;
        } catch (err) {
            console.error(`Error fetching name for user ${userId}:`, err);
            return 'Unknown';
        }
    }

    // Render reviews with user names and ratings
    async function renderReviews(reviews) {
        const reviewsContainer = document.getElementById('reviews');
        if (!reviewsContainer) return;

        reviewsContainer.innerHTML = '';
        if (reviews.length === 0) {
            reviewsContainer.innerHTML = '<p>No reviews yet.</p>';
            return;
        }

        for (const review of reviews) {
            const userName = await fetchUserName(review.user_id);

            const reviewCard = document.createElement('div');
            reviewCard.className = 'review-card';
            reviewCard.innerHTML = `
                <p>Posted by: ${userName}</p>
                <p>Review: "${review.text}"</p>
                <p class="rating">Rating: ${review.rating} Stars</p>
            `;
            reviewsContainer.appendChild(reviewCard);
        }
    }

    // === Initialize Index Page ===
    const placesList           = document.getElementById('places-list');
    const priceFilter          = document.getElementById('price-filter');

    // Load and display all places on page load
    if (placesList) {
        fetchPlaces().then(renderPlaces);
    }

    // Update list when price filter changes
    if (priceFilter) {
        priceFilter.addEventListener('change', async (e) => {
            const maxPrice = parseInt(e.target.value) || Infinity;
            const places   = await fetchPlaces();
            renderPlaces(places, maxPrice);
        });
    }

    // === Initialize Place Details & Reviews Page ===
    const placeIdFromUrl  = new URLSearchParams(window.location.search).get('id');
    const placeIdInput    = document.getElementById('place-id');
    const placeDetails    = document.getElementById('place-details');
    const reviewsContainer= document.getElementById('reviews');
    const addReviewSection= document.getElementById('add-review');

    // Pre-fill hidden place ID input if present
    if (placeIdInput && placeIdFromUrl) {
        placeIdInput.value = placeIdFromUrl;
    }

    // Load details and reviews for this place, toggle review form
    if (placeDetails && reviewsContainer && placeIdFromUrl) {
        fetchPlaceDetails(placeIdFromUrl).then(renderPlaceDetails);
        fetchPlaceReviews (placeIdFromUrl).then(renderReviews);
        if (addReviewSection) {
            addReviewSection.style.display = isLoggedIn ? 'block' : 'none';
        }
    }

    // === Review Form Submission Handling ===
    const reviewForm    = document.getElementById('review-form');
    const reviewTextArea= document.getElementById('review');
    const ratingSelect  = document.getElementById('rating');

    // Only show or process form if user is authenticated
    if (reviewForm && reviewTextArea && ratingSelect && placeIdInput) {
        if (!token) {
            // Redirect unauthenticated users away from add_review page
            const fromAddReview = window.location.pathname.includes('add_review.html');
            if (fromAddReview) window.location.href = 'index.html';
            else if (addReviewSection) addReviewSection.style.display = 'none';
            return;
        }

        reviewForm.addEventListener('submit', async (e) => {
            e.preventDefault();

            // Gather form data
            const text    = reviewTextArea.value.trim();
            const rating  = parseInt(ratingSelect.value);
            const placeId = placeIdInput.value;
            const userId  = getUserIdFromToken(token);

            console.log('Form values:', { text, rating, placeId, userId });

            // Validate inputs before sending
            if (!text || !rating || !placeId || !userId) {
                alert('Please fill out all fields.');
                return;
            }

            try {
                // Send review to API
                const response = await fetch('http://127.0.0.1:5000/api/v1/reviews', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({ text, rating, place_id: placeId, user_id: userId })
                });

                const raw  = await response.text();
                let data;
                try {
                    data = JSON.parse(raw);
                } catch {
                    console.error('Invalid JSON response:', raw);
                    alert('Unexpected server response.');
                    return;
                }

                if (response.ok) {
                    alert('Review submitted successfully!');
                    reviewForm.reset();
                    // Refresh reviews list
                    if (placeId) fetchPlaceReviews(placeId).then(renderReviews);
                } else {
                    console.error('Review error:', data);
                    alert(data.error || 'Failed to submit review.');
                }
            } catch (err) {
                console.error('Review submission error:', err);
                alert('An error occurred while submitting the review.');
            }
        });
    }
});
