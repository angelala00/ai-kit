```mermaid
sequenceDiagram
    participant A as ESP32S3
    participant B as Server


    A->>B: hello
    B-->>A: hello



    A->>B: abort
    A->>B: listen_start
    A->>B: listen_stop
    A->>B: listen_detect
    A->>B: iot_descriptors
    A->>B: iot_states
    
    B-->>A: tts
    B-->>A: stt
    B-->>A: llm
    B-->>A: setVolume
    B-->>A: command



