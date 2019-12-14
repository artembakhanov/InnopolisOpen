import json
import sys

import requests as rq
from bs4 import BeautifulSoup as bs

from config import LOGIN, PASSWORD
from static import *

cookies = None
with open("lesson.txt") as f:
    lessons = f.read().split("\n")

with open("course.txt") as f:
    courses = f.read().split("\n")


def login():
    """
    Login on stepik.org.
    :return:
    """
    global cookies
    a = rq.get("https://stepik.org/login", headers=HEADERS)  # getting csrf token
    a = rq.post("https://stepik.org/api/users/login", data={"email": LOGIN, "password": PASSWORD},
                headers=login_headers(a.cookies.get("csrftoken"), LOGIN),
                cookies=a.cookies)
    cookies = a.cookies


def test():
    a = rq.get("https://stepik.org/lesson/289183/permissions/", cookies=cookies, headers=HEADERS)
    middle_csrf = bs(a.text).select_one("input[name=\"csrfmiddlewaretoken\"]")["value"]
    a = rq.post("https://stepik.org/lesson/289183/permissions/", cookies=cookies,
                headers=lesson_headers("https://stepik.org/lesson/289183/permissions/"), data={
            "can_anyone_learn": "on",
            "save_access_settings": "Save access settings",
            "csrfmiddlewaretoken": middle_csrf,
        })
    return a.text


def set_lessons_visibility(visible):
    for lesson in lessons:
        a = rq.get(f"{lesson}permissions/", cookies=cookies, headers=HEADERS)
        middle_csrf = bs(a.text, features="html.parser").select_one("input[name=\"csrfmiddlewaretoken\"]")["value"]
        a = rq.post(f"{lesson}permissions/", cookies=cookies,
                    headers=lesson_headers(lesson), data={
                "can_anyone_learn": "on" if visible else None,
                "save_access_settings": "Save access settings",
                "csrfmiddlewaretoken": middle_csrf,
            })


def set_courses_visibility(visible):
    for course in courses:
        a = rq.get(f"https://stepik.org/api/courses/{course}",
                   headers=course_headers(course, cookies.get("csrftoken")),
                   cookies=cookies)
        course_info = json.loads(a.text)['courses'][0]
        course_info['is_public'] = visible
        course_info['is_enabled'] = visible
        a = rq.put(f"https://stepik.org/api/courses/{course}",
                   headers=course_headers(course, cookies.get("csrftoken")),
                   data=json.dumps({"course": course_info}),
                   cookies=cookies)
        print(a.text)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        visible = bool(sys.argv[1])
        login()
        set_lessons_visibility(visible)
        set_courses_visibility(visible)
