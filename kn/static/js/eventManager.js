export class EventManager {
    constructor(networkManager, searchManager, nodeInfoManager) {
        this.networkManager = networkManager;
        this.searchManager = searchManager;
        this.nodeInfoManager = nodeInfoManager;
        this.setupEvents();
    }

    setupEvents() {
        // 网络的单击事件
        this.networkManager.network.on('click', (params) => {
            if (params.nodes.length > 0) {
                // 用户点击了节点，显示信息面板
                const nodeId = params.nodes[0];
                const node = this.networkManager.nodesDataset.get(nodeId);
                this.nodeInfoManager.show(node);
            } else {
                // 用户点击了网络的空白处，隐藏信息面板
                this.nodeInfoManager.hide();
            }
        });


        // 键盘事件
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.searchManager.hideResults();
                this.nodeInfoManager.hide();
            }
        });
    }
}