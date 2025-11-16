CREATE TABLE cars (
    id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_family INTEGER NOT NULL,
    name VARCHAR(100) NOT NULL,
    CONSTRAINT fk_family
        FOREIGN KEY (id_family)
        REFERENCES families(id)
        ON DELETE CASCADE
);
