from database.database_functions import *
from utilities.normalization import *


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


