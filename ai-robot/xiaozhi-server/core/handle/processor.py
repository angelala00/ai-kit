from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
import json
import websockets
import numpy as np
import opuslib

import third.stt as stt


websocket = None


async def tts_start_callback():
    response = {"type": "tts", "state": "start"}
    send_string = json.dumps(response)
    print("Sending text:", send_string)
    await websocket.send_text(send_string)

async def tts_byte_callback(data):
    await websocket.send(data)

async def tts_end_callback():
    response = {"type": "tts", "state": "start"}
    send_string = json.dumps(response)
    print("Sending text:", send_string)
    await websocket.send_text(send_string)

async def handle_json_message(data: dict):
    """处理 JSON 消息"""
    msg_type = data.get("type", "")

    if msg_type == "hello":
        response = {
            "type": "hello",
            "transport": "websocket",
            "audio_params": {"sample_rate": 16000}
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

    send_test_string = json.dumps(response)
    print("Sending text:", send_test_string)
    await websocket.send_text(send_test_string)


# 全局缓冲区，用于累计转换后的 float32 PCM 数据
sample_buffer = np.array([], dtype=np.float32)

# 初始化 opus 解码器：采样率 16000，单声道
opus_decoder = opuslib.Decoder(16000, 1)

async def handle_audio_stream(binary_data: bytes):
    """
    处理来自硬件设备的 opus 格式音频数据，将其解码、转换为 float32 PCM 后，
    按固定块大小发送给后端的 STT 服务(asr_websocket)
    
    参数:
      websocket: 与硬件设备的连接（如果需要回复硬件设备，可以使用）
      binary_data: 从硬件设备接收到的 opus 二进制数据
      asr_websocket: 后端 STT 服务的 websocket 连接
    """
    global sample_buffer
    try:
        # 计算每帧应有的采样点数：
        # 采样率为 16000，帧时长 60ms -> 16000 * 0.06 = 960 个采样点
        frame_samples = 960

        # 使用 opus 解码器解码二进制数据，得到 PCM 数据（int16）
        pcm_data = opus_decoder.decode(binary_data, frame_samples)
        
        # 将 PCM 数据转换成 numpy 数组（int16）
        samples = np.frombuffer(pcm_data, dtype=np.int16)
        
        # 转换为 float32，并归一化到 [-1, 1]
        samples = samples.astype(np.float32) / 32768.0
        
        # 将转换后的数据添加到缓冲区中
        sample_buffer = np.concatenate([sample_buffer, samples])
        
        # 判断缓冲区中是否累计了足够的数据后再发送
        # 16000hz 60ms 960个采样点，转换成float32之后占1920个字节
        block_size = 1920
        if sample_buffer.size >= block_size:
            print(f"准备发送数据")
            # 取出前 block_size 个采样点
            block = sample_buffer[:block_size]
            # 将剩余数据保留在缓冲区中
            sample_buffer = sample_buffer[block_size:]
            # 发送数据给 STT 服务，转换为字节流
            if stt.asr_channel_task and stt.asr_channel_task.done() and stt.asr_websocket:
                await stt.asr_websocket.send(block.tobytes())
            else:
                print(f"asr_websocket还未准备好，丢弃")
            print(f"完成发送数据")
    except Exception as e:
        print(f"Error handling audio stream: {e}")

    # 临时返回一个简单的响应
    await websocket.send_text(json.dumps({"type": "audio_received", "length": len(binary_data)}))