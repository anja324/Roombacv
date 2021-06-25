from modules.raincoat import raincoat_die_roll, retrieve_raincoat
from utilities.message_information_grabs import *
from utilities.json_tokens import JsonConfig
from utilities.tools import *
from modules.scoring import *


async def fetch_balance(message):
    """
    retrieves and prints the score of a user

    :param message: the contents of the raw user message
    :return: None
    """
    no_punct_list, lowered_message = tidying_caps_punct(message)
    if len(no_punct_list) == 1:
        await my_balance(message)
    else:
        user_id, user_nick = await mentions_information(message)
        score = await score_query(user_id)
        if score is None:
            await message.channel.send(f"Error: User or balance not found.")
            await JsonConfig.channel.audits.send(f"Balance query returned None in {message.channel}.")
        else:
            await JsonConfig.channel.botSpam.send(f"{user_nick}'s current balance is {score} AnjaPoints™️.")


async def my_balance(message):

    no_punct_list, lowered_message = tidying_caps_punct(message)
    if len(no_punct_list) == 1:
        user_id = message.author.id
        user_nick = message.author.nick
        if user_nick is None:
            user_nick = message.author.name
        score = await score_query(user_id)
        if score is None:
            await message.channel.send(f"Error: User or balance not found.")
            await JsonConfig.channel.audits.send(f"Balance query returned None in {message.channel}.")
        else:
            await JsonConfig.channel.botSpam.send(f"{user_nick}, your current balance is {score} AnjaPoints™️.")
    else:
        await message.channel.send(f"Error: !mybalance does not take any parameters.")


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
            f"{user_nick}'s balance has been docked {amount_to_deduct} AnjaPoints™️ for unauthorized use of the spritzer. <:spritzer:{JsonConfig.emoji.spritzer}>")
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
                await message.channel.send(f"{user_nick}'s balance has been docked {amount_to_deduct} AnjaPoints™️. <:spritzer:{JsonConfig.emoji.spritzer}>")


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
            amount_to_add = number * 10
            await add_to_score(user_id, amount_to_add)
            await message.channel.send(f"{user_nick} has been given {number} cookies. 🍪")


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
