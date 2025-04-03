INSERT INTO users (id, first_name, last_name, email, password, is_admin) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$5z5z5z5z5z5z5z5z5z5z5u5z5z5z5z5z5z5z5z5z5z5z5z5z5z5z5', -- Replace with your hash
    TRUE
);

INSERT INTO amenities (id, name) VALUES
    ('a1b2c3d4-e5f6-4g7h-8i9j-0k1l2m3n4o5p', 'WiFi'),
    ('b2c3d4e5-f6g7-4h8i-9j0k-l1m2n3o4p5q', 'Swimming Pool'),
    ('c3d4e5f6-g7h8-4i9j-0k1l-m2n3o4p5q6r', 'Air Conditioning');
