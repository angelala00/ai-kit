```mermaid
stateDiagram
    [*] --> kDeviceStateIdle : 系统启动后,配网,更新,进入待命模式，OnNetworkError，OnAudioChannelClosed

    kDeviceStateIdle --> kDeviceStateConnecting : boot_button_.OnClick(ToggleChatState)，touch_button_.OnPressDown(StartListening)，OnWakeWordDetected
    kDeviceStateConnecting --> kDeviceStateIdle : OpenAudioChannel失败
    kDeviceStateConnecting --> kDeviceStateListening : OpenAudioChannel成功
    kDeviceStateSpeaking --> kDeviceStateListening : 收到server端tts_stop(!keep_listening_)，touch_button_.OnPressDown(StartListening)
    kDeviceStateSpeaking --> kDeviceStateIdle : 收到server端tts_stop(keep_listening_)
    kDeviceStateIdle --> kDeviceStateSpeaking : 收到server端tts_start
    kDeviceStateListening --> kDeviceStateSpeaking : 收到server端tts_start
    kDeviceStateListening --> kDeviceStateIdle : touch_button_.OnPressUp(StopListening)
