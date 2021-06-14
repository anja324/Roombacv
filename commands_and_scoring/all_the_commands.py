from utilities.message_information_grabs import *
from database.database_functions import *
from utilities.json_tokens import JsonConfig
from utilities.normalization import *
from utilities.tools import *
from discord_items import client


async def fetch_score(message):
    """
    retrieves and prints the score of a user

    :param message: the contents of the raw user message
    :return: None
    """
    user_id, user_nick = await mentions_information(message)

    score = await score_query(user_id)
    if score is None:
        await message.channel.send(f"Error: User or score not found.")
        await JsonConfig.channel.audits.send(f"Score query returned None in {message.channel}.")
    else:
        await JsonConfig.channel.botSpam.send(f"{user_nick}'s current score is {score}.")


async def fetch_leaderboard_top_five(message):
    """
    provide the top five users on the leaderboard

    :param message: Raw user inputted message object
    :return: None
    """
    no_punct_list, lowered_message, = tidying_caps_punct(message)
    if len(no_punct_list) > 1:
        await message.channel.send("This command does not take any parameters.")
    else:
        score_id_list = await retrieve_leaderboard()
        placed_list = enumerate(score_id_list[:5], 1)
        top_five = "The top five residents are:\n"
        for place, (score, name) in placed_list:
            top_five += f"{place}.  {name}, {score} points\n"
        await JsonConfig.channel.botSpam.send(top_five)


async def remove_points(message):
    """
    removes points from the designated user

    :param message: raw user inputted message
    :return: None
    """

    authorized = False
    authorized_sprizters = ["anja324", "abish", "xlexious"]
    for person in authorized_sprizters:
        if person == message.author.name:
            authorized = True
    if authorized is False:
        await message.channel.send("You are unauthorized to wield the spritzer.")
    else:
        no_punct_list, lowered_message, = tidying_caps_punct(message)
        if len(no_punct_list) != 3:
            await message.channel.send("Incorrect command structure.  Please consult !help for additional assistance.")
        elif is_int(no_punct_list[2]) is None:
            await message.channel.send("Please use an integer to properly spritz.")
        else:
            number = is_int(no_punct_list[2])
            user_id, user_nick = await mentions_information(message)
            current_score = await score_query(user_id)
            revised_score = current_score - number
            await change_score(user_id, revised_score)
            await JsonConfig.channel.botSpam.send(f"{user_nick}'s score has been docked {number} points. <:spritzer:{JsonConfig.emoji.spritzer}>")


async def need_help(message):

    no_punct_list, lowered_message, = tidying_caps_punct(message)
    if len(no_punct_list) > 1:
        await message.channel.send(f"!help takes no parameters.")
    else:
        help_text = open("text_files/helpdictionary", "r")
        help_message = "Roomba can perform the following tasks:\n"
        for line in help_text:
            stripped_line = line.strip()
            help_message += f"{stripped_line}\n"
        await JsonConfig.channel.botSpam.send(help_message)


async def cookie(message):

    authorized = False
    authorized_bakers = ["anja324", "abish", "xlexious"]
    for person in authorized_bakers:
        if person == message.author.name:
            authorized = True
    if authorized is False:
        await message.channel.send("You are unauthorized to bake cookies.")
    else:
        no_punct_list, lowered_message, = tidying_caps_punct(message)
        if len(no_punct_list) != 3:
            await message.channel.send("Incorrect command structure.  Please consult !help for additional assistance.")
        elif is_int(no_punct_list[2]) is None:
            await message.channel.send("Please use an integer to properly gib cookies.")
        else:
            number = is_int(no_punct_list[2])
            user_id, user_nick = await mentions_information(message)
            current_score = await score_query(user_id)
            revised_score = current_score + (number * 10)
            await change_score(user_id, revised_score)
            await JsonConfig.channel.botSpam.send(f"{user_nick} has been given {number} cookies. 🍪")


async def nom(message):
    await message.channel.send("https://tenor.com/view/cookies-gif-14785632")


##  async def buy_raincoat(message):

