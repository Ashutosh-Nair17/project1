CREATE TABLE users (
  id SERIAL PRIMARY KEY,	
  email VARCHAR NOT NULL,
  password VARCHAR NOT NULL
);


CREATE TABLE books (
    id SERIAL PRIMARY KEY,
    isbn INTEGER NOT NULL,
    title VARCHAR NOT NULL,
    author INTEGER NOT NULL,
    year INTEGER NOT NULL
);


CREATE TABLE reviews(
id SERIAL PRIMARY KEY,
books_id INTEGER,
rating INTEGER NOT NULL,
review VARCHAR(250) NOT NULL,
FOREIGN KEY (books_id) REFERENCES books (id)
);





CREATE TABLE user_reviews(
user_id INTEGER,
review_id INTEGER,
FOREIGN KEY(user_id) REFERENCES users (id),
FOREIGN KEY(review_id) REFERENCES reviews(id)
);
