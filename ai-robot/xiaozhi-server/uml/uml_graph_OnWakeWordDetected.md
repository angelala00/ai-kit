```mermaid
graph TD;
    A[当唤醒词检测到] --> AA{判断状态}
    AA -->|kDeviceStateIdle| B[准备唤醒词音频]
    AA -->|kDeviceStateSpeaking| AB{AbortSpeaking}
    AA -->|kDeviceStateActivating| AC{kDeviceStateIdle}
    B --> C{连接server端?}
    C -->|连接成功| D[获取并发送唤醒词音频]
    C -->|连接失败| E[开始检测模式后退出]
    D --> F[发送唤醒词音频]
    F --> G[设置为Listening模式]
    
