import praw
import json
import re
import os

# ---- Reddit Auth ----
reddit = praw.Reddit(
    client_id='brWU7p9j_4pulCPxMK2fqw',
    client_secret='SYu7-3f0iUl8QRHJvgo9X80T4efBPg',
    user_agent='reddit_data_collector by /u/Careful-Relation-574',
    username='Careful-Relation-574',
    password='TbQPu6GVbGqbQC_'
)

# ---- Subreddits ----
source_subs = [
    "depression", "depressed", "mentalhealth",
    "offmychest", "TrueOffMyChest", "confession",
    "self", "stress", "lonely", "sad", "burnout"
]

# ---- Keyword Buckets ----
keywords_depression = ["depressed", "feeling down", "hopeless", "worthless", "nothing matters", "empty", "low mood"]
keywords_anxiety    = ["anxious", "anxiety", "panic attack", "overthinking", "nervous", "fearful", "panic"]
keywords_suicidal   = ["suicidal", "kill myself", "want to die", "end it all",
    "can't go on", "life is worthless", "i hate my life",
    "done with life", "better off dead", "i give up",
    "no reason to live", "tired of living", "i don't want to exist",
    "ending my life", "die in peace", "escape this life",
    "life is too painful", "wish i was dead", "ready to die",
    "can't do this anymore", "living hurts", "not worth living"]

# Compile regex patterns
pattern_depression = re.compile("|".join(re.escape(k) for k in keywords_depression), re.IGNORECASE)
pattern_anxiety    = re.compile("|".join(re.escape(k) for k in keywords_anxiety), re.IGNORECASE)
pattern_suicidal   = re.compile("|".join(re.escape(k) for k in keywords_suicidal), re.IGNORECASE)

# ---- Load Previous Data ----
filename = "../data/raw/data.json"
existing_ids = set()
existing_posts = []

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        existing_posts = json.load(f)
        existing_ids = {post["id"] for post in existing_posts}

# ---- Scraping Logic ----
new_posts = []
limit_per_sub = 1500  # adjust to target 1k+ per class

for sub in source_subs:
    try:
        print(f"🔎 Collecting from r/{sub}...")
        for post in reddit.subreddit(sub).new(limit=limit_per_sub):
            if post.id in existing_ids:
                continue

            text = f"{post.title} {post.selftext}".lower()

            # Labeling
            if pattern_suicidal.search(text):
                label = "suicidal"
            elif pattern_depression.search(text):
                label = "depression"
            elif pattern_anxiety.search(text):
                label = "anxiety"
            else:
                label = "normal"

            new_post = {
                "id": post.id,
                "title": post.title,
                "selftext": post.selftext,
                "subreddit": sub,
                "label": label,
                "score": post.score,
                "created_utc": post.created_utc
            }
            new_posts.append(new_post)
            existing_ids.add(post.id)
    except Exception as e:
        print(f"⚠️ Skipping r/{sub} (Error: {e})")

# ---- Save Combined File ----
all_posts = existing_posts + new_posts

with open(filename, "w", encoding="utf-8") as f:
    json.dump(all_posts, f, ensure_ascii=False, indent=2)

print(f"✅ Added {len(new_posts)} new posts. Total now: {len(all_posts)}")

#SUICIDAL ONLY
import praw
import json
import re
import os

# ---- Reddit Auth ----
reddit = praw.Reddit(
    client_id='brWU7p9j_4pulCPxMK2fqw',
    client_secret='SYu7-3f0iUl8QRHJvgo9X80T4efBPg',
    user_agent='reddit_data_collector by /u/Careful-Relation-574',
    username='Careful-Relation-574',
    password='TbQPu6GVbGqbQC_'
)

# ---- Subreddits ----
source_subs = [
    "depression", "depressed", "mentalhealth",
    "offmychest", "TrueOffMyChest", "confession",
    "self", "stress", "lonely", "sad", "burnout","Anxiety","depressionsupports","MentalHealthHelp"
]

# ---- Only Suicidal Keywords ----
keywords_suicidal = [
    "suicidal", "kill myself", "want to die", "end it all",
    "can't go on", "life is worthless", "i hate my life",
    "done with life", "better off dead", "i give up",
    "no reason to live", "tired of living", "i don't want to exist",
    "ending my life", "die in peace", "escape this life",
    "life is too painful", "wish i was dead", "ready to die",
    "can't do this anymore", "living hurts", "not worth living"
]

# Compile regex pattern
pattern_suicidal = re.compile("|".join(re.escape(k) for k in keywords_suicidal), re.IGNORECASE)

# ---- Load Previous Data ----
filename = "../data/raw/suicidal.json"   # separate file just for suicidal data
existing_ids = set()
existing_posts = []

if os.path.exists(filename):
    with open(filename, "r", encoding="utf-8") as f:
        existing_posts = json.load(f)
        existing_ids = {post["id"] for post in existing_posts}

# ---- Scraping Logic ----
new_posts = []
limit_per_sub = 50000

for sub in source_subs:
    try:
        print(f"🔎 Collecting from r/{sub}...")
        for post in reddit.subreddit(sub).new(limit=limit_per_sub):
            if post.id in existing_ids:
                continue

            text = f"{post.title} {post.selftext}".lower()

            # ✅ Only keep suicidal-related posts
            if pattern_suicidal.search(text):
                new_post = {
                    "id": post.id,
                    "title": post.title,
                    "selftext": post.selftext,
                    "subreddit": sub,
                    "label": "suicidal",
                    "score": post.score,
                    "created_utc": post.created_utc
                }
                new_posts.append(new_post)
                existing_ids.add(post.id)

    except Exception as e:
        print(f"⚠️ Skipping r/{sub} (Error: {e})")

# ---- Save Combined File ----
all_posts = existing_posts + new_posts

with open(filename, "w", encoding="utf-8") as f:
    json.dump(all_posts, f, ensure_ascii=False, indent=2)

print(f"✅ Added {len(new_posts)} new suicidal posts. Total now: {len(all_posts)}")

import json
import os

labeled_file = "../data/raw/data.json"
suicidal_file = "../data/raw/suicidal.json"

# ---- Load labeled dataset ----
labeled_posts = []
labeled_ids = set()
if os.path.exists(labeled_file):
    with open(labeled_file, "r", encoding="utf-8") as f:
        labeled_posts = json.load(f)
        labeled_ids = {post["id"] for post in labeled_posts}

# ---- Load suicidal dataset ----
with open(suicidal_file, "r", encoding="utf-8") as f:
    suicidal_posts = json.load(f)

# ---- Merge without duplicates ----
new_added = 0
for post in suicidal_posts:
    if post["id"] not in labeled_ids:
        labeled_posts.append(post)
        labeled_ids.add(post["id"])
        new_added += 1

# ---- Save merged file ----
with open(labeled_file, "w", encoding="utf-8") as f:
    json.dump(labeled_posts, f, ensure_ascii=False, indent=2)

print(f"✅ Merged {new_added} suicidal posts into {labeled_file}.")
print(f"📊 Final total: {len(labeled_posts)} posts")
