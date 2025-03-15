import time
import dashscope
from dashscope.api_entities.dashscope_response import SpeechSynthesisResponse
from dashscope.audio.tts_v2 import *
import asyncio

from datetime import datetime


tts_on_open_callback = None
tts_on_data_callback = None
tts_on_close_callback = None



def get_timestamp():
    now = datetime.now()
    formatted_timestamp = now.strftime("[%Y-%m-%d %H:%M:%S.%f]")
    return formatted_timestamp

# 若没有将API Key配置到环境变量中，需将your-api-key替换为自己的API Key
dashscope.api_key = "sk-8a79301a5b814bb3b986d4e81f9fe21c"

model = "cosyvoice-v1"
#voice = "longxiaochun"
voice = "loongstella"


class Callback(ResultCallback):
    # _player = None
    # _stream = None

    def on_open(self):
        print("websocket is open.")
        tts_on_open_callback()
        # self._player = pyaudio.PyAudio()
        # self._stream = self._player.open(
        #     format=pyaudio.paInt16, channels=1, rate=16000, output=True, frames_per_buffer=1024
        # )

    def on_complete(self):
        print(get_timestamp() + " speech synthesis task complete successfully.")

    def on_error(self, message: str):
        print(f"speech synthesis task failed, {message}")

    def on_close(self):
        print(get_timestamp() + " websocket is closed.")
        tts_on_close_callback()
        # # 停止播放器
        # self._stream.stop_stream()
        # self._stream.close()
        # self._player.terminate()

    def on_event(self, message):
        pass

    def on_data(self, data: bytes) -> None:
        print(get_timestamp() + " audio result length: " + str(len(data)))
        tts_on_data_callback(data)
        # self._stream.write(data)


callback = Callback()
# test_text = [
#     "流式文本语音合成SDK，",
#     "可以将输入的文本",
#     "合成为语音二进制数据，",
#     "相比于非流式语音合成，",
#     "流式合成的优势在于实时性",
#     "更强。用户在输入文本的同时",
#     "可以听到接近同步的语音输出，",
#     "极大地提升了交互体验，",
#     "减少了用户等待时间。",
#     "适用于调用大规模",
#     "语言模型（LLM），以",
#     "流式输入文本的方式",
#     "进行语音合成的场景。",
# ]

synthesizer = None
tts_init_task = None
def init_synthesizer():
    tts_init_task = asyncio.create_task(create_synthesizer())

async def create_synthesizer():
    global synthesizer
    synthesizer = SpeechSynthesizer(
        model=model,
        voice=voice,
        #format=AudioFormat.PCM_22050HZ_MONO_16BIT,
        format=AudioFormat.PCM_16000HZ_MONO_16BIT,
        callback=callback,
    )


# for text in test_text:
#     synthesizer.streaming_call(text)
#     time.sleep(0.1)
# synthesizer.streaming_complete()

# print('[Metric] requestId: {}, first package delay ms: {}'.format(
#     synthesizer.get_last_request_id(),
#     synthesizer.get_first_package_delay()))
# synthesizer.streaming_call("再次测试")
