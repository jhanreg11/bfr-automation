import requests, os

auth_token = os.environ["auth_token"]
course_id = os.environ["course_id"]

headers = {
    "Authorization": f"Bearer {auth_token}"
}
url = f'https://bcourses.berkeley.edu/api/v1/courses/{course_id}'
print(headers, url)

print(requests.get(f'{url}/discussion_topics', headers=headers).json())

