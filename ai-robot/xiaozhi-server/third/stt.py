import websockets
import asyncio
import json


asr_channel_init_and_recv_task = None

asr_websocket = None

asr_websocket_recognizing_callback = None
asr_websocket_recognized_callback = None

asr_status = ""

def initialize_asr_channels():
    asr_channel_init_and_recv_task = asyncio.create_task(get_asr_channel())

async def get_asr_channel():
    asr_websocket = await websockets.connect("ws://127.0.0.1:7701/ws")
    print("Connected to WebSocket server for audio streaming")

    dic = {}
    while True:
        # 接收数据
        message = await asr_websocket.recv()
        # 检查数据类型
        if isinstance(message, str):
            # 如果是文本数据，直接解析 JSON
            data = json.loads(message)
            if data["stage"] == "recognizing":
                if asr_websocket_recognizing_callback:
                    asr_websocket_recognizing_callback(json.dumps({"content": data["content"]}))
                else:
                    print(f'asr_websocket_recognizing_callback not inited, ignore. content:{data["content"]}')
            if data["stage"] == "endpoint":
                asr_status = "idle"
                if asr_websocket_recognized_callback:
                    asr_websocket_recognized_callback(json.dumps({"content": data["content"]}))
                else:
                    print(f'asr_websocket_recognized_callback not inited, ignore. content:{data["content"]}')
        else:
            print("Unknown data type received")
    print(f"==you can't see this")

