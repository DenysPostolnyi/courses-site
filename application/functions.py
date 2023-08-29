import json


def take_courses() -> dict:
    courses_data = {}
    with open("application/models/courses.json") as courses_file:
        courses_data = json.load(courses_file)
    return courses_data
