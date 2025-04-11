-- Insert Administrator User
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$wegd.CgSrv5JHcswj62Gmu9fdjxK/gYYxzFJTbBm9cmOkOHH36Ole',
    TRUE
);

-- Insert Initial Amenities
INSERT INTO amenities (id, name)
VALUES
    ('a1b2c3d4-e5f6-7890-abcd-1234567890ef', 'WiFi'),
    ('b2c3d4e5-f6a7-8901-bcde-2345678901fa', 'Swimming Pool'),
    ('c3d4e5f6-a7b8-9012-cdef-3456789012ab', 'Air Conditioning');
