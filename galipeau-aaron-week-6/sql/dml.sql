-- galipeau dml.sql

-- Insert initial data into TEACHER table
INSERT INTO TEACHER (first_name, last_name, email_address)
VALUES 
    ('Merlin', 'Ambrosius', 'merlin.ambrosius@bhms.edu'),
    ('Mrs.', 'Beauregard', 'mrs.beauregard@bhms.edu'),
    ('Yoda', 'Dagobah', 'yoda.dagobah@bhms.edu');

-- Insert initial data into STUDENT table
INSERT INTO STUDENT (first_name, last_name, email_address, date_of_birth, student_grade)
VALUES 
    ('Eric', 'Neptune', 'eric.neptune@bhms.edu', '2012-04-15', 6),
    ('Aurora', 'Dawn', 'aurora.dawn@bhms.edu', '2012-01-12', 6),
    ('Moana', 'Waialiki', 'moana.waialiki@bhms.edu', '2012-01-20', 6),
    ('Cinderella', 'Hawkins', 'cinderella.hawkins@bhms.edu', '2011-11-02', 7),
    ('Lionel', 'Hawkins', 'lionel.hawkins@bhms.edu', '2011-03-22', 7),
    ('Ariel', 'Triton', 'ariel.triton@bhms.edu', '2011-10-23', 7),
    ('Elsa', 'Arendelle', 'elsa.arendelle@bhms.edu', '2010-12-21', 8),
    ('Belle', 'Beaumont', 'belle.beaumont@bhms.edu', '2010-05-12', 8),
    ('Simba', 'Lionheart', 'simba.lionheart@bhms.edu', '2010-09-14', 8);

-- Insert initial data into CLASSES table
INSERT INTO CLASSES (class_subject, teacher_id)
VALUES 
    ('Math', 1), -- Merlin teaches Math
    ('Social Studies', 2), -- Mrs. Beauregard teaches Social Studies
    ('Homeroom', 3), -- Yoda teaches Homeroom
    ('Physical Education', 1), -- Merlin also teaches Physical Education
    ('Science', 2), -- Mrs. Beauregard teaches Science
    ('History', 3); -- Yoda teaches History

-- Insert initial data into STUDENT_CLASSES table to establish relationships
INSERT INTO STUDENT_CLASSES (student_id, class_id, class_grade)
VALUES 
    (1, 1, 'A'), -- Eric is in Math with Merlin
    (2, 1, 'B'), -- Aurora is in Math with Merlin
    (3, 1, 'A'), -- Moana is in Math with Merlin

    (1, 2, 'B'), -- Eric is in Social Studies with Mrs. Beauregard
    (2, 2, 'A'), -- Aurora is in Social Studies with Mrs. Beauregard
    (3, 2, 'C'), -- Moana is in Social Studies with Mrs. Beauregard

    (4, 3, 'A'), -- Cinderella is in Homeroom with Yoda
    (5, 3, 'A'), -- Lionel is in Homeroom with Yoda
    (6, 3, 'A'), -- Ariel is in Homeroom with Yoda

    (4, 4, 'A'), -- Cinderella is in Physical Education with Merlin
    (5, 4, 'A'), -- Lionel is in Physical Education with Merlin
    (6, 4, 'A'), -- Ariel is in Physical Education with Merlin

    (7, 5, 'B'), -- Elsa is in Science with Mrs. Beauregard
    (8, 5, 'B'), -- Belle is in Science with Mrs. Beauregard
    (9, 5, 'B'), -- Simba is in Science with Mrs. Beauregard

    (1, 6, 'A'), -- Eric is in History with Yoda
    (2, 6, 'A'), -- Aurora is in History with Yoda
    (3, 6, 'A'), -- Moana is in History with Yoda

    (7, 3, 'C'), -- Elsa is in Homeroom with Yoda
    (8, 3, 'B'), -- Belle is in Homeroom with Yoda
    (9, 3, 'D'); -- Simba is in Homeroom with Yoda
