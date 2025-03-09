users_data = [
    ('prof_cs', 'professor', 'Dr. S Saroja'),
    ('prof_civil', 'professor', 'Dr. Mashuda Sultana'),
    ('prof_energy', 'professor', 'Dr. Ruben Sudhakar'),
    ('prof_thermo', 'professor', 'Dr. S. Anand'),
    ('prof_physics', 'professor', 'Dr. Sujatha Srinivasan'),
    ('prof_math', 'professor', 'Dr. Radha Krishnan'),
    ('class_rep1', 'class_rep', 'Class Representative 1'),
] + [
    (f'student_{roll_no}', 'student', f'Student {roll_no}')
    for roll_no in range(112124001, 112124080)
]

subjects_data = [
    ('CS Class', 'prof_cs'),
    ('Civil', 'prof_civil'),
    ('Energy and Environment', 'prof_energy'),
    ('Thermodynamic', 'prof_thermo'),
    ('Physics', 'prof_physics'),
    ('Mathematics', 'prof_math'),
]
