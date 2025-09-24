import json

POSTS_FILE = "posts.json"


def load_posts():
    """Load all blog posts from the JSON file."""
    try:
        with open(POSTS_FILE, encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def save_posts(posts):
    """Save all blog posts to the JSON file."""
    with open(POSTS_FILE, "w", encoding="utf-8") as file:
        json.dump(posts, file, indent=4, ensure_ascii=False)