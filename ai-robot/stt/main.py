from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from websocket_manager import websocket_endpoint
import uvicorn
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 允许跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 根据需要调整允许的来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# WebSocket端点
app.websocket("/ws")(websocket_endpoint)

# 响应 index.html
async def serve_index():
    return FileResponse("./index.html")

app.get("/")(serve_index)

# 静态文件支持（可选，如果需要托管更多 HTML/JS 文件）
app.mount("/static", StaticFiles(directory="static"), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7701)

