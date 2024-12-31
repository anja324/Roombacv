from database.database_functions import *
from utilities.user_identification import *
from utilities.json_tokens import JsonConfig 
from modules.scoring import *


async def check_counted_number(message):

    #   checks to see if message was sent in the counting channel
    if message.channel.id == JsonConfig.channel.theCountingRoom.id:
        #   checks to see if message is an integer, if it is not, it is deleted
        counted_number = message.content
        try:
            int(counted_number)
        except ValueError:
            await message.delete()
            return

        #   fetches two most recent counts in counting channel
        count_history = []
        async for count in message.channel.history(limit=2):
            count_history.append(count.content)

        previous_count = int(count_history[1])
        next_valid_count = previous_count + 1
        proposed_count = int(count_history[0])

        if next_valid_count != proposed_count:
            await message.delete()
        else:
            user_id = message.author.id
            amount_to_add = 1
            await add_count_score(user_id, amount_to_add)
            return







