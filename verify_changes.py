import re

# Emojis regex range
emoji_pattern = re.compile(
    "["
    "\U0001f600-\U0001f64f"  # emoticons
    "\U0001f300-\U0001f5ff"  # symbols & pictographs
    "\U0001f680-\U0001f6ff"  # transport & map symbols
    "\U0001f1e0-\U0001f1ff"  # flags (iOS)
    "\U00002702-\U000027b0"
    "\U000024c2-\U0001f251"
    "\U0001f900-\U0001f9ff"  # Supplemental Symbols and Pictographs
    "\U0001fa70-\U0001faff"  # Symbols and Pictographs Extended-A
    "\u2600-\u27BF"
    "]+", flags=re.UNICODE
)

html_path = "index.html"

with open(html_path, "r", encoding="utf-8") as f:
    lines = f.readlines()

emojis_found = []
dashes_found = []

for i, line in enumerate(lines):
    # Check for emojis
    emojis = emoji_pattern.findall(line)
    if emojis:
        # Ignore svg path data or hex strings that match by accident, only check plain text lines
        # (Usually lines with tag symbols like <path or stroke-width won't have actual emojis,
        # but let's check if the match is actual emojis by filtering out pure ascii/xml)
        for emoji in emojis:
            # Check if it contains actual emoji characters, not just symbols like star or arrow
            # which are part of standard fonts or layout, but let's check
            if any(ord(char) > 127 for char in emoji):
                # ignore standard mathematical/quote symbols
                if emoji not in ["★", "▸", "📋", "🛠️", "⚛️", "🤖", "☁️", "🖥️", "🎓", "📝", "💼", "🚀", "⚡", "🏅", "📍"]:
                    pass
                else:
                    emojis_found.append((i+1, line.strip(), emoji))
                    
    # Check for long dashes: — (em-dash) and – (en-dash)
    if "—" in line or "–" in line:
        dashes_found.append((i+1, line.strip()))

if emojis_found:
    print(f"Found {len(emojis_found)} emojis:")
    for num, content, emoji in emojis_found:
        print(f"Line {num}: {content} (Emoji: {emoji})")
else:
    print("✓ No emojis found.")

if dashes_found:
    print(f"Found {len(dashes_found)} lines with dashes:")
    for num, content in dashes_found:
        print(f"Line {num}: {content}")
else:
    print("✓ No em-dashes or en-dashes found.")
