import { NetworkManager } from './networkManager.js';
import { SearchManager } from './searchManager.js';
import { NodeInfoManager } from './nodeInfoManager.js';
import { EventManager } from './eventManager.js';

document.addEventListener('DOMContentLoaded', function() {
    // 初始化图谱容器
    const container = document.getElementById('graph');
    const networkManager = new NetworkManager(container);
    const nodeInfoManager = new NodeInfoManager();
    
    // 获取图谱数据
    fetch('/get_graph_data')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error('Error loading graph data:', data.error);
                return;
            }
            
            // 初始化网络图
            networkManager.initialize(data);
            
            // 初始化搜索管理器
            const searchManager = new SearchManager(networkManager, nodeInfoManager);
            
            // 初始化事件管理器
            const eventManager = new EventManager(networkManager, searchManager, nodeInfoManager);

            // 设置网络事件监听

            console.log('Graph initialized successfully');
        })
        .catch(error => {
            console.error('Error loading graph data:', error);
        });
});
