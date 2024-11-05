from flask import Flask, render_template, request, jsonify
from neo4j import GraphDatabase
import openai
import re
import json
from datetime import datetime

app = Flask(__name__)

# OpenAI配置
openai.api_key = 'sk-proj'

# Neo4j配置

#NEO4J_URI = "neo4j://38.60.163.201:7687"
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "123"
NEO4J_PASSWORD = "123"

HISTORY_FILE = 'history.json'

def convert_to_triples(text):
    response = openai.ChatCompletion.create(
        model='gpt-4o',
        messages=[
            {"role": "system", "content": "将以下内容转换为 节点1（节点1的标签）-关系-节点（节点2的标签） 格式"},
            {"role": "user", "content": f"内容: {text}\n结果为三元组，格式为: 节点1（节点1的标签）-关系-节点（节点2的标签），节点的名称和标签使用科学术语，严格按照格式输出，不要加其他任何文字，注意节点的名称不要重复，将相同名称但不同标签的节点合并，并选择最合适的标签，节点的标签不要过于具体，不要出现太多不同的标签"}
        ]
    )
    return response.choices[0].message['content'].strip()

def import_to_neo4j(triples):
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    with driver.session() as session:
        for triple in triples.split('\n'):
            if triple.strip():
                # 解析三元组
                source, relation, target = triple.strip().split('-')
                # 提取源节点名称和标签
                source_name, source_label = source.strip().split('（')
                source_label = source_label.rstrip('）')
                # 提取目标节点名称和标签
                target_name, target_label = target.strip().split('（')
                target_label = target_label.rstrip('）')
                # 保留中文字符的正则表达式
                relation = re.sub(r'[^\w\u4e00-\u9fa5]', '_', relation.strip())
                # 创建节点和关系，使用反引号包裹关系类型
                cypher_query = f"""
                    MERGE (s:{source_label} {{name: $source_name}})
                    MERGE (t:{target_label} {{name: $target_name}})
                    CREATE (s)-[:`{relation}`]->(t)
                """
                session.run(cypher_query, source_name=source_name, target_name=target_name)

    driver.close()

def save_history(input_text, result):
    try:
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            history_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history_data = []

    history_data.append({
        'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'input_text': input_text,
        'result': result
    })

    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history_data, f, ensure_ascii=False, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    input_text = request.json['text']
    try:
        result = convert_to_triples(input_text)
        save_history(input_text, result)
        return jsonify({'success': True, 'result': result})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/import-neo4j', methods=['POST'])
def import_to_graph():
    triples = request.json['triples']
    try:
        import_to_neo4j(triples)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
