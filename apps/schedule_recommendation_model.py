import os
import pandas as pd
import numpy as np
import random
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor

project_path = os.getenv('PROJECT_PATH')

directory = os.path.join(project_path, 'apps')

file_path = os.path.join(directory, 'STD.csv')

# Load data
data = pd.read_csv(file_path)
data['COURSE_ID'] = data['COURSE_ID'].astype(str).str.strip()
data['AVG'].fillna(data['AVG'].mean(), inplace=True)

# General and specific courses details
general_courses = {
    '11100': 'Computer Skills (Remedial)',
    '11102': 'Introduction to Computer Science',
    '11103': 'Structured Programming',
    '11151': 'Structured Programming Lab',
    '11206': 'Object Oriented Programming',
    '11212': 'Data Structures and Introduction to Algorithms',
    '11253': 'Object Oriented Programming Lab',
    '11313': 'Algorithms Design and Analysis',
    '11316': 'Theory of Computation',
    '11323': 'Database Systems',
    '11335': 'Operating Systems',
    '11343': 'JAVA',
    '11344': 'Advanced Topics in Internet Programming',
    '11347': 'Electronic Business',
    '11354': 'Database Systems Lab',
    '11355': 'Operating Systems Lab',
    '11391': 'Practical Training',
    '11425': 'Software Engineering',
    '11428': 'Artificial Intelligence',
    '11435': 'Data Communications & Computer Networks',
    '11436': 'Distributed Systems',
    '11447': 'Wireless Networks and Applications',
    '11449': 'Computer and Society',
    '11464': 'Information Systems Security',
    '11493': 'Graduation Project 1',
    '11494': 'Graduation Project 2',
    '12242': 'Webpage Design and Internet Programming LAB',
    '12243': 'Webpage Design and Internet Programming',
    '12258': 'Computer Applications in Fine Arts',
    '12273': 'Computer Graphics',
    '12324': 'Human Computer Interaction',
    '12343': 'Visual Programming',
    '12348': 'Multimedia Systems',
    '12446': 'Digital Image Processing',
    '13324': 'Systems Analysis and Design',
    '13334': 'Mobile Application Development',
    '13432': 'Software Project Management',
    '20100': 'Calculus (Remedial)',
    '20132': 'Calculus (1)',
    '20133': 'Calculus (2)',
    '20134': 'Discrete Mathematics',
    '20135': 'Discrete Mathematics (2)',
    '20141': 'Physics (1)',
    '20142': 'Physics (2)',
    '20147': 'Physics Lab',
    '20148': 'Physics (1) Lab',
    '20149': 'Physics (2) Lab',
    '20200': 'Technical Writing and Communication Skills',
    '20231': 'Calculus (3)',
    '20232': 'Engineering Mathematics (1)',
    '20233': 'Statistical Methods',
    '20234': 'Linear Algebra',
    '20251': 'History of Science',
    '20252': 'Arab Islamic Scientific Heritage',
    '20332': 'Operations Research',
    '20333': 'Numerical Analysis',
    '20325': 'Project Management',
    '20336': 'Principles of Probability',
    '21218': 'Engineering Drawing Lab',
    '21232': 'Digital Electronics Fundamentals',
    '22241': 'Digital Logic Design',
    '22342': 'Computer Organization and Assembly Language',
    '22348': 'Digital Logic Lab',
    '22444': 'Computer Architecture & Organization (1)',
    '22541': 'Computer Architecture',
    '24223': 'Electric Circuits',
    '25446': 'Network Protocols',
    '31010': 'Arabic Language placement test',
    '31019': 'Arabic Language (Remedial)',
    '31020': 'English placement test',
    '31029': 'English Language (Remedial)',
    '31111': 'Arabic Language',
    '31121': 'English Language',
    '31130': 'Foreign Languages',
    '31151': 'National Education',
    '31152': 'Arabic Islamic Civilization',
    '31153': 'Introduction to Society, Technology and Environment Protection',
    '31161': 'Introduction to Library Science',
    '31211': 'Arabic literature',
    '31251': 'Military Science',
    '31252': 'Governance and Development',
    '31255': 'Entrepreneurship for Business',
    '31261': 'Introduction to Politics and Economic Science',
    '31262': 'Introduction to Educational Science',
    '31263': 'Technical Writing Communication Skills',
    '31271': 'Environmental Science',
    '31311': 'Scientific Research Methods',
    '31351': 'Contemporary Issues in the Arab World',
    '31352': 'Jerusalem: History and Facts',
    '31361': 'Introduction to Philosophy',
    '31371': 'Health Education',
    '31372': 'Business Skills',
    '33212': 'Operations Research for Business'
}

courses = {key: {"credits": 3, "prerequisites": []} for key in general_courses.keys()}
courses.update({
    "20132": {"credits": 3, "prerequisites": []},  # Calculus (1)
    "20133": {"credits": 3, "prerequisites": ["20132"]},  # Calculus (2)
    "20134": {"credits": 3, "prerequisites": []},  # Discrete Mathematics
    "20135": {"credits": 3, "prerequisites": ["20134"]},  # Discrete Math (2)
    "20141": {"credits": 3, "prerequisites": []},  # Physics (1)
    "20142": {"credits": 3, "prerequisites": ["20141"]},  # Physics (2)
    "20325": {"credits": 3, "prerequisites": []},  # Project Management (Requires 80 credit hours)
    "20332": {"credits": 3, "prerequisites": ["20133"]},  # Operations Research
    "20333": {"credits": 3, "prerequisites": ["20133", "20234"]},  # Numerical Analysis
    "31010": {"credits": 0, "prerequisites": []},  # Arabic Language placement test
    "31019": {"credits": 0, "prerequisites": []},  # Arabic Language (Remedial)
    "31020": {"credits": 0, "prerequisites": []},  # English placement test
    "31029": {"credits": 0, "prerequisites": []},  # English Language (Remedial)
    "31111": {"credits": 3, "prerequisites": ["31019"]},  # Arabic Language
    "31152": {"credits": 3, "prerequisites": []},  # Arabic and Islamic Civilization
    "31161": {"credits": 3, "prerequisites": []},  # Introduction to Library Science
    "31171": {"credits": 3, "prerequisites": []},  # History of Science
    "31211": {"credits": 3, "prerequisites": ["31111"]},  # Arabic literature
    "31251": {"credits": 3, "prerequisites": []},  # Military Science (For Jordanians only)
    "31261": {"credits": 3, "prerequisites": []},  # Introduction of politics and economy
    "31262": {"credits": 3, "prerequisites": []},  # Introduction to Educational Science
    "31263": {"credits": 3, "prerequisites": ["31111", "31121"]},  # Technical Writing Communication Skills
    "31271": {"credits": 3, "prerequisites": []},  # Environmental Science
    "31351": {"credits": 3, "prerequisites": []},  # Current Issues in the Arab World
    "31352": {"credits": 3, "prerequisites": []},  # Al-Quds History and Facts
    "31361": {"credits": 3, "prerequisites": []},  # Introduction to Psychology
    "31371": {"credits": 3, "prerequisites": []},  # Health education
    "31372": {"credits": 3, "prerequisites": []},  # Business skills (Requires 60 credit hours)
})


# Function to check prerequisites
def check_prerequisites(student_courses, course_id):
    prerequisites = courses[course_id]['prerequisites']
    if not prerequisites:
        return True
    return all(prereq in student_courses for prereq in prerequisites)


# Calculate GPA based on courses taken
def calculate_gpa(student_courses):
    total_credits = 0
    total_points = 0
    for course_id, grade in student_courses.items():
        if course_id in courses:
            credits = courses[course_id]['credits']
            total_credits += credits
            total_points += grade * credits
    return total_points / total_credits if total_credits else 0


# Aggregate data and calculate GPA for each student
student_data = data.groupby('STD_NO').apply(lambda df: {
    'courses_taken': df.set_index('COURSE_ID')['AVG'].to_dict(),
    'GPA': calculate_gpa(df.set_index('COURSE_ID')['AVG'].to_dict())
}).to_dict()


# Recommend courses and predict grades
def recommend_and_predict_grades(student_id, num_recommendations=5):
    eligible_courses = []
    student_info = student_data.get(student_id)
    for course_id in courses:
        if course_id not in student_info['courses_taken'] and check_prerequisites(student_info['courses_taken'],
                                                                                  course_id):
            eligible_courses.append(course_id)

    recommended_courses = random.sample(eligible_courses, min(len(eligible_courses), num_recommendations))
    recommended_course_names = [general_courses[course_id] for course_id in recommended_courses]
    grades_predictions = {}

    for course_id in recommended_courses:
        course_data = data[data['COURSE_ID'] != course_id]
        X = course_data[['AVG']]  # Ideally, add more features here
        y = course_data['AVG']

        if X.empty or y.empty:
            grades_predictions[general_courses[course_id]] = 'Insufficient data'
            continue

        imputer = SimpleImputer(strategy='mean')
        scaler = StandardScaler()
        X_imputed = imputer.fit_transform(X)
        X_scaled = scaler.fit_transform(X_imputed)
        model = RandomForestRegressor(n_estimators=100)  # More complex model
        model.fit(X_scaled, y)

        student_features = np.array([student_info['GPA']])  # Use more student-specific features if available
        student_features_imputed = imputer.transform([student_features])
        student_features_scaled = scaler.transform(student_features_imputed)
        predicted_grade = model.predict(student_features_scaled)[0]
        grades_predictions[course_id] = predicted_grade

    return grades_predictions
