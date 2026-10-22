#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
本地测试脚本 - 验证时空胶囊完整流程
"""

import requests
import json
import time

BASE_URL = 'http://localhost:8080'

def test_create_capsule():
    """测试创建胶囊"""
    print('\n' + '='*50)
    print('测试1: 创建时空胶囊')
    print('='*50)

    data = {
        'name': '测试小明',
        'age': 10,
        'theme': 'space',
        'message': '我想成为宇航员，探索宇宙的奥秘！',
        'goal': '学会用C++做一个太空游戏'
    }

    print(f'\n提交数据: {json.dumps(data, ensure_ascii=False, indent=2)}')

    try:
        response = requests.post(f'{BASE_URL}/api/capsule', json=data)
        result = response.json()

        print(f'\n响应: {json.dumps(result, ensure_ascii=False, indent=2)}')

        if result.get('success'):
            print('\n✅ 创建成功！')
            return result.get('capsuleId')
        else:
            print('\n❌ 创建失败！')
            return None
    except Exception as e:
        print(f'\n❌ 请求失败: {e}')
        return None

def test_get_capsules(capsule_id):
    """测试获取胶囊"""
    print('\n' + '='*50)
    print('测试2: 获取所有胶囊')
    print('='*50)

    try:
        response = requests.get(f'{BASE_URL}/api/capsules')
        result = response.json()

        if result.get('success'):
            capsules = result.get('capsules', [])
            print(f'\n✅ 获取成功！共 {len(capsules)} 个胶囊')

            for c in capsules:
                print(f'\n- 编号: {c["capsule_id"]}')
                print(f'  姓名: {c["name"]}')
                print(f'  年龄: {c["age"]}岁')
                print(f'  主题: {c["theme"]}')
                print(f'  目标: {c["goal"]}')
                print(f'  创建时间: {c["created_at"]}')
                print(f'  开启日期: {c["open_date"]}')
        else:
            print('\n❌ 获取失败！')
    except Exception as e:
        print(f'\n❌ 请求失败: {e}')

def test_get_single_capsule(capsule_id):
    """测试获取单个胶囊"""
    print('\n' + '='*50)
    print('测试3: 获取单个胶囊详情')
    print('='*50)

    if not capsule_id:
        print('\n⚠️ 没有可用的胶囊ID，跳过此测试')
        return

    try:
        response = requests.get(f'{BASE_URL}/api/capsule/{capsule_id}')
        result = response.json()

        if result.get('success'):
            capsule = result.get('capsule')
            print(f'\n✅ 获取成功！')
            print(f'\n胶囊详情:')
            print(f'  编号: {capsule["capsule_id"]}')
            print(f'  姓名: {capsule["name"]}')
            print(f'  年龄: {capsule["age"]}岁')
            print(f'  主题: {capsule["theme"]}')
            print(f'  给未来的自己: {capsule["message"]}')
            print(f'  学习目标: {capsule["goal"]}')
            print(f'  创建时间: {capsule["created_at"]}')
            print(f'  开启日期: {capsule["open_date"]}')
        else:
            print(f'\n❌ 获取失败: {result.get("error")}')
    except Exception as e:
        print(f'\n❌ 请求失败: {e}')

def test_update_capsule(capsule_id):
    """测试更新胶囊"""
    print('\n' + '='*50)
    print('测试4: 更新胶囊状态')
    print('='*50)

    if not capsule_id:
        print('\n⚠️ 没有可用的胶囊ID，跳过此测试')
        return

    data = {
        'is_opened': True,
        'teacher_id': 'T001',
        'remarks': '测试备注：续报成功'
    }

    print(f'\n更新数据: {json.dumps(data, ensure_ascii=False, indent=2)}')

    try:
        response = requests.put(f'{BASE_URL}/api/capsule/{capsule_id}', json=data)
        result = response.json()

        if result.get('success'):
            print('\n✅ 更新成功！')
        else:
            print(f'\n❌ 更新失败: {result.get("error")}')
    except Exception as e:
        print(f'\n❌ 请求失败: {e}')

def test_export():
    """测试导出数据"""
    print('\n' + '='*50)
    print('测试5: 导出数据')
    print('='*50)

    try:
        response = requests.get(f'{BASE_URL}/api/export')
        print(f'\n✅ 导出成功！')
        print(f'\nCSV内容:\n{response.text[:500]}...')
    except Exception as e:
        print(f'\n❌ 请求失败: {e}')

def main():
    print('\n' + '='*60)
    print('🚀 时空胶囊API测试脚本')
    print('='*60)
    print(f'\n服务地址: {BASE_URL}')
    print('\n请确保已启动服务: python3 app.py')
    time.sleep(1)

    # 测试1: 创建胶囊
    capsule_id = test_create_capsule()

    # 等待1秒
    time.sleep(1)

    # 测试2: 获取所有胶囊
    test_get_capsules(capsule_id)

    # 测试3: 获取单个胶囊
    test_get_single_capsule(capsule_id)

    # 测试4: 更新胶囊
    test_update_capsule(capsule_id)

    # 测试5: 导出数据
    test_export()

    print('\n' + '='*60)
    print('✅ 所有测试完成！')
    print('='*60)
    print('\n💡 提示:')
    print('  1. 浏览器访问 http://localhost:8080 查看前端页面')
    print('  2. 数据已保存到 capsules.db')
    print('  3. 访问 http://localhost:8080/api/capsules 查看数据')
    print()

if __name__ == '__main__':
    main()
