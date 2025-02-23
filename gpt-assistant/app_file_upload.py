from flask import Flask, request, jsonify, send_from_directory
import os
import uuid
import json
from apscheduler.schedulers.background import BackgroundScheduler
import time

app = Flask(__name__)

# 配置
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
FILE_LIFETIME_DAYS = 7  # 可配置的过期时间，单位为天

# 用于存储文件的ID、文件路径和原始文件名的映射的文件路径
MAPPING_FILE_PATH = 'file_mapping.json'

# 判断文件扩展名是否允许
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 加载文件映射
def load_file_mapping():
    if os.path.exists(MAPPING_FILE_PATH):
        with open(MAPPING_FILE_PATH, 'r') as f:
            return json.load(f)
    return {}

# 保存文件映射
def save_file_mapping(file_mapping):
    with open(MAPPING_FILE_PATH, 'w') as f:
        json.dump(file_mapping, f)

# 文件上传接口
@app.route('/upload', methods=['POST'])
def upload_file():
    file_mapping = load_file_mapping()

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # 生成文件ID
        file_id = str(uuid.uuid4())
        # 获取文件扩展名并生成新的文件路径
        file_extension = os.path.splitext(file.filename)[1]
        filename = os.path.join(UPLOAD_FOLDER, file_id + file_extension)
        
        # 保存文件
        try:
            file.save(filename)
        except Exception as e:
            return jsonify({'error': f'File save failed: {str(e)}'}), 500
        
        # 存储文件ID、文件路径和原始文件名的映射
        file_mapping[file_id] = {'filename': file.filename, 'path': filename}
        
        # 保存文件映射
        save_file_mapping(file_mapping)
        
        return jsonify({'message': 'File successfully uploaded', 'file_id': file_id, 'original_filename': file.filename}), 200
    
    return jsonify({'error': 'File type not allowed'}), 400

# 通过文件ID下载文件
@app.route('/file/<file_id>', methods=['GET'])
def get_file(file_id):
    file_mapping = load_file_mapping()

    if file_id not in file_mapping:
        return jsonify({'error': 'File not found'}), 404
    
    file_path = file_mapping[file_id]['path']
    return send_from_directory(os.path.dirname(file_path), os.path.basename(file_path))

# 获取文件的原始文件名
@app.route('/file_name/<file_id>', methods=['GET'])
def get_file_name(file_id):
    file_mapping = load_file_mapping()

    if file_id not in file_mapping:
        return jsonify({'error': 'File not found'}), 404
    
    original_filename = file_mapping[file_id]['filename']
    return jsonify({'file_id': file_id, 'original_filename': original_filename})

# 删除过期文件的函数
def delete_expired_files():
    now = time.time()
    file_mapping = load_file_mapping()

    for file_id, file_data in list(file_mapping.items()):
        file_path = file_data['path']
        if os.path.isfile(file_path):
            file_age = now - os.path.getmtime(file_path)
            if file_age > FILE_LIFETIME_DAYS * 86400:  # 86400是一天的秒数
                os.remove(file_path)
                del file_mapping[file_id]
                print(f"Deleted expired file: {file_id}")
    
    # 删除过期文件后保存文件映射
    save_file_mapping(file_mapping)

# 启动定时任务
scheduler = BackgroundScheduler()
scheduler.add_job(delete_expired_files, 'interval', days=1)  # 每天检查一次
scheduler.start()

if __name__ == '__main__':
    app.run(debug=True)

