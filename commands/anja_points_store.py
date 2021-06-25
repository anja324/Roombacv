from modules.raincoat import retrieve_raincoat, raincoat_db_add
from modules.scoring import deduct_from_score, score_query
from utilities.json_tokens import JsonConfig
from utilities.normalization import tidying_caps_punct


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