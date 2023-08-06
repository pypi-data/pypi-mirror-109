import requests

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer bla"
}

resource_id = "Users/033639ae-f78b-4fb8-85f3-fb824c8d5a5a/Messages/AAkALgAAAAAAHYQDEapmEc2byACqAC-EWg0AhqnbfePLvEenp1kwI5dSoQAB6LUsdgAA"
url = f"https://graph.microsoft.com/v1.0/" + resource_id

"""user_id = ""
message_id = ""
url = f"https://graph.microsoft.com/v1.0/users/{user_id}/messages/{message_id}"""""

res = requests.get(url=url, headers=headers)
print(res.json())