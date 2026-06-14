from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.routing import Route
from starlette.requests import Request
import asyncio

async def dashboard(request: Request):
    html_content = """
    <html>
        <head>
            <title>Monkey D. Luffy Dashboard</title>
            <style>
                body { font-family: Arial; text-align: center; margin-top: 50px; background: #111; color: #fff; }
                h1 { color: #f3c623; }
                .status { font-size: 24px; margin: 20px; }
                .online { color: #0f0; }
            </style>
        </head>
        <body>
            <h1>🏴‍☠️ Monkey D. Luffy Music Bot</h1>
            <div class="status">Status: <span class="online">ONLINE</span></div>
            <p>Powered by <strong>@Mad_x_Avi</strong></p>
            <p>Use /play in any group to start listening!</p>
        </body>
    </html>
    """
    return HTMLResponse(html_content)

async def stats(request: Request):
    return JSONResponse({
        "status": "online",
        "bot_name": "Monkey D. Luffy",
        "version": "2.0",
        "author": "@Mad_x_Avi"
    })

app = Starlette(debug=False, routes=[
    Route("/dashboard", dashboard),
    Route("/stats", stats),
])
