import asyncio
from fastapi import WebSocket, WebSocketDisconnect
import uuid
import json
from models import sessions, Session
from speech_recognition import recognizer, RecognizerStream, streams


# 发送session_id给前端
async def send_session_id(websocket: WebSocket, session_id: str):
    await websocket.send_text(json.dumps({
        "type": "session",
        "session_id": session_id
    }))


# WebSocket连接处理
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = str(uuid.uuid4())
    try:
        session = Session(session_id, websocket)
        sessions[session_id] = session
        stream = recognizer.create_stream()
        recognizer_stream = RecognizerStream(session_id, stream)
        streams[session_id] = recognizer_stream
        # 启动输入和输出处理器
        asyncio.create_task(input_processor(session))
        asyncio.create_task(output_processor(session))
        # 监听消息
        while True:
            data = await websocket.receive_bytes()
            await session.input_queue.put(data)
    except WebSocketDisconnect:
        if session_id and session_id in sessions:
            del sessions[session_id]


# 输入处理器（针对每个会话）
async def input_processor(session: Session):
    while True:
        data = await session.input_queue.get()
        stream = streams[session.session_id]
        await stream.recognition_stream(session, data)


# 输出处理器（针对每个会话）
async def output_processor(session: Session):
    while True:
        message = await session.output_queue.get()
        await session.websocket.send_text(json.dumps(message))

