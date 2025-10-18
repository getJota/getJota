#!/usr/bin/env python3
import os, requests, re, sys

STEAM_KEY = os.environ.get("STEAM_KEY")
STEAM_ID = os.environ.get("STEAM_ID")
APPID = 359550  # Rainbow Six Siege

if not STEAM_KEY or not STEAM_ID:
    print("Faltan STEAM_KEY o STEAM_ID en las variables de entorno.", file=sys.stderr)
    sys.exit(1)

url = "https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
params = {
    "key": STEAM_KEY,
    "steamid": STEAM_ID,
    "include_appinfo": "false",
    "include_played_free_games": "true",
    "format": "json"
}

r = requests.get(url, params=params, timeout=15)
r.raise_for_status()
data = r.json().get("response", {}).get("games", [])

minutes = 0
for g in data:
    if g.get("appid") == APPID:
        minutes = g.get("playtime_forever", 0)
        break

hours = round(minutes / 60.0, 1)  # 1 decimal
replacement = f"**{hours} horas**"

readme_path = "README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

new_content, n = re.subn(r"<!-- R6_PLAYTIME -->", replacement, content)
if n == 0:
    print("No se encontró el placeholder <!-- R6_PLAYTIME --> en README.md", file=sys.stderr)
    sys.exit(1)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print(f"README actualizado: {hours} horas (minutos: {minutes})")
