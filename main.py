import discord

from resident_member_info.Resident import *
from utilities.json_tokens import *
from modules.explicit_words import *
from modules.easter_eggs import *
from utilities.command_identifier import create_command_dict, command_exists
from modules.scoring import *


#   connects to the server via id
# intents = discord.Intents.default()
# intents.members = True
client = discord.Client()
#   intents=intents

#   global variables
resident_roster = []
explicit_array = []
command_dict = {}
easter_egg_dict = {}


@client.event
async def on_ready():

    global explicit_array, easter_egg_dict, resident_roster, command_dict

    #   prints confirmation of bot connection, and the server to which it is connected
    print(f'{client.user} has connected to Discord!')
    for guild in client.guilds:
        print(f'{client.user} is connected to the following guilds:\n'
              f'{guild.name} id {guild.id}')
        members_list = await guild.fetch_members(limit=200).flatten()
        for dweller in members_list:
            resident_roster.append(Resident(dweller.name, dweller.id))
    population_of_resident_database(resident_roster)

    #   creates arrays utilized for bot reference
    explicit_array = create_explicit_array()
    easter_egg_dict = create_easter_egg_dict()
    command_dict = create_command_dict()
    JsonConfig.channel = JsonConfig.Channel(json_config, client)


#   waits for a user message to perform related functions
@client.event
async def on_message(message):

    #   bot will not respond to itself
    if message.author == client.user:
        return

    no_punct_list, lowered_message = tidying_caps_punct(message)
    await explicit_words(explicit_array, message, no_punct_list)
    await command_exists(message, command_dict, lowered_message)
    await easter_eggs(message, easter_egg_dict, lowered_message)
    await tabulate_message_score(message)


@client.event
async def on_member_join(member):
    await accept_new_resident(member, resident_roster)

#   opens the json file, and assigns all data to variables inside class JsonConfig
json_config = open_assign_json()
JsonConfig.token = JsonConfig.Token(json_config)
JsonConfig.emoji = JsonConfig.Emoji(json_config)

connect_andor_create_resident_database()
client.run(JsonConfig.token.discord)
