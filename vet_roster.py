import urllib.request
import urllib.error
import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

matches = re.findall(r'day:\s*(\d+).*?title:\s*"([^"]+)".*?videoId:\s*"([^"]+)"', content, re.DOTALL)

print(f"🔍 Testing {len(matches)} tracks against YouTube Embed Policy...\n" + "=" * 60)

blocked = []

for day, title, vid in matches:
    url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid}&format=json"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        urllib.request.urlopen(req, timeout=5)
        print(f"✅ Day {day:>2}: OK       | {title}")
    except urllib.error.HTTPError as e:
        status = "BLOCKED (Embed Restricted)" if e.code in (401, 403) else f"ERROR {e.code}"
        print(f"❌ Day {day:>2}: {status:<24} | {title} (ID: {vid})")
        blocked.append((day, title, vid, status))
    except Exception as e:
        print(f"⚠️ Day {day:>2}: TIMEOUT    | {title} (ID: {vid})")
        blocked.append((day, title, vid, "TIMEOUT"))

print("=" * 60)
if not blocked:
    print("🎉 All 30 tracks are 100% verified and embed-safe!")
else:
    print(f"⚠️ {len(blocked)} track(s) need alternate embed-permissive IDs.")
