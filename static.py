USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"

HEADERS = {
    "user-agent": USER_AGENT
}


def lesson_headers(lesson):
    headers = {
        "user-agent": USER_AGENT,
        "referer": lesson,
    }
    return headers


def course_headers(course, csrf):
    headers = {
        "user-agent": USER_AGENT,
        "referer": f"https://stepik.org/edit-course-permissions/{course}",
        "x-csrftoken": csrf,
        "xrequestedwith": "XMLHttpRequest",
        "content-type": "application/json; charset=UTF-8",
    }
    return headers


def login_headers(csrf, email):
    headers = {
        "user-agent": USER_AGENT,
        "x-csrftoken": csrf,
        "x-requested-with": "XMLHttpRequest",
        "referer": f"https://stepik.org/login"
    }
    return headers
