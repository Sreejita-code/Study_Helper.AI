import requests
import json
import os
import random

LOG_PATH = os.path.join("data", "leetcode_log.json")

# ---------------- Fetch recent AC problems ---------------- #
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
    headers = {
        "Content-Type": "application/json",
        "Referer": f"https://leetcode.com/{username}/",
        "Origin": "https://leetcode.com"
    }

    try:
        res = requests.post(url, json={"query": query, "variables": {"username": username, "limit": limit}}, headers=headers)
        if res.status_code != 200:
            print(f"❌ LeetCode request failed with status: {res.status_code}")
            return []

        problems = res.json().get("data", {}).get("recentAcSubmissionList", [])
        if problems:
            os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
            with open(LOG_PATH, "w") as f:
                json.dump(problems, f, indent=2)

        return problems
    except Exception as e:
        print(f"❌ Error fetching LeetCode data: {e}")
        return []

# ---------------- Fetch metadata of a problem ---------------- #
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
          slug
        }
      }
    }
    """
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Referer": f"https://leetcode.com/problems/{title_slug}/",
        "Origin": "https://leetcode.com"
    }

    try:
        res = requests.post(url, json={"query": query, "variables": {"titleSlug": title_slug}}, headers=headers)
        return res.json().get("data", {}).get("question", None)
    except Exception as e:
        print(f"❌ Failed to fetch metadata for {title_slug}: {e}")
        return None

# ---------------- Fetch questions from public problemset ---------------- #
def fetch_additional_questions(topics=None, limit=50):
    url = "https://leetcode.com/graphql"
    query = """
    query problemsetQuestionList($filters: QuestionListFilterInput, $limit: Int, $skip: Int) {
      problemsetQuestionList(filters: $filters, limit: $limit, skip: 0) {
        questions {
          title
          titleSlug
          difficulty
          topicTags {
            name
            slug
          }
        }
      }
    }
    """

    # Mapping from topic names to slugs
    name_to_slug = {
        "Array": "array",
        "Math": "math",
        "Bit Manipulation": "bit-manipulation",
        "Hash Table": "hash-table",
        "Binary Search": "binary-search",
        "Sorting": "sorting",
        "Two Pointers": "two-pointers",
        "Dynamic Programming": "dynamic-programming",
        "Greedy": "greedy",
        "String": "string",
        "Prefix Sum": "prefix-sum",
        "Number Theory": "number-theory",
        "Simulation": "simulation",
        "Recursion": "recursion"
    }

    tag_slugs = [name_to_slug[tag] for tag in topics if tag in name_to_slug] if topics else []

    variables = {
        "filters": {
            "tags": tag_slugs
        },
        "limit": limit,
        "skip": 0
    }

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://leetcode.com/problemset/all/",
        "Origin": "https://leetcode.com"
    }

    try:
        res = requests.post(url, json={"query": query, "variables": variables}, headers=headers)
        questions = res.json().get("data", {}).get("problemsetQuestionList", {}).get("questions", [])
        return [{
            "title": q["title"],
            "titleSlug": q["titleSlug"],
            "difficulty": q["difficulty"],
            "tags": [tag["name"] for tag in q["topicTags"]],
            "problemLink": f"https://leetcode.com/problems/{q['titleSlug']}/",
            "solutionLink": f"https://leetcode.com/problems/{q['titleSlug']}/solutions/"
        } for q in questions]
    except Exception as e:
        print(f"❌ Error fetching problemset: {e}")
        return []

# ---------------- Generate personalized test ---------------- #
def generate_custom_test(username, limit=25, num_questions=10):
    recent = fetch_recent_ac_problems(username, limit=limit)
    print("Debug — recent submissions:", [p["titleSlug"] for p in recent])

    if not recent:
        print("⚠️ No recent problems fetched.")
        return []

    recent_slugs = {p["titleSlug"] for p in recent}
    topic_counter = {}

    for p in recent:
        meta = fetch_problem_metadata(p["titleSlug"])
        print(f"Debug — metadata for {p['titleSlug']}:", meta)
        if not meta:
            continue
        for tag in meta["topicTags"]:
            topic = tag["name"]
            topic_counter[topic] = topic_counter.get(topic, 0) + 1

    print("Debug — topic_counts:", topic_counter)

    if not topic_counter:
        print("⚠️ No topics found in recent submissions.")
        return []

    top_topics = sorted(topic_counter, key=topic_counter.get, reverse=True)[:3]
    print("📌 Top topics:", top_topics)

    # Try to find similar unsolved problems
    similar = fetch_additional_questions(topics=top_topics, limit=50)
    print("Debug — fetched similar slugs:", [q["titleSlug"] for q in similar])

    new_questions = [q for q in similar if q["titleSlug"] not in recent_slugs]
    print("Debug — filtered new slugs:", [q["titleSlug"] for q in new_questions])

    if not new_questions:
        print("⚠️ No similar unsolved questions found. Trying fallback...")

        # Fallback to all questions with top topics (including already solved ones)
        similar_all = fetch_additional_questions(topics=top_topics, limit=50)
        fallback_questions = similar_all[:]

        if not fallback_questions:
            print("⚠️ Even fallback failed. Returning random recent questions.")
            fallback_questions = [
                {
                    "title": p["title"],
                    "titleSlug": p["titleSlug"],
                    "difficulty": "Easy",
                    "tags": [],
                    "problemLink": f"https://leetcode.com/problems/{p['titleSlug']}/",
                    "solutionLink": f"https://leetcode.com/problems/{p['titleSlug']}/solutions/"
                }
                for p in recent
            ]

        picked = random.sample(fallback_questions, min(num_questions, len(fallback_questions)))
        print("✅ Final picks from fallback:", [q["titleSlug"] for q in picked])
        return picked

    # Return picked from new questions
    picked = random.sample(new_questions, min(num_questions, len(new_questions)))
    print("✅ Final picks:", [q["titleSlug"] for q in picked])
    return picked
