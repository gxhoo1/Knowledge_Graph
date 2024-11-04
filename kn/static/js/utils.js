const colorArray = [
    'rgb(214,94,121)',    // 颜色1
    'rgb(190,195,200)',    // 颜色2
    'rgb(68,205,205)',    // 颜色3
    'rgb(161,132,216)',   // 颜色4
    'rgb(69,186,69)',     // 颜色5
    'rgb(223,131,81)',    // 颜色6
    'rgb(71,149,198)',    // 颜色7
    'rgb(205,182,108)',   // 颜色8
    'rgb(57,168,168)',    // 颜色9
    'rgb(213,204,177)',   // 颜色10
    'rgb(228,96,121)',    // 颜色11
    'rgb(53,143,200)',    // 颜色12
    'rgb(250,199,75)',    // 颜色13
    'rgb(176,159,213)',   // 颜色14
    'rgb(227,139,53)',    // 颜色15
    'rgb(218,100,100)',   // 颜色16
    'rgb(104,119,223)',    // 颜色17
    'rgb(172,84,172)',   // 颜色18
    'rgb(82,195,112)',   // 颜色19
    'rgb(243,150,128)',     // 颜色20
  
];

const labelColorMap = {};

export function getNodeColor(label) {
    if (labelColorMap[label]) {
        // 如果标签已存在映射，直接返回对应的颜色
        return labelColorMap[label];
    } else {
        // 从颜色数组中随机选取一个颜色
        const randomIndex = Math.floor(Math.random() * colorArray.length);
        const color = colorArray[randomIndex];
        // 将标签和颜色存入映射
        labelColorMap[label] = color;
        return color;
    }
}

// 根据标签生成颜色的函数
function generateColorFromLabel(label) {
    // 简单的哈希函数，将标签转换为颜色
    let hash = 0;
    for (let i = 0; i < label.length; i++) {
        hash = label.charCodeAt(i) + ((hash << 5) - hash);
    }
    const hue = hash % 360;
    return `hsl(${hue}, 70%, 50%)`;
}

