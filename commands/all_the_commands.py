import random

from modules.raincoat import raincoat_die_roll, retrieve_raincoat
from modules.scoring import score_query
from utilities.message_information_grabs import *
from utilities.json_tokens import JsonConfig
from utilities.normalization import tidying_caps_punct
from utilities.tools import *
from modules.scoring import *
from utilities.user_identification import user_is_mod


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
    """
    retrieves and prints the score of the user who calls it

    :param message: the contents of the raw user message
    :return: None
    """

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

    mod_status = await user_is_mod(message)
    if mod_status is False:
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
        elif int(no_punct_list[2]) > 5:
            await message.channel.send(
                "Your spritz was too high.  Perhaps if the offense was this serious it should be 'discussed'.")
        elif int(no_punct_list[2]) < 1:
            await message.channel.send(
                "If you want to spritz, you should probably pick a positive integer between 0 and 6")
        else:
            user_id, user_nick = await mentions_information(message)
            user_score = await score_query(user_id)
            spritz_amount = int(round(((int(no_punct_list[2]) * user_score) / 100), 0))
            raincoat_status = await retrieve_raincoat(user_id)
            if raincoat_status == 1:
                await message.channel.send(
                    f"Your raincoat has kept you from being spritzed {spritz_amount} AnjaPoints™️.")
                await raincoat_die_roll(user_id, message)
                return
            else:
                await deduct_from_score(user_id, spritz_amount)
                await message.channel.send(
                    f"{user_nick}'s balance has been docked {spritz_amount} AnjaPoints™️. <:spritzer:{JsonConfig.emoji.spritzer}>")


async def cookie(message):
    """
    Gives the mentioned user a "cookie" worth 10 points
    :param message: The raw user inputted message
    :return:None
    """

    mod_status = await user_is_mod(message)
    if mod_status is False:
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
    :return: None
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


async def open_point_store(message):
    """
    Prints a list of purchasable items and their costs

    :param message: the contents of the raw user message
    :return: None
    """

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


async def bot_control(message):
    """
    Prints the text specified by a user in a given channel

    :param message: the contents of the raw user message
    :return: None
    """
    can_make_roomby_speak = await user_is_mod(message)
    if can_make_roomby_speak is True:
        channel_info_list = message.channel_mentions
        if len(channel_info_list) > 1 or len(channel_info_list) < 1:
            await message.channel.send("You done effed up.  Please make sure you mention exactly one channel")
        else:
            desired_channel = channel_info_list[0].name
            server_channel_list = await message.guild.fetch_channels()
            for room in server_channel_list:
                if desired_channel == room.name:
                    command_split = message.content.split(" ", 2)
                    if len(command_split) < 2:
                        await message.channel.send(
                            "You done effed up.  Please check your command structure and try again. (!speak <channel mention> message)")
                    else:
                        desired_text = command_split[2]
                        await room.send(desired_text)
                else:
                    pass
    else:
        await message.delete()
        return


async def roll_die(message):
    """
    Rolls a specified number of dice with a specified number of sides.

    :param message: the contents of the raw user message
    :return: None
    """

    #   separates user request from command message and checks that it is properly formatted as a command
    no_punct_list, lowered_message = tidying_caps_punct(message)
    if len(no_punct_list) > 2 or len(no_punct_list) < 2:
        await message.channel.send("Invalid command structure, maybe take a look at help.")
        return
    #   separates the number of dice and the number of sides, discards the "d"
    desired_roll = no_punct_list[1]

    if len(desired_roll.split("d")) != 2:
        await message.channel.send("Invalid command structure, maybe read the description in the help text.")
        return

    number_of_dice = desired_roll.split("d")[0]
    number_of_sides = desired_roll.split("d")[1]

    #   Checks that number of dice and sides are integers, and not stupid large
    if not is_int(number_of_dice):
        await message.channel.send("Try using a number that doesn't break the universe, genius.")
    elif not is_int(number_of_sides):
        await message.channel.send("Try using a number that doesn't break the universe, genius.")
    elif int(number_of_dice) > 100:
        await message.channel.send("Isn't rolling that many dice a little excessive?  Maybe you should reevaluate your choices.")
    elif int(number_of_sides) > 1000:
        await message.channel.send("Isn't rolling a die that big a little excessive?  Maybe you should reevaluate your choices.")

    #   rolls specified number of dice, formats results, and sends to channel
    else:
        roll_results = []
        number_of_dice = int(number_of_dice)
        number_of_sides = int(number_of_sides)
        while len(roll_results) != number_of_dice:
            roll_it = random.randint(1, number_of_sides)
            roll_results.append(str(roll_it))
        pretty_rolls = ", ".join(roll_results)
        await message.channel.send(pretty_rolls)


async def fetch_count_balance(message):
    """
    retrieves and prints the score of a user

    :param message: the contents of the raw user message
    :return: None
    """

    no_punct_list, lowered_message = tidying_caps_punct(message)
    if len(no_punct_list) == 1:
        await my_count_balance(message)
    else:
        user_id, user_nick = await mentions_information(message)
        count_score = await count_score_query(user_id)
        if count_score is None:
            await message.channel.send(f"Error: User or balance not found.")
            await JsonConfig.channel.audits.send(f"Balance query returned None in {message.channel}.")
        else:
            await JsonConfig.channel.botSpam.send(f"{user_nick}'s current total count is {count_score} numbers. Ah ah ah.")


async def my_count_balance(message):
    """
    retrieves and prints the count score of the user who calls it

    :param message: the contents of the raw user message
    :return: None
    """

    no_punct_list, lowered_message = tidying_caps_punct(message)
    if len(no_punct_list) == 1:
        user_id = message.author.id
        user_nick = message.author.nick
        if user_nick is None:
            user_nick = message.author.name
        count_score = await count_score_query(user_id)
        if count_score is None:
            await message.channel.send(f"Error: User or balance not found.")
            await JsonConfig.channel.audits.send(f"Balance query returned None in {message.channel}.")
        else:
            await JsonConfig.channel.botSpam.send(f"{user_nick}, your current total count is {count_score} numbers. Ah ah ah.")
    else:
        await message.channel.send(f"Error: !mycountbalance does not take any parameters.")

