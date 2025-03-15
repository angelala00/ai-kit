from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import uvicorn
import core.handle.processor as processor
import json
import websockets
import third.stt as stt
import third.llm as llm
import third.tts as tts

app = FastAPI()

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok", "message": "Service is running!"})

@app.websocket("/xiaozhi/v1/")
async def websocket_endpoint(websocket: WebSocket):
    print("Received headers:")
    for header, value in websocket.headers.items():
        print(f"==={header}: {value}")

    # authorization_header = websocket.headers.get('Authorization')
    # protocol_version = websocket.headers.get('Protocol-Version')
    # device_id = websocket.headers.get('Device-Id')
    # if authorization_header:
    #     print(f"Authorization header: {authorization_header}")
    # else:
    #     print("Authorization header not found")


    await websocket.accept()
    processor.websocket = websocket
    #初始化asr websocket（异步）
    stt.initialize_asr_channels()
    # print(f"stt.asr_channel_init_and_recv_task:{stt.asr_channel_init_and_recv_task}")
    def asr_recognized_callback(query):
        tts.init_synthesizer()
        tts.tts_on_open_callback = processor.tts_start_callback
        tts.tts_on_data_callback = processor.tts_byte_callback
        tts.tts_on_close_callback = processor.tts_end_callback
        llm.chat_with_query(query)

    stt.asr_websocket_recognized_callback = asr_recognized_callback

    try:
        while True:
            message = await websocket.receive()
            if "text" in message:
                text_data = message["text"]
                print("Received text:", text_data)
                try:
                    json_data = json.loads(text_data)
                    await processor.handle_json_message(json_data)
                except json.JSONDecodeError:
                    await websocket.send_text(json.dumps({"status": "error", "message": "Invalid JSON format"}))
            elif "bytes" in message:
                binary_data = message["bytes"]
                # print(f"Received binary audio data, length: {len(binary_data)} bytes")
                await processor.handle_audio_stream(binary_data)
    except WebSocketDisconnect:
        print("Client disconnected")
    except RuntimeError as e:
        if str(e) == 'Cannot call "receive" once a disconnect message has been received.':
            print("Client disconnected (RuntimeError detected disconnect)")
            # 同样在这里添加断线后的清理逻辑
        else:
            raise e
    finally:
        await stt.close_asr_channels()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)