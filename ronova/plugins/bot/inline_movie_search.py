from pyrogram import Client, filters
from pyrogram.types import (InputRichMessage, InlineQuery,
                            InlineQueryResultArticle, InputRichMessageContent)

from ..utilities import get_full_movie


def build_movie_html(poster, banner, title, overview, genre, release, rating, runtime) -> str:

    clean_desc = (overview or "N/A") \
        .replace("<br><br>\n", "\n\n") \
        .replace("<br>", " ") \
        .strip()

    genre_list = "".join(f"<li>{g}</li>" for g in genre)

    return f"""<tg-slideshow>
<img src="{poster}"/>
<img src="{banner}"/>
</tg-slideshow>

<h1>{title}</h1>

<hr/>

<table bordered striped>
<tr><td><b>📅 Release</b></td><td><code>{release}</code></td></tr>
<tr><td><b>⭐ Rating</b></td><td><code>{rating}/10</code></td></tr>
<tr><td><b>⏱ Runtime</b></td><td><code>{runtime} min</code></td></tr>
</table>

<hr/>

<details>
<summary><b>🎭 Genres</b></summary>
<ul>{genre_list}</ul>
</details>

<hr/>

<details>
<summary><b>📖 Synopsis</b></summary>
<blockquote>{clean_desc}</blockquote>
</details>"""

@Client.on_inline_query(filters.regex(r"moviename (.+)"))
async def inline_movie(c: Client, q: InlineQuery):
    name      = q.matches[0].group(1)
    result    = await get_full_movie(name)
    rich_text = build_movie_html(*result)

    await q.answer([
        InlineQueryResultArticle(
            title="send movie",
            input_message_content=InputRichMessageContent(
                InputRichMessage(html=rich_text)
            )
        )
    ], cache_time=0)