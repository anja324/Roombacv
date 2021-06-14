# noinspection PyUnresolvedReferences
from commands_and_scoring.all_the_commands import *


# noinspection SpellCheckingInspection
def create_command_dict():
    """
    creates a dictionary with the format command:function

    :return: command_dict
    """
    command_file = open("text_files/commandslist", "r")
    command_dict = {}
    for line in command_file:
        split_line = line.split(" ", 1)
        command_line = split_line[1].rstrip()
        command_dict.update({split_line[0]: command_line})
    return command_dict


async def command_exists(message, command_dict, lowered_message):
    """
    Determines whether a user input beginning with ! is a valid command.  If so, triggers run_a_command.

    :param message: raw user inputted message
    :param command_dict: dictionary of commands format command:function
    :param lowered_message: lowered version of raw user inputted message
    :return: maybe_command, command_parameter_id
    """
    if lowered_message.startswith("!"):
        no_exclaim = lowered_message.replace("!", "", 1)
        split_message = no_exclaim.split(" ")
        if len(split_message) <= 3:
            maybe_command = command_dict.get(split_message[0])
            if maybe_command is None:
                await message.channel.send("Command does not exist.  Reference !help for more information.")
            else:
                command_name = maybe_command
                await globals().get(command_name)(message)
        else:
            await message.channel.send("Invalid command structure.  Reference !help for more information.")
