import os
from openai import OpenAI
import third.tts as tts

client = OpenAI(
    # 若没有配置环境变量，请用百炼API Key将下行替换为：api_key="sk-xxx",
    api_key="sk-8a79301a5b814bb3b986d4e81f9fe21c",
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
)


def chat_with_query(query):
    completion = client.chat.completions.create(
        model="qwen-plus",
        messages=[
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': query}
        ],
        stream=True,
        stream_options={"include_usage": True}
    )
    for chunk in completion:
        if len(chunk.choices) > 0:
            if chunk.choices[0].finish_reason != 'stop':
                if tts.synthesizer:
                    tts.synthesizer.streaming_call(chunk.choices[0].delta.content)
                else:
                    print(f"llm_complations_callback not inited, ignore. content:{chunk.choices[0].delta.content}")
            else:
                if tts.synthesizer:
                    tts.synthesizer.streaming_complete()
                else:
                    print("llm_complations_stop_callback not inited, ignore.")