```mermaid
stateDiagram
    [*] --> kDeviceStateStarting : 设备启动
    kDeviceStateStarting --> kDeviceStateWifiConfiguring : 连网不成功等三种情况，进入配网模式
    kDeviceStateWifiConfiguring --> kDeviceStateUpgrading : 配网成功，检查升级

    kDeviceStateStarting --> kDeviceStateUpgrading : 连网成功，检查升级


    kDeviceStateUpgrading --> kDeviceStateStarting : 更新成功（设备重启）
