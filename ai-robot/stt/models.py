from typing import Dict, List, Any
from fastapi import WebSocket
import asyncio


# 会话类
class Session:
    def __init__(self, session_id: str, websocket: WebSocket):
        self.session_id = session_id
        self.websocket = websocket
        self.input_queue = asyncio.Queue()
        self.output_queue = asyncio.Queue()
        self.history: List[Dict[str, Any]] = []


# 会话管理
sessions: Dict[str, Session] = {}
