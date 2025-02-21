from flask import Flask, request, jsonify
import uuid
from typing import List, Dict
import json

app = Flask(__name__)


# Message 类，表示单个消息
class Message:
    def __init__(self, id: str, conversation_id: str, parent: str, model: str, author: {}, content: {}, children: List[str]):
        self.id = id  # 消息唯一ID
        self.conversation_id = conversation_id  # 会话ID
        self.parent = parent  # 父消息ID
        self.model = model  # 模型
        self.author = author  # 发送者: 'user' 或 'ai'
        self.content = content  # 消息内容
        self.children = children  # 子消息ID


# Conversation 类，表示一个聊天会话
class Conversation:
    def __init__(self, user_id: str, id: str):
        self.user_id = user_id  # 用户ID
        self.id = id  # 会话唯一ID
        self.messages: List[str] = []  # 会话中的消息列表，消息是根消息或提问


# 模拟存储所有会话的字典
conversations = {}
messages = {}


# 假设这是用来模拟文件处理的简单方法
def process_file_chat(file_id, content):
    return "这是什么re2222"

# 假设这是用来模拟文件处理的简单方法
def process_chat(content):
    return "这是什么re11111"


# 处理聊天请求
@app.route('/chat', methods=['POST'])
def handle_chat():
    data = request.json

    conversation_id = data.get("conversation_id",str(uuid.uuid4()))
    conversation = conversations.get(conversation_id)
    if not conversation:
        conversation = Conversation("uid123",conversation_id)
        conversations[conversation_id] = conversation

    model = data.get("model")
    content = data.get("content")
    if not model or not content:
        return jsonify({"error": "Missing required fields model or content"}), 400

    data["id"]=str(uuid.uuid4())

    parent = data.get("parent","0")
    if parent == "0":
        conversation.messages.append(data["id"])
    else:
        if not parent in messages:
            return jsonify({"error": "Missing required fields parent_message"}), 400
        parent_message = messages[parent]
        parent_message.children.append(data["id"])

    message = Message(data["id"],conversation_id,parent,"","user",content,[])
    messages[data["id"]] = message

    content_type = content.get("content_type")
    if content_type == "file_chat":
        file_id = content.get("file_id")
        msg_content = content.get("msg_content")
        if not file_id or not msg_content:
            return jsonify({"error": "Missing msg content or file ID"}), 400
        response = process_file_chat(file_id, msg_content)
    elif content_type == "chat":
        msg_content = content.get("msg_content")
        if not msg_content:
            return jsonify({"error": "Missing chat content"}), 400
        response = process_chat(msg_content)
    else:
        return jsonify({"error": "Unknown content type"}), 400
    response_message = Message(str(uuid.uuid4()),conversation_id,data['id'],model,"assistant",response,[])
    messages[response_message.id] = response_message

    return jsonify({
        "conversation_id": conversation_id,
        "message_id": message.id,
        "response_id": response_message.id
    }), 200


# 获取指定会话的聊天记录
@app.route('/conversation/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    conversation = conversations.get(conversation_id)
    if not conversation:
        return jsonify({"error": "Conversation not found"}), 404

    # 构建消息树的辅助函数
    def build_message_tree(message_id):
        message_data = messages.get(message_id)
        if not message_data:
            return None
        
        # 构建基本消息结构
        message_tree = {
            "id": message_data.id,
            "content": message_data.content,
            "model": message_data.model,
            "author": message_data.author,
            "children": []
        }
        
        # 查找所有以当前消息为父消息的回复
        for msg_id, msg in messages.items():
            if msg.parent == message_id:
                child_tree = build_message_tree(msg_id)
                if child_tree:
                    message_tree["children"].append(child_tree)
        
        return message_tree

    # 获取会话中的所有根消息（没有父消息的消息）
    root_messages = []
    for msg_id, msg in messages.items():
        if msg.conversation_id == conversation_id and msg.parent in ["0", None]:
            tree = build_message_tree(msg_id)
            if tree:
                root_messages.append(tree)

    return jsonify({
        "conversation_id": conversation_id,
        "messages": root_messages
    })


if __name__ == '__main__':
    app.run(debug=True)
