export class SearchManager {
    constructor(networkManager, nodeInfoManager) {
        this.networkManager = networkManager;
        this.searchInput = document.getElementById('searchInput');
        this.searchResults = document.getElementById('searchResults');
        this.searchStats = document.getElementById('searchStats');
        this.setupSearch();
    }

    setupSearch() {
        this.searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase().trim();

            if (searchTerm.length < 1) {
                this.hideResults();
                return;
            }

            const results = this.networkManager.allNodes.filter(node => {
                const nodeLabel = (node.label || '').toLowerCase();
                const nodeGroup = (node.group || '').toLowerCase();
                return nodeLabel.includes(searchTerm) || nodeGroup.includes(searchTerm);
            }).slice(0, 10);
            this.displayResults(results);
        });
    
        this.searchResults.addEventListener('click', (e) => {
            const resultItem = e.target.closest('.search-result-item');
            if (resultItem) {
                const nodeId = resultItem.dataset.nodeId;
                this.networkManager.focusNode(nodeId);
                this.hideResults();
                this.searchInput.value = resultItem.textContent;
            }
        });
    }

    displayResults(results) {
        this.searchResults.innerHTML = '';
        if (results.length > 0) {
            results.forEach(node => {
                const div = document.createElement('div');
                div.className = 'search-result-item';
                div.textContent = `${node.label} (${node.group})`;
                div.dataset.nodeId = node.id;
                this.searchResults.appendChild(div);
            });
            this.showResults();
        } else {
            this.hideResults();
        }
    }

    showResults() {
        this.searchResults.style.display = 'block';
    }

    hideResults() {
        this.searchResults.style.display = 'none';
        this.searchStats.textContent = '';
    }

    setupSearch() {
        this.searchInput.addEventListener('input', (e) => {
            const searchTerm = e.target.value.toLowerCase().trim();
            if (searchTerm.length < 1) {
                this.hideResults();
                return;
            }
            this.performSearch(searchTerm);
        });
    
        this.searchInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                const searchTerm = this.searchInput.value.toLowerCase().trim();
                if (searchTerm.length > 0) {
                    const results = this.performSearch(searchTerm);
                    if (results && results.length > 0) {
                        const firstNode = results[0];
                        this.networkManager.focusNode(firstNode.id);
                        this.hideResults();
                    }
                }
            }
        });
    
        this.searchResults.addEventListener('click', (e) => {
            const resultItem = e.target.closest('.search-result-item');
            if (resultItem) {
                const nodeId = resultItem.dataset.nodeId;
                this.networkManager.focusNode(nodeId);
                this.hideResults();
                this.searchInput.value = resultItem.textContent;
            }
        });
    }
    
    performSearch(searchTerm) {
        const results = this.networkManager.allNodes.filter(node => {
            const nodeLabel = (node.label || '').toLowerCase();
            const nodeGroup = (node.group || '').toLowerCase();
            return nodeLabel.includes(searchTerm) || nodeGroup.includes(searchTerm);
        }).slice(0, 10);
    
        this.displayResults(results);
        return results;
    }
}