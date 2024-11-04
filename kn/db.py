from py2neo import Graph
from logger import logger

# Neo4j数据库连接配置
NEO4J_HOST = 'bolt://localhost:7687'
NEO4J_AUTH = ('123', '123')

def get_db():
    """获取数据库连接"""
    try:
        return Graph(NEO4J_HOST, auth=NEO4J_AUTH)
    except Exception as e:
        logger.error(f"数据库连接失败: {str(e)}")
        return None