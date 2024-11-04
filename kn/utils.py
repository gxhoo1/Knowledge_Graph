from logger import logger

def process_results(results):
    nodes = []
    edges = []
    nodes_set = set()
    node_relationship_counts = {}
    for record in results:
        start_node = record['n']
        process_node(start_node, nodes_set, nodes, node_relationship_counts)
        end_node = record['m']
        process_node(end_node, nodes_set, nodes, node_relationship_counts)
        relationship = record['r']
        edge_data = {
            'from': str(start_node.identity),
            'to': str(end_node.identity),
            'label': type(relationship).__name__,
            'title': type(relationship).__name__,
            'properties': dict(relationship)
        }
        edges.append(edge_data)
        node_relationship_counts[start_node.identity] += 1
        node_relationship_counts[end_node.identity] += 1
    for node in nodes:
        node['size'] = (node_relationship_counts[int(node['id'])] or 1) * 10
    return nodes, edges, nodes_set, node_relationship_counts


def process_node(node, nodes_set, nodes, node_relationship_counts):
    """处理节点数据"""
    if node.identity not in nodes_set:
        properties = dict(node)
        labels = list(node.labels)
        label_name = labels[0] if labels else "Unknown"
        node_data = {
            'id': str(node.identity),
            'label': properties.get('name', '未命名'),
            'title': properties.get('name', '未命名'),
            'group': label_name,
            'properties': properties
        }
        nodes.append(node_data)
        nodes_set.add(node.identity)
        node_relationship_counts[node.identity] = 0
        

# 移除 determine_node_type 函数