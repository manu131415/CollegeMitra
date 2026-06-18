CREATE TABLE institutes (
    institute_id SERIAL PRIMARY KEY,
    institute_name TEXT NOT NULL UNIQUE,
    type VARCHAR(50),
    state VARCHAR(100),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    nirf_rank INTEGER,
    annual_fees NUMERIC(12,2),
    median_package_lpa NUMERIC(8,2)
);

CREATE TABLE programs (
    program_id SERIAL PRIMARY KEY,
    program_name TEXT NOT NULL UNIQUE
);

CREATE TABLE jossa_ranks (
    rank_id BIGSERIAL PRIMARY KEY,
    year SMALLINT NOT NULL,
    round SMALLINT NOT NULL,
    institute_id INTEGER NOT NULL,
    program_id INTEGER NOT NULL,
    quota TEXT,
    seat_type TEXT,
    gender TEXT,
    opening_rank INTEGER,
    closing_rank INTEGER,
    CONSTRAINT fk_jossa_institute
        FOREIGN KEY (institute_id)
        REFERENCES institutes(institute_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_jossa_program
        FOREIGN KEY (program_id)
        REFERENCES programs(program_id)
        ON DELETE CASCADE
);

CREATE TABLE csab_ranks (
    rank_id BIGSERIAL PRIMARY KEY,
    year SMALLINT NOT NULL,
    special_round SMALLINT NOT NULL,
    institute_id INTEGER NOT NULL,
    program_id INTEGER NOT NULL,
    quota TEXT,
    seat_type TEXT,
    gender TEXT,
    opening_rank INTEGER,
    closing_rank INTEGER,
    CONSTRAINT fk_csab_institute
        FOREIGN KEY (institute_id)
        REFERENCES institutes(institute_id)
        ON DELETE CASCADE,
    CONSTRAINT fk_csab_program
        FOREIGN KEY (program_id)
        REFERENCES programs(program_id)
        ON DELETE CASCADE
);

CREATE TABLE raw_jossa (
    year SMALLINT,
    round SMALLINT,
    institute_name TEXT,
    academic_program_name TEXT,
    quota TEXT,
    seat_type TEXT,
    gender TEXT,
    opening_rank TEXT,
    closing_rank TEXT
);


CREATE TABLE raw_csab (
    institute_name TEXT,
    academic_program_name TEXT,
    quota TEXT,
    seat_type TEXT,
    gender TEXT,
    opening_rank TEXT,
    closing_rank TEXT,
    year SMALLINT,
    special_round SMALLINT
);