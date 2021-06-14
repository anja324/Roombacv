from database.database_functions import *
from utilities.normalization import *
import random
from database.database_functions import *


async def per_text_message_score(message):
    score_addition = 0
    if message.content.startswith("!"):
        return
    no_punct_list, lowered_message = tidying_caps_punct(message)
    if len(no_punct_list) > 1:
        score_addition = len(no_punct_list) * .5

    user_id = message.author.id
    amount_to_add = score_addition
    await add_to_score(user_id, amount_to_add)
    return


async def raincoat_die_roll(user_id, message):
    die_to_roll = await retrieve_raincoat_die_roll(user_id)
    roll_it = random.randint(1, die_to_roll)
    if roll_it == 1:
        await remove_raincoat(user_id)
        await message.channel.send("Your raincoat has broken.  So sad.  Maybe buy a new one?")
    else:
        await increase_raincoat_break_prob(user_id)






