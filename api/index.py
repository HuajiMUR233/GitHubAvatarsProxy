import re

from aiohttp_client_cache import CachedSession, SQLiteBackend
import fastapi


app = fastapi.FastAPI(
    title="GitHub Avatars Proxy",
    openapi_url=None,
    docs_url=None,
    redoc_url=None
)
base_url = "https://avatars.githubusercontent.com/"
path_formats = [
    re.compile(r"^\w+"),
    re.compile(r"^(\/*)u\/\d+$")
]


@app.get("/{path:path}")
async def _(path: str):
    matched = False
    for i in path_formats:
        if re.fullmatch(i, path):
            matched = True
    if not matched:
        return fastapi.Response(status_code=404)
    url = base_url + path
    print("Getting {}".format(url))
    async with CachedSession(cache=SQLiteBackend("avatars-cache", use_temp=True)) as session:
        async with session.get(url) as response:
            return fastapi.Response(await response.read(), status_code=response.status, headers=response.headers)
