from fastapi import FastAPI
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import uvicorn
import core.handel.processor

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
    try:
        while True:
            message = await websocket.receive()
            if "text" in message:
                text_data = message["text"]
                print("Received text:", text_data)
                try:
                    json_data = json.loads(text_data)
                    await processor.handle_json_message(websocket, json_data)
                except json.JSONDecodeError:
                    await websocket.send_text(json.dumps({"status": "error", "message": "Invalid JSON format"}))
            elif "bytes" in message:
                binary_data = message["bytes"]
                await processor.handle_audio_stream(websocket, binary_data)
    except WebSocketDisconnect:
        print("Client disconnected")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)