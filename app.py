#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
时空胶囊 - 后端API服务
使用Flask + SQLite，轻量级部署方案
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from datetime import datetime, timedelta
import sqlite3
import os
import json

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# 数据库文件
DB_PATH = os.path.join(os.path.dirname(__file__), 'capsules.db')

def init_db():
    """初始化数据库"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS capsules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            capsule_id TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            theme TEXT NOT NULL,
            message TEXT NOT NULL,
            goal TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            open_date DATE NOT NULL,
            is_opened BOOLEAN DEFAULT 0,
            teacher_id TEXT,
            remarks TEXT
        )
    ''')
    conn.commit()
    conn.close()

def generate_capsule_id():
    """生成胶囊编号"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    import random
    random_str = ''.join([str(random.randint(0, 9)) for _ in range(4)])
    return f'TC{timestamp}{random_str}'

@app.route('/')
def index():
    """返回前端页面"""
    return send_from_directory('.', 'index.html')

@app.route('/api/capsule', methods=['POST'])
def create_capsule():
    """创建时空胶囊"""
    try:
        data = request.get_json()

        # 验证必填字段
        required_fields = ['name', 'age', 'theme', 'message', 'goal']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'success': False, 'error': f'缺少必填字段: {field}'}), 400

        capsule_id = generate_capsule_id()
        open_date = (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d')

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''
            INSERT INTO capsules (capsule_id, name, age, theme, message, goal, open_date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (capsule_id, data['name'], data['age'], data['theme'],
              data['message'], data['goal'], open_date))

        conn.commit()
        conn.close()

        return jsonify({
            'success': True,
            'capsuleId': capsule_id,
            'openDate': open_date
        })

    except Exception as e:
        print(f'Error creating capsule: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/capsules', methods=['GET'])
def get_capsules():
    """获取所有胶囊（辅导老师端）"""
    try:
        # 可选：按teacher_id筛选
        teacher_id = request.args.get('teacher_id')

        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        if teacher_id:
            cursor.execute('''
                SELECT * FROM capsules WHERE teacher_id = ? ORDER BY created_at DESC
            ''', (teacher_id,))
        else:
            cursor.execute('SELECT * FROM capsules ORDER BY created_at DESC')

        rows = cursor.fetchall()
        conn.close()

        capsules = []
        for row in rows:
            capsules.append({
                'id': row['id'],
                'capsule_id': row['capsule_id'],
                'name': row['name'],
                'age': row['age'],
                'theme': row['theme'],
                'message': row['message'],
                'goal': row['goal'],
                'created_at': row['created_at'],
                'open_date': row['open_date'],
                'is_opened': bool(row['is_opened']),
                'teacher_id': row['teacher_id'],
                'remarks': row['remarks']
            })

        return jsonify({'success': True, 'capsules': capsules})

    except Exception as e:
        print(f'Error getting capsules: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/capsule/<capsule_id>', methods=['GET'])
def get_capsule(capsule_id):
    """获取单个胶囊详情"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM capsules WHERE capsule_id = ?', (capsule_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return jsonify({'success': False, 'error': '胶囊不存在'}), 404

        capsule = {
            'id': row['id'],
            'capsule_id': row['capsule_id'],
            'name': row['name'],
            'age': row['age'],
            'theme': row['theme'],
            'message': row['message'],
            'goal': row['goal'],
            'created_at': row['created_at'],
            'open_date': row['open_date'],
            'is_opened': bool(row['is_opened']),
            'teacher_id': row['teacher_id'],
            'remarks': row['remarks']
        }

        return jsonify({'success': True, 'capsule': capsule})

    except Exception as e:
        print(f'Error getting capsule: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/capsule/<capsule_id>', methods=['PUT'])
def update_capsule(capsule_id):
    """更新胶囊（添加备注、标记为已打开等）"""
    try:
        data = request.get_json()

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 支持更新备注、老师ID、打开状态
        update_fields = []
        update_values = []

        if 'is_opened' in data:
            update_fields.append('is_opened = ?')
            update_values.append(1 if data['is_opened'] else 0)

        if 'teacher_id' in data:
            update_fields.append('teacher_id = ?')
            update_values.append(data['teacher_id'])

        if 'remarks' in data:
            update_fields.append('remarks = ?')
            update_values.append(data['remarks'])

        if not update_fields:
            conn.close()
            return jsonify({'success': False, 'error': '没有可更新的字段'}), 400

        update_values.append(capsule_id)
        cursor.execute(f'''
            UPDATE capsules SET {', '.join(update_fields)} WHERE capsule_id = ?
        ''', update_values)

        conn.commit()
        conn.close()

        return jsonify({'success': True})

    except Exception as e:
        print(f'Error updating capsule: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/export', methods=['GET'])
def export_capsules():
    """导出胶囊数据（CSV格式）"""
    try:
        teacher_id = request.args.get('teacher_id')

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if teacher_id:
            cursor.execute('''
                SELECT * FROM capsules WHERE teacher_id = ? ORDER BY created_at DESC
            ''', (teacher_id,))
        else:
            cursor.execute('SELECT * FROM capsules ORDER BY created_at DESC')

        rows = cursor.fetchall()
        conn.close()

        # 生成CSV内容
        csv_lines = ['胶囊编号,姓名,年龄,主题,给未来的自己,学习目标,创建时间,开启日期,辅导老师ID,备注']

        theme_names = {
            'algorithm': '算法工程师',
            'game': '游戏开发工程师',
            'ai': 'AI科学家'
        }

        for row in rows:
            csv_lines.append(','.join([
                row[1],  # capsule_id
                row[2],  # name
                str(row[3]),  # age
                theme_names.get(row[4], row[4]),  # theme
                f'"{row[5]}"',  # message
                f'"{row[6]}"',  # goal
                row[7],  # created_at
                row[8],  # open_date
                row[10] or '',  # teacher_id
                f'"{row[11] or ""}"'  # remarks
            ]))

        from flask import Response
        return Response(
            '\n'.join(csv_lines),
            mimetype='text/csv',
            headers={'Content-Disposition': 'attachment; filename=capsules_export.csv'}
        )

    except Exception as e:
        print(f'Error exporting: {e}')
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # 初始化数据库
    init_db()

    # 启动服务
    print('=' * 50)
    print('🚀 时空胶囊API服务启动')
    print('=' * 50)
    print('访问地址: http://localhost:8080')
    print('API文档:')
    print('  POST   /api/capsule          - 创建胶囊')
    print('  GET    /api/capsules          - 获取所有胶囊')
    print('  GET    /api/capsule/<id>      - 获取胶囊详情')
    print('  PUT    /api/capsule/<id>      - 更新胶囊')
    print('  GET    /api/export            - 导出数据')
    print('=' * 50)

    app.run(host='0.0.0.0', port=8080, debug=True)
