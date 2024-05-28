import os
import pandas as pd

project_path = os.getenv('PROJECT_PATH')

directory = os.path.join(project_path, 'apps')

std_csv = os.path.join(directory, 'STD.csv')

web_development_courses_csv = os.path.join(directory, 'web_development_courses.csv')

# Load the datasets
udemy_courses = pd.read_csv(web_development_courses_csv)
students = pd.read_csv(std_csv)

# Ensure price is a string first
udemy_courses['price'] = udemy_courses['price'].astype(str)

# Replace 'Free' with '0' and remove '$'
udemy_courses['price'] = udemy_courses['price'].str.replace('Free', '0')
udemy_courses['price'] = udemy_courses['price'].str.replace('$', '')

# Convert price to numeric
udemy_courses['price'] = pd.to_numeric(udemy_courses['price'], errors='coerce')


def recommend_courses_for_student(student_id):
    student = students[students['STD_NO'] == int(student_id)]
    if not student.empty:
        student_gpa = student.iloc[0]['AVG']
        if student_gpa >= 76:
            recommended_courses = udemy_courses[(udemy_courses['level'] == 'Intermediate') |
                                                (udemy_courses['level'] == 'Expert')]
        else:
            recommended_courses = udemy_courses[udemy_courses['level'] == 'Beginner']

        # Add 'All Levels' conditionally
        all_levels_courses = udemy_courses[udemy_courses['level'] == 'All Levels']
        recommended_courses = pd.concat([recommended_courses, all_levels_courses]).drop_duplicates()

        # Sort by price descending (higher priced courses first), then by content duration
        recommended_courses = recommended_courses.sort_values(
            by=['price', 'content_duration'],
            ascending=[False, False]
        ).head(10)
        recommended_courses.set_index('course_id', inplace=True)
        return recommended_courses[
            ['course_title', 'url', 'is_paid', 'price', 'level', 'content_duration', 'course_image']
        ].to_dict(orient='index')
    else:
        raise Exception('Student not found')
