from utilities.json_tokens import JsonConfig


async def log_edited_message(message, after):
    await JsonConfig.channel.topLevelAudits.send(f"```Message edited.\nChannel: {message.channel}\n"
                                                 f"Author: {message.author}\n"
                                                 f"Original Message: {message.content}\n"
                                                 f"Edited Message: {after.content}```")


async def log_deleted_message(message):
    await JsonConfig.channel.topLevelAudits.send(f"```Message deleted.\nChannel: {message.channel}\n"
                                                 f"Author: {message.author}\n"
                                                 f"Message: {message.content}\n```")
