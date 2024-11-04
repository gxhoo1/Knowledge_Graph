import { networkOptions } from './config.js';
import { getNodeColor } from './utils.js';

export class NetworkManager {
    constructor(container) {
        this.container = container;
        this.network = null;
        this.nodesDataset = null;
        this.edgesDataset = null;
        this.allNodes = [];
    }

    initialize(data) {
        this.processData(data);
        this.createNetwork();
        this.setupEvents();
    } catch (error) {
        console.error('初始化网络时出错:', error);
    }

    processData(data) {
        
        const nodeSizes = this.calculateNodeSizes(data.edges);
        this.nodesDataset = new vis.DataSet(this.processNodes(data.nodes, nodeSizes));
        this.edgesDataset = new vis.DataSet(data.edges);
        this.allNodes = data.nodes;
    }
    
//节点大小计算
    calculateNodeSizes(edges) {
        const sizes = {};
        edges.forEach(edge => {
            sizes[edge.from] = (sizes[edge.from] || 0) + 1;
            sizes[edge.to] = (sizes[edge.to] || 0) + 1;
        });
        return sizes;
    }

    processNodes(nodes, nodeSizes) {
        return nodes.map(node => {
            const size = Math.min((nodeSizes[node.id] || 10) * 25 + 200, 700);
            const fontSize = Math.min(size / 2, 150) ;
            const nodeLabel = node.group || 'default';
            const nodeColor = getNodeColor(nodeLabel);
            const radius = size * 1.25 + 50;
            
            return {
                ...node,
                tag: node.tag || '无标签信息',
                fullLabel: node.label,
                label: node.label.length > 5 ? node.label.substring(0, 5) + '..' : node.label,
                size: radius,
                color: {
                    background: nodeColor,
                    border: nodeColor,
                    highlight: {
                        background: nodeColor,
                        border: nodeColor
                    },
                    hover: {
                        background: nodeColor,
                        border: '#8dda8d' // 设置悬停时的边框颜色为红色
                    }
                },

                font: {
                    size: fontSize,
                    color: 'rgba(0,0,0,1)',
                    face: 'Arial Bold',
                    weight: 'bold',      
                    vadjust: -1.3 * radius,            // 垂直位置调整
                    strokeWidth: 2,                
                    strokeColor: 'rgba(0,0,0,0.5)',
                 
                            


                }
            };
        });
    }

    createNetwork() {
        this.network = new vis.Network(this.container, {
            nodes: this.nodesDataset,
            edges: this.edgesDataset
        }, networkOptions);
    }

   


    setupEvents() {
        this.network.on('stabilizationIterationsDone', () => {
            this.network.fit({
                animation: {
                    duration: 1000,
                    easingFunction: 'easeInOutQuad'
                }
            });
        });
    }

    focusNode(nodeId) {
        this.network.focus(nodeId, {
            scale: 0.2,    //缩放比例
            animation: {
                duration: 1000,
                easingFunction: 'easeInOutQuad'
            }
        });
        this.network.selectNodes([nodeId]);
    }

    
}