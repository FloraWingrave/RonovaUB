import aiohttp
from config import PASTEBIN_KEY

async def paste(content: str, title: str = None, fmt: str = None, time: str = None) -> str:
    url = "https://pastebin.com/api/api_post.php"

    data = {
        "api_dev_key": PASTEBIN_KEY,
        "api_option": "paste",
        "api_paste_code": content,
        "api_paste_name": title if title else "BreezeKuns paste",
        "api_paste_format": fmt if fmt else "text",
        "api_paste_private": "0",
        "api_paste_expire_date": time if time else "10M",
    }

    async with aiohttp.ClientSession() as s:
        async with s.post(url, data=data) as resp:
            data = await resp.json()
            paste_id = data["id"]
            return paste_id, f"https://mystb.in/{paste_id}"

async def delete_paste(paste_id: str):
    async with aiohttp.ClientSession() as s:
        await s.delete(f"https://mystb.in/api/pastes/{paste_id}")