# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calculator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)  # 允许前端跨域访问

db = SQLAlchemy(app)


# 数据库表：一条历史记录
class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    expression = db.Column(db.String(200), nullable=False)
    result = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)


with app.app_context():
    db.create_all()  # 自动建表


# 安全计算函数
def safe_calc(expr):
    # 1) 把 × ÷ 换成 * /
    expr = expr.replace('×', '*').replace('÷', '/')

    # 2) 字符白名单校验：只允许数字、空格、+ - * / ( ) .
    if not re.match(r'^[\d\s+\-*/().]+$', expr):
        raise ValueError("表达式含非法字符")
    if not expr.strip():
        raise ValueError("表达式为空")

    # 去掉空格，方便检查语法
    s = expr.replace(' ', '')

    # 3) 禁止连续两个运算符，除非第二个是紧跟 ( * / + - 之后的一元正负号
    #    例如：3*-2 可以，1++2 不行
    for i in range(1, len(s)):
        a, b = s[i - 1], s[i]
        if a in '+-*/' and b in '+-*/':
            if b in '+-' and a in '(*/+-':
                continue  # b 是一元正负号，合法
            raise ValueError("无效表达式")

    # 4) 括号必须配对
    depth = 0
    for ch in s:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            if depth < 0:
                raise ValueError("无效表达式")
    if depth != 0:
        raise ValueError("无效表达式")

    # 5) 不允许空括号
    if '()' in s:
        raise ValueError("无效表达式")

    # 6) 左括号后不能直接是 * 或 /；运算符后不能直接接 )
    if re.search(r'[(][*/]', s) or re.search(r'[+\-*/][)]', s):
        raise ValueError("无效表达式")

    # 7) 表达式不能以运算符结尾
    if s and s[-1] in '+-*/':
        raise ValueError("无效表达式")

    # 8) 计算
    try:
        result = eval(expr, {"__builtins__": None}, {})
        return result
    except ZeroDivisionError:
        raise ZeroDivisionError("除数不能为0")
    except Exception:
        raise ValueError("无效表达式")


# 接口1：计算
@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    expr = data.get('expression', '').strip()
    if not expr:
        return jsonify({"success": False, "message": "表达式为空"}), 400
    try:
        result = safe_calc(expr)
        rec = History(expression=expr, result=str(result))
        db.session.add(rec)
        db.session.commit()
        return jsonify({"success": True, "expression": expr, "result": result}), 200
    except ZeroDivisionError as e:
        return jsonify({"success": False, "message": str(e)}), 400
    except ValueError as e:
        return jsonify({"success": False, "message": str(e)}), 400


# 接口2：获取历史
@app.route('/api/history', methods=['GET'])
def get_history():
    records = History.query.order_by(History.created_at.desc()).all()
    return jsonify({
        "success": True,
        "history": [{
            "id": r.id,
            "expression": r.expression,
            "result": r.result,
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for r in records]
    }), 200


# 接口3：删除一条历史
@app.route('/api/history/<int:rid>', methods=['DELETE'])
def delete_history(rid):
    rec = History.query.get(rid)
    if not rec:
        return jsonify({"success": False, "message": "记录不存在"}), 404
    db.session.delete(rec)
    db.session.commit()
    return jsonify({"success": True}), 200


# 接口4：清空全部历史
@app.route('/api/history', methods=['DELETE'])
def clear_history():
    History.query.delete()
    db.session.commit()
    return jsonify({"success": True, "message": "已清空全部历史"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)