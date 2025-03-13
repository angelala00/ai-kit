
```mermaid
sequenceDiagram
    participant A as 用户
    participant B as 认证系统
    participant C as 数据库
    participant D as 缓存

    A->>B: 发送登录请求 (用户名, 密码)
    B->>D: 查询缓存 (用户数据)
    
    alt 缓存命中
        D-->>B: 返回用户数据
    else 缓存未命中
        B->>C: 查询数据库 (用户数据)
        C-->>B: 返回用户数据
        B->>D: 存入缓存 (用户数据)
    end

    B->>B: 验证用户密码

    alt 验证成功
        B-->>A: 返回认证成功 + 用户信息
    else 验证失败
        B-->>A: 返回认证失败 (错误信息)
    end

    note over A,B: 用户收到登录结果
