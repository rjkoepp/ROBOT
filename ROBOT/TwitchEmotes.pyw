import urllib, json

def generate_emotes():
    url = "https://twitchemotes.com/api_cache/v2/global.json"

    response = urllib.urlopen(url)
    emoticon_data = json.loads(response.read())
 
    return [str(emote_name_key) for key in emoticon_data.iterkeys()
            for emote_name_key in emoticon_data[key]]
