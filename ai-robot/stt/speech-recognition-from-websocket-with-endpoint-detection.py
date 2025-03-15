from fastapi import FastAPI, WebSocket
import numpy as np
import sherpa_onnx
import uvicorn


def create_recognizer():
    recognizer = sherpa_onnx.OnlineRecognizer.from_transducer(
        tokens="/opt/source/github.com/k2-fsa/sherpa-onnx/sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20/tokens.txt",
        encoder="/opt/source/github.com/k2-fsa/sherpa-onnx/sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20/encoder-epoch-99-avg-1.onnx",
        decoder="/opt/source/github.com/k2-fsa/sherpa-onnx/sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20/decoder-epoch-99-avg-1.onnx",
        joiner="/opt/source/github.com/k2-fsa/sherpa-onnx/sherpa-onnx-streaming-zipformer-bilingual-zh-en-2023-02-20/joiner-epoch-99-avg-1.onnx",
        num_threads=1,
        sample_rate=16000,
        feature_dim=80,
        enable_endpoint_detection=True,
        rule1_min_trailing_silence=2.4,
        rule2_min_trailing_silence=1.2,
        rule3_min_utterance_length=300,  # it essentially disables this rule
        decoding_method="greedy_search",
        provider="cpu",
        hotwords_file="",
        hotwords_score=1.5,
        blank_penalty=0.0,
    )
    return recognizer


# 初始化 FastAPI 应用
app = FastAPI()

recognizer = create_recognizer()

sample_rate = 48000

stream = recognizer.create_stream()

@app.websocket("/ws/recognize")
async def websocket_recognize(websocket: WebSocket):
    """
    使用 WebSocket 接口实现流式识别
    """
    await websocket.accept()
    last_result = ""
    try:
        while True:
            data = await websocket.receive_bytes()
            print(f"receive_bytes:")
            samples = np.frombuffer(data, dtype=np.float32)
            stream.accept_waveform(sample_rate, samples)
            while recognizer.is_ready(stream):
                recognizer.decode_stream(stream)

            is_endpoint = recognizer.is_endpoint(stream)

            result = recognizer.get_result(stream)
            print(f"result: {result}")

            if result and (last_result != result):
                last_result = result
                await websocket.send_text(result)
            if is_endpoint:
                if result:
                    await websocket.send_text(result)
                recognizer.reset(stream)
    except Exception as e:
        print(f"Connection closed: {e}")


if __name__ == "__main__":

    uvicorn.run(app, host="0.0.0.0", port=8000)

