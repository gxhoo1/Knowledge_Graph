export class NodeInfoManager {
    constructor() {
        this.nodeInfo = document.getElementById('nodeInfo');
        if (!this.nodeInfo) {
            console.error('Node info element not found!');
        }
    }

    show(node) {
        if (!node || !this.nodeInfo) return;
    
        this.nodeInfo.innerHTML = `
            <h3>${node.fullLabel}</h3>
            <p>分组: ${node.group|| ' '}</p>
       
            <p>定义:</p>
            ${node.properties ? 
              `<div class="node-properties">${
                Object.entries(node.properties)
                  .filter(([key]) => key !== 'name')
                  .map(([key, value]) => `   ${value}`)
                  .join('<br>')
              }</div>` : 
              '<p>无定义信息</p>'
            }

        `;

        this.nodeInfo.style.display = 'block';
        this.nodeInfo.classList.add('visible');
        console.log('显示节点信息:', node);
    }

    hide() {
        if (this.nodeInfo) {
            this.nodeInfo.classList.remove('visible');
            this.nodeInfo.innerHTML = '';
            console.log('隐藏节点信息');
        }
    }
}