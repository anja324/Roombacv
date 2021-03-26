from database_functions import *
from normalization import *


async def per_text_message_score(message):
    score_addition = 0
    if message.content.startswith("!"):
        return
    no_punct_list, lowered_message = tidying_caps_punct(message)
    if len(no_punct_list) > 1:
        score_addition = len(no_punct_list) * .5

    user_id = message.author.id
    current_score = await score_query(user_id)

    revised_score = current_score + score_addition
    await change_score(user_id, revised_score)
    return
