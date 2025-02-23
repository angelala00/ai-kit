http://182.92.219.73:8000/health


http://182.92.219.73:8000/xiaozhi/v1


https://api.toolool.com/xiaozhi/v1/


wscat -c wss://api.toolool.com/xiaozhi/v1/


wscat -c wss://api.toolool.com/xiaozhi/v -H "Authorization: Bearer YOUR_TOKEN_HERE"



client发送/服务端接收
语音
    二进制语音数据
hello
    "{\"type\":\"hello\",\"version\": 1,\"transport\":\"websocket\",\"audio_params\":{\"format\":\"opus\", \"sample_rate\":16000, \"channels\":1, \"frame_duration\":" + std::to_string(OPUS_FRAME_DURATION_MS)}}";
SendAbortSpeaking
    "{\"session_id\":\"" + session_id_ + "\",\"type\":\"abort\"}"
    "{\"session_id\":\"" + session_id_ + "\",\"type\":\"abort\",\"reason\":\"wake_word_detected\"}"
SendWakeWordDetected
    "{\"session_id\":\"" + session_id_ + "\",\"type\":\"listen\",\"state\":\"detect\",\"text\":\"" + wake_word + "\"}"
SendStartListening
    "{\"session_id\":\"" + session_id_ + "\",\"type\":\"listen\",\"state\":\"start\",\"mode\":\"realtime\"}"
    "{\"session_id\":\"" + session_id_ + "\",\"type\":\"listen\",\"state\":\"start\",\"mode\":\"auto\"}"
    "{\"session_id\":\"" + session_id_ + "\",\"type\":\"listen\",\"state\":\"start\",\"mode\":\"manual\"}"
SendStopListening
    "{\"session_id\":\"" + session_id_ + "\",\"type\":\"listen\",\"state\":\"stop\"}"
SendIotDescriptors
    "{\"session_id\":\"" + session_id_ + "\",\"type\":\"iot\",\"descriptors\":" + descriptors + "}"
SendIotStates
    "{\"session_id\":\"" + session_id_ + "\",\"type\":\"iot\",\"states\":" + states + "}";

client接收/服务端发送
语音
    进制制语音数据
hello
    "{\"type\":\"hello\"}"  transport  ??
tts:start
    "{\"type\":\"tts\"}"
tts:stop
    "{\"type\":\"tts\"}"
tts:sentence_start
    "{\"type\":\"tts\"}"
stt:text
llm:emotion
iot:commands


OnIncomingJson