from utilities.message_information_grabs import *
from database.database_functions import *
from utilities.json_tokens import JsonConfig
from utilities.normalization import *
from utilities.tools import *
from commands_and_scoring.scoring import *


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


async def spritz(message):
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
        amount_to_deduct = 5
        user_id = message.author.id
        user_nick = message.author.nick
        if user_nick is None:
            user_nick = message.author.name
        await message.channel.send("You are unauthorized to wield the spritzer.")
        await deduct_from_score(user_id, amount_to_deduct)
        await JsonConfig.channel.botSpam.send(
            f"{user_nick}'s score has been docked {amount_to_deduct} points for unauthorized use of the spritzer. <:spritzer:{JsonConfig.emoji.spritzer}>")
    else:
        no_punct_list, lowered_message, = tidying_caps_punct(message)
        if len(no_punct_list) != 3:
            await message.channel.send("Incorrect command structure.  Please consult !help for additional assistance.")
        elif is_int(no_punct_list[2]) is None:
            await message.channel.send("Please use an integer to properly spritz.")
        else:
            user_id, user_nick = await mentions_information(message)
            raincoat_status = await retrieve_raincoat(user_id)
            if raincoat_status == 1:
                await message.channel.send("Your raincoat has kept you from being spritzed.")
                await raincoat_die_roll(user_id, message)
                return
            else:
                amount_to_deduct = is_int(no_punct_list[2])
                user_id, user_nick = await mentions_information(message)
                await deduct_from_score(user_id, amount_to_deduct)
                await JsonConfig.channel.botSpam.send(f"{user_nick}'s score has been docked {amount_to_deduct} points. <:spritzer:{JsonConfig.emoji.spritzer}>")


async def need_help(message):
    """
    Returns the user with a list of Roomba's current capabilities
    :param message: The raw user inputted message
    :return:
    """
    no_punct_list, lowered_message, = tidying_caps_punct(message)
    if len(no_punct_list) > 1:
        await message.channel.send(f"!help takes no parameters.")
    else:
        help_text = open("text_files/helpdictionary", "r")
        help_message = "```Roomba can perform the following tasks:\n"
        for line in help_text:
            stripped_line = line.strip()
            help_message += f"{stripped_line}\n"
        help_message = help_message + "```"
        await JsonConfig.channel.botSpam.send(help_message)


async def cookie(message):
    """
    Gives the mentioned user a "cookie" worth 10 points
    :param message: The raw user inputted message
    :return:
    """

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
            amount_to_add = 10
            await add_to_score(user_id, amount_to_add)
            await JsonConfig.channel.botSpam.send(f"{user_nick} has been given {number} cookies. 🍪")


async def nom(message):
    """
    Posts a link containing a cookie monster gif and deducts 50 points from the user.
    :param message: The raw user inputted message
    :return:
    """
    user_id = message.author.id
    current_score = await score_query(user_id)
    if current_score >= 50:
        amount_to_deduct = 50
        await deduct_from_score(user_id, amount_to_deduct)
        await message.channel.send("You have spent 50 AnjaPoints™️")
        await message.channel.send("https://tenor.com/view/cookies-gif-14785632")
    else:
        message.channel.send("You cannot afford to nom.")


async def uwu(message):
    """
    Posts a gif of a weeb uwu and deducts 500 points from the user
    :param message: The raw user inputted message
    :return:
    """
    user_id = message.author.id
    current_score = await score_query(user_id)
    if current_score >= 500:
        amount_to_deduct = 500
        await deduct_from_score(user_id, amount_to_deduct)
        await message.channel.send("You have spent 500 AnjaPoints™️")
        await message.channel.send("https://tenor.com/view/uwu-cat-heart-gif-19132889")
    else:
        message.channel.send("You cannot afford to uwu.")


async def buy_raincoat(message):
    """
    Buys a raincoat.
    :param message: Raw user inputted message.
    :return:
    """
    user_id = message.author.id
    raincoat_status = await retrieve_raincoat(user_id)
    if raincoat_status == 1:
        await message.channel.send("You already own a raincoat.")
    else:
        await raincoat_db_add(user_id)
        user_id = message.author.id
        amount_to_deduct = 500
        await deduct_from_score(user_id, amount_to_deduct)
        await message.channel.send("You have purchased a raincoat for 500 AnjaPoints™️.")


async def open_point_store(message):
    no_punct_list, lowered_message, = tidying_caps_punct(message)
    if len(no_punct_list) > 1:
        await message.channel.send(f"!pointstore takes no parameters.")
    else:
        point_store = open("text_files/apstore", "r")
        help_message = "```You may purchase the following items:\n"
        for line in point_store:
            stripped_line = line.strip()
            help_message += f"{stripped_line}\n"
        help_message = help_message + "```"
        await JsonConfig.channel.botSpam.send(help_message)
