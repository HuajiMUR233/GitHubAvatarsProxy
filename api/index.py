import re

import fastapi
import fastapi.responses
import aiohttp


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


@app.route("/")
async def _():
    return fastapi.responses.RedirectResponse("https://github.com")


@app.get("/{path:path}")
async def _(path: str):
    matched = False
    for i in path_formats:
        if re.fullmatch(i, path):
            matched = True
    if not matched:
        return fastapi.Response(status_code=404)
    print("Getting {}".format(base_url + path))
    async with aiohttp.ClientSession(base_url) as session:
        async with session.get(path) as response:
            return fastapi.Response(await response.read(), status_code=response.status, headers=response.headers)
