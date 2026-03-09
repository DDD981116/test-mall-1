from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
import json
import os

app = Flask(__name__)
app.secret_key = "test_mall_2026_key"
port = int(os.environ.get('PORT', 8080))

# 管理员账号密码
ADMIN_USER = "admin"
ADMIN_PWD = "admin123"

# 商品数据文件
PRODUCTS_FILE = "products.json"

# 初始化30款电器商品（价格10-100元）
def init_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    # 30款电器商品数据
    products = [
        {"id": 1, "name": "迷你电饭煲", "category": "厨房电器", "price": 10, "stock": 100},
        {"id": 2, "name": "电动打蛋器", "category": "厨房电器", "price": 13, "stock": 100},
        {"id": 3, "name": "小型电煮锅", "category": "厨房电器", "price": 16, "stock": 100},
        {"id": 4, "name": "便携榨汁机", "category": "厨房电器", "price": 19, "stock": 100},
        {"id": 5, "name": "电热水壶", "category": "厨房电器", "price": 22, "stock": 100},
        {"id": 6, "name": "微波炉", "category": "厨房电器", "price": 25, "stock": 100},
        {"id": 7, "name": "桌面加湿器", "category": "生活电器", "price": 28, "stock": 100},
        {"id": 8, "name": "小型电风扇", "category": "生活电器", "price": 31, "stock": 100},
        {"id": 9, "name": "手持挂烫机", "category": "生活电器", "price": 34, "stock": 100},
        {"id": 10, "name": "电动牙刷", "category": "生活电器", "price": 37, "stock": 100},
        {"id": 11, "name": "吹风机", "category": "生活电器", "price": 40, "stock": 100},
        {"id": 12, "name": "空气净化器", "category": "生活电器", "price": 43, "stock": 100},
        {"id": 13, "name": "USB小台灯", "category": "办公电器", "price": 46, "stock": 100},
        {"id": 14, "name": "无线鼠标", "category": "办公电器", "price": 49, "stock": 100},
        {"id": 15, "name": "键盘清洁器", "category": "办公电器", "price": 52, "stock": 100},
        {"id": 16, "name": "便携充电宝", "category": "办公电器", "price": 55, "stock": 100},
        {"id": 17, "name": "蓝牙音箱", "category": "办公电器", "price": 58, "stock": 100},
        {"id": 18, "name": "热敏打印机", "category": "办公电器", "price": 61, "stock": 100},
        {"id": 19, "name": "入耳式耳机", "category": "影音电器", "price": 64, "stock": 100},
        {"id": 20, "name": "头戴式耳机", "category": "影音电器", "price": 67, "stock": 100},
        {"id": 21, "name": "手机支架", "category": "影音电器", "price": 70, "stock": 100},
        {"id": 22, "name": "数据线", "category": "影音电器", "price": 73, "stock": 100},
        {"id": 23, "name": "充电器", "category": "影音电器", "price": 76, "stock": 100},
        {"id": 24, "name": "蓝牙接收器", "category": "影音电器", "price": 79, "stock": 100},
        {"id": 25, "name": "智能手环", "category": "智能设备", "price": 82, "stock": 100},
        {"id": 26, "name": "温湿度计", "category": "智能设备", "price": 85, "stock": 100},
        {"id": 27, "name": "智能插座", "category": "智能设备", "price": 88, "stock": 100},
        {"id": 28, "name": "运动相机", "category": "智能设备", "price": 91, "stock": 100},
        {"id": 29, "name": "行车记录仪", "category": "智能设备", "price": 94, "stock": 100},
        {"id": 30, "name": "电子闹钟", "category": "智能设备", "price": 100, "stock": 100}
    ]
    
    with open(PRODUCTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
    return products

# 加载商品数据
products = init_products()

# 创建网页模板（自动生成，不用手动建）
def create_templates():
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    # 首页模板
    index_html = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>测试一号 - 电器商城</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #ff4400; text-align: center; margin-bottom: 30px; }
        .product-card { border: 1px solid #ddd; padding: 15px; margin-bottom: 15px; border-radius: 8px; }
        .product-name { font-size: 18px; margin-bottom: 5px; }
        .product-price { color: red; font-weight: bold; }
        .product-cat { color: #666; font-size: 14px; }
        .admin-link { text-align: center; margin-top: 30px; }
        .admin-link a { color: #ff4400; text-decoration: none; font-size: 16px; }
    </style>
</head>
<body>
    <h1>测试一号电器商城</h1>
    {% for product in products %}
    <div class="product-card">
        <div class="product-name">{{ product.name }}</div>
        <div class="product-cat">分类：{{ product.category }}</div>
        <div class="product-price">价格：¥{{ product.price }}</div>
    </div>
    {% endfor %}
    <div class="admin-link">
        <a href="/admin/login">管理员后台入口</a>
    </div>
</body>
</html>
    '''
    
    # 管理员登录模板
    login_html = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>管理员登录 - 测试一号商城</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
        .login-box { border: 1px solid #ddd; padding: 30px; border-radius: 8px; }
        h2 { text-align: center; color: #ff4400; margin-bottom: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; }
        button { width: 100%; padding: 10px; background: #ff4400; color: white; border: none; border-radius: 4px; cursor: pointer; }
    </style>
</head>
<body>
    <div class="login-box">
        <h2>管理员登录</h2>
        <form method="POST">
            <div class="form-group">
                <label>账号</label>
                <input type="text" name="username" placeholder="admin" required>
            </div>
            <div class="form-group">
                <label>密码</label>
                <input type="password" name="password" placeholder="admin123" required>
            </div>
            <button type="submit">登录</button>
        </form>
    </div>
</body>
</html>
    '''
    
    # 管理员后台模板
    admin_html = '''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>管理后台 - 测试一号商城</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        h1 { color: #ff4400; margin-bottom: 20px; }
        table { width: 100%; border-collapse: collapse; margin-bottom: 20px; }
        th, td { border: 1px solid #ddd; padding: 10px; text-align: left; }
        th { background: #f5f5f5; }
    </style>
</head>
<body>
    <h1>测试一号商城 - 管理员后台</h1>
    <table>
        <tr>
            <th>商品ID</th>
            <th>商品名称</th>
            <th>分类</th>
            <th>价格（元）</th>
            <th>库存</th>
        </tr>
        {% for product in products %}
        <tr>
            <td>{{ product.id }}</td>
            <td>{{ product.name }}</td>
            <td>{{ product.category }}</td>
            <td>{{ product.price }}</td>
            <td>{{ product.stock }}</td>
        </tr>
        {% endfor %}
    </table>
</body>
</html>
    '''
    
    # 写入模板文件
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    with open('templates/login.html', 'w', encoding='utf-8') as f:
        f.write(login_html)
    with open('templates/admin.html', 'w', encoding='utf-8') as f:
        f.write(admin_html)

# 初始化模板
create_templates()

# 首页路由
@app.route('/')
def index():
    categories = list(set([p['category'] for p in products]))
    return render_template('index.html', products=products, categories=categories)

# 管理员登录
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PWD:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
    return render_template('login.html')

# 管理员后台
@app.route('/admin')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    return render_template('admin.html', products=products)

# 启动应用
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
