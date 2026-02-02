# ========== Imports ==========
import aiohttp


# ========== Configuration ==========
# we request data from riot. riot looks at headers to check for access.
# riot looks for "X-Riot-Token"
API_KEY = ""
headers = {
    "X-Riot-Token" : API_KEY
}

# step 1: region. jayden is from a different server so fuck.
REGIONS = {
    # AMERICAS
    "NA": "https://americas.api.riotgames.com",
    "BR": "https://americas.api.riotgames.com",
    "LAN": "https://americas.api.riotgames.com",
    "LAS": "https://americas.api.riotgames.com",
    "OCE": "https://americas.api.riotgames.com",
    "PBE": "https://americas.api.riotgames.com",

    # EUROPES
    "EUW": "https://europe.api.riotgames.com",
    "EUNE": "https://europe.api.riotgames.com",
    "TR": "https://europe.api.riotgames.com",
    "RU": "https://europe.api.riotgames.com",

    # ASIA
    "KR": "https://asia.api.riotgames.com",
    "JP": "https://asia.api.riotgames.com",

    # RANDOMS ASIA
    "PH": "https://sea.api.riotgames.com",
    "SG": "https://sea.api.riotgames.com",
    "TW": "https://sea.api.riotgames.com",
    "TH": "https://sea.api.riotgames.com",
    "VN": "https://sea.api.riotgames.com",
}
