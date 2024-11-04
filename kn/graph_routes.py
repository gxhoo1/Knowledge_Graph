
from flask import Blueprint, render_template, jsonify
from db import get_db
from utils import process_results
from datetime import datetime
from logger import logger

graph_bp = Blueprint('graph_bp', __name__)

@graph_bp.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"渲染主页失败: {str(e)}")
        return "服务器错误", 500


@graph_bp.route('/get_graph_data')
def get_graph_data():
    try:
        graph = get_db()
        if not graph:
            logger.error("数据库连接失败")
            return jsonify({"error": "数据库连接失败"}), 500
            
        # 修改查询以获取更多有用的属性
        query = """
        MATCH (n)-[r]->(m)
        RETURN DISTINCT n, r, m
        """
        
        results = graph.run(query)
        nodes, edges, nodes_set, node_relationship_counts = process_results(results)
        logger.info(f"获取图谱数据成功 - 节点数: {len(nodes)}, 关系数: {len(edges)}")
        return jsonify({
            'nodes': nodes,
            'edges': edges,
            'stats': {
                'nodeCount': len(nodes),
                'edgeCount': len(edges),
                'timestamp': datetime.now().isoformat()
            }
        })
    except Exception as e:
        logger.error(f"获取图谱数据失败: {str(e)}")
        return jsonify({"error": str(e)}), 500     

@graph_bp.route('/search_nodes/<query>')
def search_nodes(query):
    """搜索节点"""
    try:
        graph = get_db()
        if not graph:
            return jsonify({"error": "数据库连接失败"}), 500
        cypher_query = """
        MATCH (n)
        WHERE n.name =~ $name
        RETURN n
        LIMIT 10
        """
        results = graph.run(cypher_query, name=f"(?i).*{query}.*")
        nodes = []
        for record in results:
            node = record['n']
            properties = dict(node)
            labels = list(node.labels)
            nodes.append({
                'id': str(node.identity),
                'label': properties.get('name', '未命名'),
                'fullLabel': properties.get('name', '未命名'),  
                'properties': properties
            })
        logger.info(f"搜索节点成功 - 关键词: {query}, 结果数: {len(nodes)}")
        return jsonify(nodes)
    except Exception as e:
        logger.error(f"搜索节点失败 - 关键词: {query}, 错误: {str(e)}")
        return jsonify({"error": str(e)}), 500

