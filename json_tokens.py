import json


class JsonConfig:

    channel = None
    token = None
    emoji = None

    class Channel:
        def __init__(self, json_config, client):
            self.audits = client.get_channel(json_config["auditsLogs"])
            self.rules = client.get_channel(json_config["rules"])
            self.lounge = client.get_channel(json_config["lounge"])
            self.botTest = client.get_channel(json_config["botSpam"])

    class Token:
        def __init__(self, json_config):
            self.discord = json_config["discordToken"]
            self.server = json_config["serverId"]

    class Emoji:
        def __init__(self, json_config):
            self.spritzer = json_config["spritzer"]


def open_assign_json():
    """
    opens and loads the json file

    :return: JsonTokens.json_config
    """
    with open("tokens.json") as json_file:
        json_config = json.load(json_file)
    return json_config
