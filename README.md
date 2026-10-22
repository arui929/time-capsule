# 🚀 C++编程之旅 · 时空胶囊

一个低成本的H5互动工具，用于辅导老师首次添加微信时与家长/孩子互动。

## ✨ 功能特点

- 🎨 **酷炫视觉**：星空主题、流星动画、胶囊浮动效果
- 📝 **写信功能**：给半年后的自己写期待和目标
- 💾 **数据存储**：SQLite数据库，支持导出CSV
- 🔢 **专属编号**：每个胶囊有唯一编号，便于查找
- 📅 **到期提醒**：自动计算半年后的开启日期

## 🚀 快速开始

### 1. 安装依赖

```bash
cd 时空胶囊
pip3 install -r requirements.txt
```

### 2. 启动服务

```bash
python3 app.py
```

服务启动后，访问：http://localhost:5000

### 3. 本地测试

浏览器打开 http://localhost:5000 即可看到前端页面。

填写表单后，数据会保存到 `capsules.db` 文件中。

## 📊 数据管理

### 查看所有胶囊

访问：http://localhost:5000/api/capsules

返回JSON格式的所有胶囊数据。

### 按辅导老师筛选

http://localhost:5000/api/capsules?teacher_id=T001

### 导出CSV

http://localhost:5000/api/export?teacher_id=T001

可以直接用Excel打开，用于续报/防退费等场景。

### 更新胶囊状态

```bash
# 标记为已打开
curl -X PUT http://localhost:5000/api/capsule/TC123456789012 \
  -H "Content-Type: application/json" \
  -d '{"is_opened": true, "remarks": "已续报成功"}'
```

## 🌐 部署方案

### 方案1：局域网部署（最简单）

在一台电脑上运行服务，其他设备通过局域网访问。

```bash
# 启动服务
python3 app.py
```

手机访问：http://你的IP地址:5000

### 方案2：云服务器部署（推荐）

购买一台轻量云服务器（如腾讯云、阿里云），安装Python环境后部署。

```bash
# 上传代码到服务器
scp -r 时空胶囊 root@服务器IP:/opt/

# SSH连接服务器
ssh root@服务器IP

# 安装依赖
cd /opt/时空胶囊
pip3 install -r requirements.txt

# 使用nohup后台运行
nohup python3 app.py > app.log 2>&1 &

# 或者使用screen
screen -S capsule
python3 app.py
# 按Ctrl+A, D 脱离
```

### 方案3：使用PythonAnywhere（免费）

1. 注册 https://www.pythonanywhere.com
2. 上传代码
3. 配置Web App，指向 app.py
4. 获得免费域名：https://你的用户名.pythonanywhere.com

## 📱 使用流程

### 辅导老师使用

1. 首次添加家长微信时，发送链接
2. 邀请家长/孩子填写时空胶囊
3. 家长填写完成后，截图保存
4. 辅导老师后台导出数据

### 续报/防退费场景

半年后：
1. 导出该学生的胶囊数据
2. 对比学习成果与当初目标
3. 打感情牌沟通："还记得半年前你写的目标吗？我们已经实现了..."

## 🎨 自定义

### 修改主题

编辑 `index.html` 中的主题选项：

```html
<div class="theme-item" data-theme="space">
    <div class="theme-icon">🚀</div>
    <div>太空探险</div>
</div>
```

可以添加更多主题，如：
- 🏆 竞赛达人
- 🎨 动画导演
- 💻 网站开发者

### 修改颜色

编辑 `index.html` 中的CSS变量：

```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

## 🔧 API文档

### POST /api/capsule - 创建胶囊

请求体：
```json
{
    "name": "小明",
    "age": 10,
    "theme": "space",
    "message": "我想成为宇航员...",
    "goal": "学会用C++做游戏"
}
```

响应：
```json
{
    "success": true,
    "capsuleId": "TC202601211530001234",
    "openDate": "2026-07-21"
}
```

### GET /api/capsules - 获取所有胶囊

可选参数：`teacher_id`

### GET /api/capsule/<capsule_id> - 获取胶囊详情

### PUT /api/capsule/<capsule_id> - 更新胶囊

请求体：
```json
{
    "is_opened": true,
    "teacher_id": "T001",
    "remarks": "续报成功"
}
```

### GET /api/export - 导出数据

可选参数：`teacher_id`

## 📝 数据备份

数据存储在 `capsules.db` 文件中，定期备份此文件即可。

## ❓ 常见问题

**Q: 手机如何访问？**
A: 确保手机和电脑在同一WiFi下，访问 http://电脑IP:5000

**Q: 如何查看数据？**
A: 访问 http://localhost:5000/api/capsules 或查看 capsules.db

**Q: 如何部署到线上？**
A: 推荐使用PythonAnywhere（免费）或轻量云服务器

**Q: 可以修改填写内容吗？**
A: 前端页面可以自定义，修改 index.html 即可

## 📞 技术支持

如有问题，请联系技术支持。
