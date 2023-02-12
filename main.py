import requests, os
# Main Method, runs code
def main():
    auth_token = os.environ["auth_token"]
    course_id = os.environ["course_id"]

    headers = {
        "Authorization": f"Bearer {auth_token}"
    }
    url = f'https://bcourses.berkeley.edu/api/v1/courses/{course_id}'
    print(headers, url)
    disc_topics = get_discussion_topics(url, headers)
    print(disc_topics)
    result_disc_yes = []
    for topic in (disc_topics):
        print(topic)
        result_disc_yes.append(yes_counter(topic, url, headers))
    print(result_disc_yes)


# Returns a list of discussion topics. Hardcoded right now to be only useful for the berkeley fiction bcourses discussion page.
def get_discussion_topics(url, headers):
    return(requests.get(f'{url}/discussion_topics?scope=unlocked', headers=headers).json())

# Returns a dictionary for yes, no counters for the specific discussion topic
def yes_counter(topic, url, headers):
    topic_id = topic["id"]
    entries = requests.get(f'{url}/discussion_topics/{topic_id}/entries', headers=headers).json()
    yes_counter = 0
    no_counter = 0
    result_counter = {}
    for e in entries:
        message = e["message"]
        first_word = ""
        for i in range(len(message)):
            if i != " ":
                first_word += i
            else:
                break
        
        if first_word == "YES" or first_word == "yes" or first_word == "Yes":
            yes_counter += 1
        elif first_word == "NO" or first_word == "no" or first_word == "No":
            no_counter += 1
    result_counter["topic"] = topic;
    result_counter["yes"] = yes_counter;
    result_counter["no"] = no_counter;
    return result_counter;
    
# Runs main method.
main()





