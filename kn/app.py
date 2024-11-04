from flask import Flask
from graph_routes import graph_bp
from logger import logger

app = Flask(__name__)
app.register_blueprint(graph_bp)

if __name__ == '__main__':
    logger.info("应用启动")
    app.run(debug=True, host='0.0.0.0', port=5010)