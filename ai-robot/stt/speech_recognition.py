from models import Session
import sherpa_onnx
import numpy as np


streams = {}

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
    print("recognizer inited")
    return recognizer


recognizer = create_recognizer()


class RecognizerStream:
    def __init__(self, session_id: str, stream: any):
        self.session_id = session_id
        self.sample_rate = 48000
        self.last_result = ""
        self.segment_id = 0
        self.stream = stream

    async def recognition_stream(self, session: Session, data: any):
        try:
            # print("data 的长度 (字节数):", len(data))
            samples = np.frombuffer(data, dtype=np.float32)
            # print("samples 的形状:", samples.shape)

            self.stream.accept_waveform(self.sample_rate, samples)
            while recognizer.is_ready(self.stream):
                recognizer.decode_stream(self.stream)

            is_endpoint = recognizer.is_endpoint(self.stream)
            result = recognizer.get_result(self.stream)

            if result and (self.last_result != result):
                self.last_result = result
                # 将回复放入输出队列
                print(f"segment_id:{self.segment_id}, stage:recognizing, result:{result}")
                await session.output_queue.put({"type": "text", "segment_id": self.segment_id, "stage": "recognizing", "content": result})
            if is_endpoint:
                if result:
                    print(f"segment_id:{self.segment_id}, stage:endpoint, result:{result}")
                    await session.output_queue.put({"type": "text", "segment_id": self.segment_id, "stage": "endpoint", "content": result})
                    self.segment_id += 1
                recognizer.reset(self.stream)
        except Exception as e:
            print(f"Connection closed: {e}")
