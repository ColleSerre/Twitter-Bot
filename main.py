import requests
import json
from random import choice


def boot():
    url = "https://api.twitter.com/1.1/direct_messages/events/list.json"

    payload = {}
    headers = {
    'Authorization': 'OAuth oauth_consumer_key="evU44CQF1zDWuk5xbsevanivE",oauth_token="875370818552946688-xQFoplPIaNNLtreqYNYn5I7n5S7RgEY",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1597353192",oauth_nonce="zd0XmW94OuM",oauth_version="1.0",oauth_signature="SmaIbfgajA4DsANfTvM%2BG%2Fb69Jk%3D"',
    'Cookie': 'personalization_id="v1_2/hmGenDkuo9anjp3e7TdA=="; guest_id=v1%3A159722505884068591'
    }

    response = requests.request("GET", url, headers=headers, data = payload)

    response = response.json()

    with open("DM.json", "w+") as file:
        response = dict(response)
        for i in response["events"]:
            i["used"] = "true"
        json.dump(response, file)
        file.close()

    url = "https://api.twitter.com/1.1/followers/list.json"

    payload = {}
    headers = {
    'Authorization': 'OAuth oauth_consumer_key="evU44CQF1zDWuk5xbsevanivE",oauth_token="875370818552946688-xQFoplPIaNNLtreqYNYn5I7n5S7RgEY",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1597353172",oauth_nonce="FhMn88x4KWt",oauth_version="1.0",oauth_signature="Gn%2B4WacQ1K7G3j%2BvBYguzdIDfGY%3D"',
    'Cookie': 'personalization_id="v1_2/hmGenDkuo9anjp3e7TdA=="; guest_id=v1%3A159722505884068591'
    }

    r = requests.request("GET", url, headers=headers, data = payload)


    r = r.json()

    with open("follows.json", "w+") as file:
        json.dump(r, file)
        file.close()


def modify_payload(message, recipient):
    username = selected_user["screen_name"]

    with open("DmPayload.json", "r") as file:
        contents = json.loads(file.read())
        # CHANGE TO selected_user["id_str"] on release
        contents["event"]["message_create"]["target"]["recipient_id"] = "866285986208239616"
        contents["event"]["message_create"]["message_data"]["text"] = message
        file.close()
    with open("DmPayload.json", "w") as file:
        json.dump(contents, file)
        file.close()


def send_dm():
   
    url = "https://api.twitter.com/1.1/direct_messages/events/new.json"

    with open("DmPayload.json", "r") as file:
        payload = file.read()
        print(type(payload))
        file.close()

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'OAuth oauth_consumer_key="evU44CQF1zDWuk5xbsevanivE",oauth_token="875370818552946688-xQFoplPIaNNLtreqYNYn5I7n5S7RgEY",oauth_signature_method="HMAC-SHA1",oauth_timestamp="1597353172",oauth_nonce="Dd1obqudVCi",oauth_version="1.0",oauth_signature="NdLU57hTbl3yEh6CcU4ec4UyG4Q%3D"',
    'Cookie': 'personalization_id="v1_2/hmGenDkuo9anjp3e7TdA=="; guest_id=v1%3A159722505884068591'
    }

    response = requests.request("POST", url, headers=headers, data = payload)

    print(response.text.encode('utf8'))
    print(response.status_code)


with open("follows.json", "r") as file:
    contents = json.loads(file.read())
    selected_user = choice(contents["users"])
    file.close()

with open("DM.json", "r") as file:
    contents = json.loads(file.read())
    count = 0
    for i in contents["events"]:
        if i["used"] == "true":
            print("Ignored 1")
            continue
        else:
            body = i["message_create"]["message_data"]["text"]
            modify_payload('Your message "{}" has successfully been sent to user @{}'.format(
                body, selected_user["screen_name"]), selected_user)
            print("-"*100)
            send_dm()
            modify_payload("Someone confesses '{}' ; Your turn ? ".format(
                body), selected_user)
            send_dm()
        count += 1
    file.close()

