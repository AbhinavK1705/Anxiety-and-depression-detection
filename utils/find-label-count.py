import json
from collections import Counter

# ---- Load Your Data ----
filename = "../data/raw/data.json"   # change if your file is named differently

with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f)

# ---- Count Labels ----
labels = [post.get("label", "unknown") for post in data]
counts = Counter(labels)

# ---- Print Results ----
print("📊 Posts per Category:")
for label, count in counts.items():
    print(f"{label}: {count}")

print(f"\n✅ Total posts: {len(data)}")
