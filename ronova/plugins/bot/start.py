from pyrogram import Client, filters
from pyrogram.types import Message, ReplyParameters, InputRichMessage, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ButtonStyle

@Client.on_message(filters.command("start"))
async def start(c: Client, m: Message):
    chat_id = m.chat.id

    rich_text = """
        <img src="https://i.ibb.co/RTzpvx9Z/x.jpg"/>

        <h1>RonovaUB</h1>
        <p>A powerful <b>Telegram Userbot</b> built with Pyrogram.</p>

        <hr/>

        <h2>Available Commands</h2>

        <table bordered striped>
        <caption>Command Reference</caption>
        <tr>
        <th>Command</th>
        <th>Description</th>
        <th>Usage</th>
        </tr>
        <tr>
        <td><code>.eval</code></td>
        <td>Execute Python code and get the result</td>
        <td><code>.eval 1 + 1</code></td>
        </tr>
        <tr>
        <td><code>.bash</code></td>
        <td>Run a shell/terminal command</td>
        <td><code>.bash ls -la</code></td>
        </tr>
        <tr>
        <td><code>.logs</code></td>
        <td>Fetch the bot's runtime logs</td>
        <td><code>.logs</code></td>
        </tr>
        <tr>
        <td><code>.del</code></td>
        <td>Delete a replied-to message</td>
        <td>Reply + <code>.del</code></td>
        </tr>
        </table>

        <hr/>

        <footer>Use the button below to visit the source repo.</footer>
        """
    await c.send_reaction(chat_id, message_id=m.id, emoji="🔥",big=True)

    await c.send_rich_message(
        chat_id=chat_id,
        rich_message=InputRichMessage(rich_text),
        reply_parameters=ReplyParameters(message_id=m.id),
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Repo", url="https://github.com/BreezeKun/RonovaUB", style=ButtonStyle.PRIMARY)]
        ])
    )