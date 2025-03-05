```mermaid
stateDiagram
    [*] --> kDeviceStateIdle : 多种情况下，进入等命模式

    kDeviceStateIdle --> kDeviceStateConnecting : boot_button_.OnClick，touch_button_.OnPressDown，OnWakeWordDetected，OnWakeWordDetected，StartListening
    kDeviceStateConnecting --> kDeviceStateIdle : OpenAudioChannel失败
    kDeviceStateConnecting --> kDeviceStateListening : OpenAudioChannel成功
    kDeviceStateSpeaking --> kDeviceStateListening : 收到server端tts_stop，StartListening
    kDeviceStateIdle --> kDeviceStateSpeaking : 收到server端tts_start
    kDeviceStateListening --> kDeviceStateSpeaking : 收到server端tts_start
