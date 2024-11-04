from flask import Flask, render_template, request, redirect, url_for
from neo4j import GraphDatabase

app = Flask(__name__)

# 配置Neo4j数据库连接
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("123", "123"))  # 请修改为你的Neo4j用户名和密码

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        search_term = request.form.get('search_term', '')
    else:
        search_term = request.args.get('search_term', '')

    with driver.session() as session:
        # 搜索节点
        nodes = session.run("""
            MATCH (n)
            WHERE n.name CONTAINS $search_term OR ANY(label IN labels(n) WHERE label CONTAINS $search_term)
            RETURN properties(n) as props, id(n) as id, labels(n) as labels
        """, search_term=search_term).data()
        
        # 搜索相关的所有关系
        relationships = session.run("""
            MATCH (a)-[r]->(b)
            WHERE a.name CONTAINS $search_term OR b.name CONTAINS $search_term
            RETURN type(r) as type, id(r) as id, properties(r) as props,
                   properties(a) as source_props, properties(b) as target_props,
                   labels(a) as source_label, labels(b) as target_label
        """, search_term=search_term).data()
        
    return render_template('search_results.html', 
                           nodes=nodes, 
                           relationships=relationships,
                           search_term=search_term)


# 修改节点
@app.route('/edit_node', methods=['POST'])
def edit_node():
    node_id = request.form['node_id']
    new_name = request.form['new_name']
    new_definition = request.form['new_definition']
    search_term = request.form.get('search_term', '')
    
    with driver.session() as session:
        # 先执行节点更新
        session.run("""
            MATCH (n) WHERE id(n) = $id 
            SET n.name = $new_name, n.definition = $new_definition
        """, id=int(node_id), new_name=new_name, new_definition=new_definition)
        
        # 在同一会话中执行搜索查询
        nodes = session.run("""
            MATCH (n)
            WHERE n.name CONTAINS $search_term 
            RETURN properties(n) as props, id(n) as id, labels(n) as labels
        """, search_term=search_term).data()
        
        relationships = session.run("""
            MATCH (a)-[r]->(b)
            WHERE a.name CONTAINS $search_term OR b.name CONTAINS $search_term
            RETURN type(r) as type, id(r) as id, properties(r) as props,
                   properties(a) as source_props, properties(b) as target_props,
                   labels(a) as source_label, labels(b) as target_label
        """, search_term=search_term).data()
        
    # 在会话关闭后渲染模板
    return render_template('search_results.html',
                         nodes=nodes,
                         relationships=relationships,
                         search_term=search_term)
    
# 添加节点和关系
@app.route('/add_nodes_relationship', methods=['POST'])
def add_nodes_relationship():
    node1_name = request.form['node1_name']
    node1_label = request.form['node1_label']
    relationship = request.form['relationship']
    node2_name = request.form['node2_name']
    node2_label = request.form['node2_label']
    
    with driver.session() as session:
        # 使用MERGE语句，如果节点存在则匹配，不存在则创建
        session.run("""
            MERGE (a:%s {name: $node1_name})
            MERGE (b:%s {name: $node2_name})
            CREATE (a)-[r:%s]->(b)
        """ % (node1_label, node2_label, relationship), 
        node1_name=node1_name, node2_name=node2_name)
    return redirect(url_for('index'))

# 添加/修改节点属性
@app.route('/add_node_property', methods=['POST'])
def add_node_property():
    node_name = request.form['node_name']
    node_label = request.form['node_label']
    definition = request.form['definition']
    
    with driver.session() as session:
        # 使用MERGE语句：如果节点存在则匹配并更新定义，如果不存在则创建新节点
        session.run("""
            MERGE (n:%s {name: $node_name})
            SET n.definition = $definition
        """ % node_label, node_name=node_name, definition=definition)
    return redirect(url_for('index'))

# 删除节点
@app.route('/delete_node', methods=['POST'])  # 确保指定 POST 方法
def delete_node():
    node_id = request.form['node_id']
    search_term = request.form.get('search_term', '')  # 获取搜索词
    
    with driver.session() as session:
        # 删除节点
        session.run("MATCH (n) WHERE id(n) = $id DETACH DELETE n", id=int(node_id))
        
        # 重新执行搜索
        nodes = session.run("""
            MATCH (n)
            WHERE n.name CONTAINS $search_term 
            RETURN properties(n) as props, id(n) as id, labels(n) as labels
        """, search_term=search_term).data()
        
        relationships = session.run("""
            MATCH (a)-[r]->(b)
            WHERE a.name CONTAINS $search_term OR b.name CONTAINS $search_term
            RETURN type(r) as type, id(r) as id, properties(r) as props,
                   properties(a) as source_props, properties(b) as target_props,
                   labels(a) as source_label, labels(b) as target_label
        """, search_term=search_term).data()
    
    # 返回搜索结果页面
    return render_template('search_results.html',
                         nodes=nodes,
                         relationships=relationships,
                         search_term=search_term)

# 添加关系（保留原有功能可选）
@app.route('/add_relationship', methods=['POST'])
def add_relationship():
    start_id = request.form['start_id']
    end_id = request.form['end_id']
    rel_type = request.form['rel_type']
    with driver.session() as session:
        session.run("""
            MATCH (a), (b)
            WHERE id(a) = $start_id AND id(b) = $end_id
            CREATE (a)-[r:%s]->(b)
        """ % rel_type, start_id=int(start_id), end_id=int(end_id))
    return redirect(url_for('index'))

# 保留删除关系的路由
@app.route('/delete_relationship', methods=['POST'])
def delete_relationship():
    rel_id = request.form['rel_id']
    search_term = request.form.get('search_term', '')  # 获取搜索词
    
    with driver.session() as session:
        # 删除关系
        session.run("MATCH ()-[r]->() WHERE id(r) = $id DELETE r", id=int(rel_id))
        
        # 重新执行搜索
        nodes = session.run("""
            MATCH (n)
            WHERE n.name CONTAINS $search_term 
            RETURN properties(n) as props, id(n) as id, labels(n) as labels
        """, search_term=search_term).data()
        
        relationships = session.run("""
            MATCH (a)-[r]->(b)
            WHERE a.name CONTAINS $search_term OR b.name CONTAINS $search_term
            RETURN type(r) as type, id(r) as id, properties(r) as props,
                   properties(a) as source_props, properties(b) as target_props,
                   labels(a) as source_label, labels(b) as target_label
        """, search_term=search_term).data()
    
    # 返回搜索结果页面
    return render_template('search_results.html',
                         nodes=nodes,
                         relationships=relationships,
                         search_term=search_term)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)  # 允许外部访问