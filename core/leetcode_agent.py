import requests
import json
import os
import random

LOG_PATH = os.path.join("data", "leetcode_log.json")



def fetch_recent_ac_problems(username, limit=15):
    url = "https://leetcode.com/graphql"

    query = """
    query recentAcSubmissions($username: String!, $limit: Int!) {
      recentAcSubmissionList(username: $username, limit: $limit) {
        title
        titleSlug
        timestamp
      }
    }
    """

    variables = {
        "username": username,
        "limit": limit
    }

    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/{username}/",
        "Origin": "https://leetcode.com"
    }

    try:
        response = requests.post(url, json={"query": query, "variables": variables}, headers=headers)

        if response.status_code != 200:
            print("❌ Request failed:", response.status_code)
            return []

        data = response.json()
        problems = data.get("data", {}).get("recentAcSubmissionList", [])

        if not problems:
            print("⚠️ No recent accepted problems found.")
            return []

        with open(LOG_PATH, "w") as f:
            json.dump(problems, f, indent=2)

        return problems

    except Exception as e:
        print(f"❌ Error fetching LeetCode data: {e}")
        return []
    
def fetch_problem_metadata(title_slug):
    url = "https://leetcode.com/graphql"
    query = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        title
        titleSlug
        difficulty
        topicTags {
          name
        }
      }
    }
    """
    variables = {"titleSlug": title_slug}
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://leetcode.com/problems/{title_slug}/",
        "Origin": "https://leetcode.com"
    }

    try:
        res = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
        data = res.json()
        return data.get("data", {}).get("question", None)
    except Exception as e:
        print(f"❌ Failed to fetch metadata for {title_slug}: {e}")
        return None


def generate_custom_test(username, limit=20, topics=None, difficulty=None, num_questions=5):
    problems = fetch_recent_ac_problems(username, limit=limit)
    if not problems:
        print("⚠️ No recent submissions found for test generation.")
        return []

    test_pool = []

    for item in problems:
        title_slug = item.get("titleSlug")
        if not title_slug:
            continue

        metadata = fetch_problem_metadata(title_slug)
        if not metadata:
            continue

        problem_difficulty = metadata.get("difficulty")
        topic_tags = [tag["name"] for tag in metadata.get("topicTags", [])]

        # Apply filters
        if difficulty and problem_difficulty.lower() != difficulty.lower():
            continue
        if topics and not any(tag in topics for tag in topic_tags):
            continue

        test_pool.append({
            "title": metadata["title"],
            "titleSlug": metadata["titleSlug"],
            "difficulty": problem_difficulty,
            "tags": topic_tags,
            "link": f"https://leetcode.com/problems/{metadata['titleSlug']}/"
        })

    if not test_pool:
        print("⚠️ No questions matched the filters.")
        return []

    return random.sample(test_pool, min(num_questions, len(test_pool)))

