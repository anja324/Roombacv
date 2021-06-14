from utilities.json_tokens import JsonConfig


def create_explicit_array():
    """
    creates an array of explicit terms which are not acceptable

    :return: explicit_array
    """
    # noinspection SpellCheckingInspection
    explicit_arr = open("text_files/explicitarray", "r")
    explicit_array = []
    for line in explicit_arr:
        stripped_line = line.strip()
        explicit_array.append(stripped_line)

    return explicit_array


async def explicit_words(explicit_array, message, no_punct_list):
    """
    determines whether an explicit word is present in the user message, deletes the message with explicit content,
     sends a message to the channel,  and logs occurrence in a logs channel
    
    :param explicit_array: an array of explicit words or terms that are unacceptable
    :param message: the raw user sent message in the server
    :param no_punct_list: a normalized, lowered, punctuation-less version of the raw message
    :return: None
    """

    for item in no_punct_list:
        for word in explicit_array:
            if item == word:
                await JsonConfig.channel.audits.send(f"```Explicit message sent.\nChannel: {message.channel}\n"
                                                     f"Author: {message.author}\n"
                                                     f"Message: {message.content}```")
                await message.delete()
                await message.channel.send(f"You have sent a message which contains a racial slur on my list.  "
                                           f"There is no place for that here.  "
                                           f"Please reference {JsonConfig.channel.rules} for further information.  "
                                           f"This is your **only** warning.")
