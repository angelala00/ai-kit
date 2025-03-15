import websockets
import asyncio
import json


asr_channel_init_and_recv_task = None

asr_websocket = None

asr_websocket_recognizing_callback = None
asr_websocket_recognized_callback = None

asr_status = ""

async def close_asr_channels():
    global asr_websocket
    global asr_channel_init_and_recv_task
    if asr_websocket:
        try:
            await asr_websocket.close()
            print("websocket closed.")
        except Exception as e:
            print(f"Error closing websocket: {e}")
        finally:
            asr_websocket = None

    if asr_channel_init_and_recv_task:
        asr_channel_init_and_recv_task.cancel()
        try:
            await asr_channel_init_and_recv_task
        except asyncio.CancelledError:
            print("asr_channel_init_and_recv_task cancelled.")
        finally:
            asr_channel_init_and_recv_task = None

def initialize_asr_channels():
    global asr_channel_init_and_recv_task
    asr_channel_init_and_recv_task = asyncio.create_task(get_asr_channel())

async def get_asr_channel():
    global asr_websocket
    asr_websocket = await websockets.connect("ws://127.0.0.1:7701/ws")
    print("Connected to WebSocket server for audio streaming")

    dic = {}

    try:
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
    except websockets.exceptions.ConnectionClosed as e:
        print("Websocket connection closed:", e)
    except Exception as e:
        print("Other error:", e)