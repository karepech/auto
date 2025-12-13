import requests

INPUT = "sources.txt"

OUT_BOLA = "playlist_bola.m3u"
OUT_SPORT = "playlist_sport.m3u"

# =========================
# KEYWORD SEPAKBOLA
# =========================
BOLA_KEYS = [
    "football", "soccer", "bola",
    "liga", "league",
    "epl", "premier",
    "serie a", "la liga", "bundesliga",
    "ucl", "uefa", "champions",
    "europa league",
    "world cup", "fifa",
    "afc", "asian cup"
]

# =========================
# KEYWORD SPORT LAINNYA
# =========================
SPORT_OTHER_KEYS = [
    "nba", "basket",
    "f1", "formula",
    "motogp", "moto gp",
    "tennis", "badminton",
    "ufc", "mma", "boxing",
    "wwe", "golf",
    "cricket", "baseball",
    "nhl"
]

bola = ["#EXTM3U"]
sport = ["#EXTM3U"]

def is_bola(text):
    t = text.lower()
    return any(k in t for k in BOLA_KEYS)

def is_other_sport(text):
    t = text.lower()
    return any(k in t for k in SPORT_OTHER_KEYS)

# =========================
# LOAD SOURCE URL
# =========================
with open(INPUT, "r") as f:
    urls = [u.strip() for u in f if u.strip()]

# =========================
# PROCESS PLAYLIST
# =========================
for url in urls:
    try:
        r = requests.get(url, timeout=20)
        if r.status_code != 200:
            continue

        lines = r.text.splitlines()
        i = 0
        while i < len(lines):
            if lines[i].startswith("#EXTINF"):
                info = lines[i]
                stream = lines[i + 1] if i + 1 < len(lines) else ""

                if is_bola(info):
                    bola.append(info)
                    bola.append(stream)
                elif is_other_sport(info):
                    sport.append(info)
                    sport.append(stream)

                i += 2
            else:
                i += 1

    except Exception as e:
        print("ERROR:", url, e)

# =========================
# SAVE FILE
# =========================
with open(OUT_BOLA, "w", encoding="utf-8") as f:
    f.write("\n".join(bola))

with open(OUT_SPORT, "w", encoding="utf-8") as f:
    f.write("\n".join(sport))

print("DONE: playlist_bola.m3u & playlist_sport.m3u")
