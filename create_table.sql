-- since the name, url_key and description are too long, use TEXT type
CREATE TABLE products (
    id BIGINT PRIMARY KEY,
    name TEXT,
    url_key TEXT,
    price BIGINT,
    description TEXT,
    images TEXT[] -- store many image urls with array
);
