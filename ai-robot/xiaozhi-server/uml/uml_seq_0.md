```mermaid
sequenceDiagram
    participant A as ESP32S3
    participant B as Server
    participant C as ASR-Server
    participant D as TTS-Server
    participant E as LLM-Server
    


    A->>B: hello ping
    B-->>A: hello pong
    B->>C: Init ping
    C-->>B: Init pong
    B->>D: Init ping
    D-->>B: Init pong
    B->>E: Init ping
    E-->>B: Init pong


    A->>B: start_listening
    A->>B: 音频流
    B->>C: 实时检测
    C-->>B: 检测到一句话
    loop 多次调用模型，无function_call直接退出
        B->>E: 调用大模型（with prompt and functions）
        E-->>B: 大模型返回
        alt 是否需要
            B->>B: 调用function_call
        end
    end
    B->>D: 语音生成（with config）
    D-->>B: 返回语音
    
    B-->>A: tts_start
    B-->>A: 音频流
    B-->>A: tts_end



