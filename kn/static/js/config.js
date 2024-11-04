export const networkOptions = {
    
    nodes: {
        shape: 'dot',
        borderWidth: 2,
        shadow: {
            enabled: true,
            color: 'rgba(0,0,0,0.2)',
            size: 2,
            x: 1,
            y: 1
        },


    },

    edges: {
        width: 50,
        color: {
            color: '#76b3f4',
            highlight: '#76b3f4',
            hover: '#76b3f4'
        },
        arrows: {
            to: {
                enabled: true,
                scaleFactor: 0.2
            }
        },
        smooth: {
            enabled: true,
            type: 'continuous',
            roundness: 0.15
        },
        font: {
            size: 80,
            align: 'middle',
            background: 'rgba(255, 255, 255, 0)'
        }
    },
    physics: {
        enabled: true,
        solver: 'forceAtlas2Based',
        forceAtlas2Based: {
            gravitationalConstant: -2500,
            centralGravity: 0.004,
            springLength: 1000,
            springConstant: 0.01,
            damping: 0.3,
            avoidOverlap: 1
        },
        stabilization: {
            enabled: true,
            iterations: 2000,
            updateInterval: 20
        },
        maxVelocity: 50,
        minVelocity: 0.1,
        timestep: 0.3
    },
    layout: {
        randomSeed: 42,
        improvedLayout: true
    },
    interaction: {
        selectable: true,       
        multiselect: false,         
        selectConnectedEdges: true, 
        hover: true,               
        tooltipDelay: 300,         
        zoomView: true,
        dragView: true,
        keyboard: true
    },

};