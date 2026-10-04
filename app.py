# app.py
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calculator.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)  # 允许网页跨域访问后端

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
    expr = expr.replace('×', '*').replace('÷', '/')
    # 只允许 数字、空格、+ - * / ( ) .
    if not re.match(r'^[\d\s+\-*/().]+$', expr):
        raise ValueError("表达式含非法字符")
    if not expr.strip():
        raise ValueError("表达式为空")
    try:
        # 限制 eval 的可用名字空间，防止代码注入
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