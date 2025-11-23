CREATE TABLE user_access (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES user_info(id),
    family_id INTEGER NOT NULL REFERENCES families(id)
);