from utilities.json_tokens import JsonConfig


async def log_edited_message(before, after):
    await JsonConfig.channel.topLevelAudits.send(f"```Message edited.\nChannel: {before.channel}\n"
                                                 f"Author: {before.author}\n"
                                                 f"Original Message: {before.content}\n"
                                                 f"Edited Message: {after.content}```")


async def log_deleted_message(message):
    await JsonConfig.channel.topLevelAudits.send(f"```Message deleted.\nChannel: {message.channel}\n"
                                                 f"Author: {message.author}\n"
                                                 f"Message: {message.content}\n```")
