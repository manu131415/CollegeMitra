SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'institutes';

ALTER TABLE institutes
ALTER COLUMN nirf_rank TYPE VARCHAR(20)
USING nirf_rank::VARCHAR;

COPY institutes(
    institute_name,
    latitude,
    longitude,
    state,
    nirf_rank,
    annual_fees,
    median_package_lpa,
    type
)
FROM 'D:/ASUS/Desktop/Manu/CollegeMitra/CollegeMitra/database/processed/institutes.csv'
DELIMITER ','
CSV HEADER;

SELECT COUNT(*) FROM institutes;
SELECT * FROM institutes LIMIT 5;


COPY programs(program_name)
FROM 'D:/ASUS/Desktop/Manu/CollegeMitra/CollegeMitra/database/processed/programs.csv'
DELIMITER ','
CSV HEADER;

SELECT COUNT(*) FROM programs;
SELECT * FROM programs LIMIT 5;

COPY raw_jossa(
    year, 
	round,
	institute_name,
    academic_program_name,
    quota,
    seat_type,
    gender,
    opening_rank,
    closing_rank   
)
FROM 'D:/ASUS/Desktop/Manu/CollegeMitra/CollegeMitra/database/processed/josaa_ranks.csv'
DELIMITER ','
CSV HEADER;

Select * from raw_jossa limit 5;

COPY raw_csab(
    year, 
	special_round,
	institute_name,
    academic_program_name,
    quota,
    seat_type,
    gender,
    opening_rank,
    closing_rank   
)
FROM 'D:/ASUS/Desktop/Manu/CollegeMitra/CollegeMitra/database/processed/csab_ranks.csv'
DELIMITER ','
CSV HEADER;

select * from raw_csab limit 5;

SELECT COUNT(*)
FROM raw_jossa r
JOIN institutes i
    ON r.institute_name = i.institute_name
JOIN programs p
    ON r.academic_program_name = p.program_name;

SELECT COUNT(*) FROM raw_jossa;

INSERT INTO jossa_ranks (
    year,
    round,
    institute_id,
    program_id,
    quota,
    seat_type,
    gender,
    opening_rank,
    closing_rank
)
SELECT
    r.year,
    r.round,
    i.institute_id,
    p.program_id,
    r.quota,
    r.seat_type,
    r.gender,
    NULLIF(REGEXP_REPLACE(r.opening_rank, '[^0-9]', '', 'g'), '')::INTEGER,
    NULLIF(REGEXP_REPLACE(r.closing_rank, '[^0-9]', '', 'g'), '')::INTEGER
FROM raw_jossa r
JOIN institutes i
    ON r.institute_name = i.institute_name
JOIN programs p
    ON r.academic_program_name = p.program_name;


select * from jossa_ranks limit 10;

select institute_name from institutes where institute_id = 57;
select program_name from programs where program_id = 159;



INSERT INTO csab_ranks (
    year,
    special_round,
    institute_id,
    program_id,
    quota,
    seat_type,
    gender,
    opening_rank,
    closing_rank
)
SELECT
    r.year,
    r.special_round,
    i.institute_id,
    p.program_id,
    r.quota,
    r.seat_type,
    r.gender,
    NULLIF(REGEXP_REPLACE(r.opening_rank, '[^0-9]', '', 'g'), '')::INTEGER,
    NULLIF(REGEXP_REPLACE(r.closing_rank, '[^0-9]', '', 'g'), '')::INTEGER
FROM raw_csab r
JOIN institutes i
    ON r.institute_name = i.institute_name
JOIN programs p
    ON r.academic_program_name = p.program_name;


select * from csab_ranks limit 10;

select institute_name from institutes where institute_id = 15;
select program_name from programs where program_id = 111;