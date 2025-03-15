import sys
import websockets
import sounddevice as sd
import asyncio
import json


async def receive_messages(websocket):
    while True:
        # 接收数据
        message = await websocket.recv()
        # 检查数据类型
        if isinstance(message, str):
            # 如果是文本数据，直接解析 JSON
            data = json.loads(message)
            print(f"Parsed JSON: {data}")
        else:
            print("Unknown data type received")


async def main():
    websocket = await websockets.connect("ws://127.0.0.1:7701/ws")
    print("Connected to WebSocket server for audio streaming")
    asyncio.create_task(receive_messages(websocket))

    devices = sd.query_devices()
    if len(devices) == 0:
        print("No microphone devices found")
        sys.exit(0)
    print(devices)
    print(f'Use default device: {devices[sd.default.device[0]]["name"]}')
    print(f'default device info: {devices[sd.default.device[0]]}')

    sample_rate = 48000
    samples_per_read = int(0.1 * sample_rate)  # 0.1 second = 100 ms

    with sd.InputStream(channels=1, dtype="float32", samplerate=sample_rate) as s:
        while True:
            samples, _ = s.read(samples_per_read)
            # print("samples 的形状:", samples.shape)
            samples = samples.reshape(-1)
            # print("samples 的形状:", samples.shape)
            samples_bytes = samples.tobytes()
            # print("len(samples_bytes) 的长度:", len(samples_bytes))
            await websocket.send(samples_bytes)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nCaught Ctrl + C. Exiting")
