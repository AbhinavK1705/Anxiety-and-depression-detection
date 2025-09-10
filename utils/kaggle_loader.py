import os
import json
import uuid
import pandas as pd
import time
from pathlib import Path
import random
from tqdm import tqdm
from datetime import datetime

# ---------------- CONFIG ---------------- #
KAGGLE_PATH = "../../archive/Suicide_Detection.csv"
RAW_JSON_PATH = "../data/raw/data.json"

# Define keywords for filtering
SUICIDE_KEYWORDS = [
    "suicidal", "i am suicidal", "i'm suicidal", "want to die", "want to end it all",
    "kill myself", "i will kill myself", "i want to die", "end it all", "ending my life",
    "i cant take it", "i can't take it", "i don't want to live", "dont want to live",
    "dont want to be here", "i give up", "ready to die", "wish i was dead", "better off dead",
    "thinking about suicide", "thoughts of suicide", "i want to end it", "i'm done",
    "im done", "going to end it", "overdose", "want to disappear", "no reason to live",
    "i want out", "i want to die right now"
]

DEPRESSION_KEYWORDS = [
    "depressed", "feeling depressed", "i feel depressed", "feeling low", "im feeling down",
    "i'm feeling down", "feeling down", "low mood", "hopeless", "hopelessness", "worthless",
    "i hate myself", "i'm broken", "i am broken", "i'm lonely", "im lonely", "numb",
    "nothing matters", "i'm so sad", "i am so sad", "i'm so tired", "i'm tired of living",
    "crying again", "i cry", "feeling empty", "lost interest", "no motivation", "can't cope",
    "cant cope", "can't enjoy", "cant enjoy"
]

ANXIETY_KEYWORDS = [
    "anxious", "feeling anxious", "i'm anxious", "im anxious", "panic attack",
    "panic attacks", "panic", "overwhelmed", "i'm overwhelmed", "im overwhelmed",
    "heart racing", "racing heart", "cant breathe", "can't breathe", "hyperventilate",
    "overthinking", "worrying", "constant worry", "nervous", "social anxiety",
    "can't sleep", "insomnia", "sweating", "shaking", "feeling panicked"
]

ALL_KEYWORDS = SUICIDE_KEYWORDS + DEPRESSION_KEYWORDS + ANXIETY_KEYWORDS


# ---------------- FUNCTIONS ---------------- #

def text_contains_keywords(text: str) -> bool:
    """Check if text contains any of our mental health keywords."""
    text_lower = text.lower()
    return any(keyword in text_lower for keyword in ALL_KEYWORDS)


def split_text_into_title_selftext(text: str, title_word_limit: int = 10):
    """Split text into title (first N words) and selftext (remaining)."""
    words = text.strip().split()
    if not words:
        return "", ""
    title = " ".join(words[:title_word_limit])
    selftext = " ".join(words[title_word_limit:]) if len(words) > title_word_limit else ""
    return title, selftext


# def process_kaggle_dataset():
#     """Process ONLY non-suicide posts from Kaggle dataset as 'normal' and save into raw JSON."""
#     df = pd.read_csv(KAGGLE_PATH)

#     # Load existing raw JSON if present
#     raw_data = []
#     if os.path.exists(RAW_JSON_PATH):
#         with open(RAW_JSON_PATH, "r", encoding="utf-8") as f:
#             try:
#                 raw_data = json.load(f)
#             except json.JSONDecodeError:
#                 raw_data = []

#     new_entries_json = []

#     for _, row in tqdm(df.iterrows(), total=len(df), desc="Processing Kaggle data"):
#         text = str(row["text"]).strip()
#         label = row["class"]

#         # ✅ Only consider non-suicide rows
#         if label != "non-suicide":
#             continue  

#         # Skip if mental health keywords are present
#         if text_contains_keywords(text):
#             continue  

#         # Otherwise, assign as normal
#         post_id = str(uuid.uuid4())[:8]
#         title, selftext = split_text_into_title_selftext(text)

#         json_entry = {
#             "id": post_id,
#             "subreddit": "kaggle_dataset",
#             "title": title,
#             "selftext": selftext,
#             "label": "normal",
#             "created_utc": int(time.time()),
#             "url": f"https://kaggle.com/{post_id}"
#         }

#         new_entries_json.append(json_entry)

#     # Append to raw data JSON
#     raw_data.extend(new_entries_json)
#     with open(RAW_JSON_PATH, "w", encoding="utf-8") as f:
#         json.dump(raw_data, f, ensure_ascii=False, indent=2)

#     print(f"✅ Added {len(new_entries_json)} NON-SUICIDE posts as normal into raw JSON.")
#     print(f"📊 Updated raw JSON: {len(raw_data)} entries total")

def process_kaggle_dataset(kaggle_csv=KAGGLE_PATH,
                           raw_json=RAW_JSON_PATH,
                           n_samples=10000):
    """
    Process Kaggle Suicide_Detection.csv and add N random non-suicide posts
    as 'normal' into raw_data.json (with proper structure).
    """

    # 1. Load dataset
    df = pd.read_csv(kaggle_csv)

    # 2. Filter only non-suicide
    df = df[df["class"] == "non-suicide"].copy()
    print(f"📊 Found {len(df)} non-suicide rows in Kaggle dataset.")

    # 3. Sample N random posts
    if len(df) > n_samples:
        df = df.sample(n=n_samples, random_state=42).reset_index(drop=True)
    else:
        df = df.reset_index(drop=True)
        print(f"⚠️ Only {len(df)} non-suicide rows available, using all.")

    # 4. Load existing raw_data.json
    if os.path.exists(raw_json):
        with open(raw_json, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
    else:
        raw_data = []

    existing_ids = {entry["id"] for entry in raw_data}

    new_entries = []

    for _, row in df.iterrows():
        text = str(row["text"]).strip()

        # Skip empty text
        if not text or len(text) < 20:
            continue

        # Split text into title + selftext
        words = text.split()
        title = " ".join(words[:7])  # first few words as title
        selftext = " ".join(words[7:]) if len(words) > 7 else ""

        # Generate unique ID
        post_id = str(uuid.uuid4())[:8]  # short random ID

        if post_id in existing_ids:
            continue

        entry = {
            "id": post_id,
            "subreddit": "kaggle_normal",
            "title": title,
            "selftext": selftext,
            "label": "normal",
            "created_utc": datetime.utcnow().timestamp(),
            "url": "https://www.kaggle.com/datasets/nikhileswarkomati/suicide-watch"
        }

        raw_data.append(entry)
        new_entries.append(entry)

    # 5. Save back JSON
    with open(raw_json, "w", encoding="utf-8") as f:
        json.dump(raw_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Added {len(new_entries)} Kaggle NON-SUICIDE posts as normal.")
    print(f"📊 Raw JSON now has {len(raw_data)} entries total.")
  
if __name__ == "__main__":
    process_kaggle_dataset()

