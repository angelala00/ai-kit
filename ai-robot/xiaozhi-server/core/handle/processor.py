from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse


async def handle_json_message(websocket: WebSocket, data: dict):
    """处理 JSON 消息"""
    msg_type = data.get("type", "")

    if msg_type == "hello":
        response = {
            "type": "hello_response",
            "version": 1,
            "transport": "websocket",
            "audio_params": {"format": "opus", "sample_rate": 16000, "channels": 1, "frame_duration": 20}
        }
    
    elif msg_type == "abort":
        response = {"type": "abort_response", "session_id": data.get("session_id", ""), "message": "Speech aborted"}

    elif msg_type == "listen":
        state = data.get("state")
        if state == "detect":
            response = {"type": "listen_response", "state": "detect", "text": data.get("text", "")}
        elif state == "start":
            response = {"type": "listen_response", "state": "start", "mode": data.get("mode", "unknown")}
        elif state == "stop":
            response = {"type": "listen_response", "state": "stop"}
        else:
            response = {"status": "error", "message": "Unknown listen state"}

    elif msg_type == "iot":
        if "descriptors" in data:
            response = {"type": "iot_response", "descriptors": data["descriptors"]}
        elif "states" in data:
            response = {"type": "iot_response", "states": data["states"]}
        else:
            response = {"status": "error", "message": "Invalid IoT data"}

    else:
        response = {"status": "error", "message": "Unknown message type"}

    await websocket.send_text(json.dumps(response))


async def handle_audio_stream(websocket: WebSocket, binary_data: bytes):
    """处理二进制语音流"""
    print(f"Received binary audio data, length: {len(binary_data)} bytes")
    
    # 这里可以添加音频处理逻辑，比如：
    # - 将 OPUS 数据转换为 PCM
    # - 发送给语音识别 ASR 服务

    # 临时返回一个简单的响应
    await websocket.send_text(json.dumps({"type": "audio_received", "length": len(binary_data)}))
