import {defineStore} from 'pinia';

export const useRecipeStore = defineStore('recipe', {
    state: () => ({
        recipeList:[
        {
            name: '番茄炒蛋',
            ingredients: ['番茄', '鸡蛋', '盐', '油'],
            steps: [
                '将番茄切块，鸡蛋打散',
                '热锅凉油，放入番茄炒软',
                '倒入鸡蛋液，快速翻炒',
                '加盐调味，出锅装盘'
            ],
            img: 'https://tse3-mm.cn.bing.net/th/id/OIP-C.Zk-wRUPHXqqJfbrY7nFvNwHaE7?w=244&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
        },
        {
            name: '宫保鸡丁',
            ingredients: ['鸡丁', '花生', '青椒', '干辣椒', '盐', '油'],
            steps: [
                '将鸡丁用盐和油腌制15分钟',
                '热锅凉油，放入花生炒香',
                '加入鸡丁翻炒至变色',
                '放入青椒和干辣椒炒匀',
                '加盐调味，出锅装盘'
            ],
            img: 'https://tse1-mm.cn.bing.net/th/id/OIP-C.MU-wgg1cm6NeYV9pTDXQDAHaEJ?w=284&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
        },
        {
            name: '红烧肉',
            ingredients: ['五花肉', '生抽', '老抽', '糖', '葱', '姜'],
            steps: [
                '五花肉切块，焯水去腥',
                '热锅凉油，放入糖炒至糖色',
                '加入五花肉翻炒上色',
                '加入生抽、老抽、葱姜炒匀',
                '加水没过肉，炖煮1小时',
                '收汁后出锅装盘'
            ],
            img: 'https://tse4-mm.cn.bing.net/th/id/OIP-C.uO4BQ9ntoqmPYbtJe8WCXAHaE7?w=272&h=181&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
        },
        {
            name: '清炒时蔬',
            ingredients: ['青菜', '蒜', '盐', '油'],
            steps: [
                '青菜洗净切段，蒜切片',
                '热锅凉油，放入蒜片炒香',
                '加入青菜翻炒至断生',
                '加盐调味，出锅装盘'
            ],
            img: 'https://tse2-mm.cn.bing.net/th/id/OIP-C.saSlf9lPtaO6REikBCFssQHaE8?w=291&h=194&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
        },
        {
            name: '蒸鱼',
            ingredients: ['鱼', '姜', '葱', '盐', '料酒'],
            steps: [
                '鱼清理干净，放姜葱盐料酒腌制30分钟',
                '蒸锅加水，放入鱼蒸10分钟',
                '出锅后撒上葱花，淋上热油'
            ],
            img: "https://tse2-mm.cn.bing.net/th/id/OIP-C.x5hMn0tZRn9B06iRhfr2pgHaEJ?w=331&h=186&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3"
        },
        {
            name: '炒饭',
            ingredients: ['米饭', '鸡蛋', '胡萝卜', '青豆', '盐', '油'],
            steps: [
                '热锅凉油，放入鸡蛋炒散',
                '加入米饭翻炒均匀',
                '放入胡萝卜丁和青豆炒匀',
                '加盐调味，出锅装盘'
            ],
            img: 'https://tse2-mm.cn.bing.net/th/id/OIP-C.xddN2uqYmIyXpjEgsHzJYQHaEJ?w=287&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
        },
        {
            name: '牛肉面',
            ingredients: ['牛肉', '面条', '青菜', '姜', '葱', '盐', '油'],
            steps: [
                '牛肉切片，用盐和油腌制15分钟',
                '热锅凉油，放入牛肉翻炒至变色',
                '加入姜葱炒香',
                '倒入面条和青菜翻炒均匀',
                '加盐调味，出锅装盘'
            ],
            img: 'https://tse1-mm.cn.bing.net/th/id/OIP-C.KK5q5GsCDwKMnkxX3TOmpAHaHa?w=174&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
        },
        {
            name: '麻辣香锅',
            ingredients: ['各种蔬菜', '豆腐', '香肠', '辣椒', '花椒', '盐', '油'],
            steps: [
                '热锅凉油，放入花椒炒香',
                '加入豆腐和香肠翻炒',
                '放入各种蔬菜和辣椒炒匀',
                '加盐调味，出锅装盘'
            ],
            img: 'https://tse2-mm.cn.bing.net/th/id/OIP-C.lQ_SAA1XgEZFZyB92TeCvwHaE8?w=239&h=180&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
        },
        {
            name: '糖醋排骨',
            ingredients: ['排骨', '糖', '醋', '生抽', '姜', '葱'],
            steps: [
                '排骨焯水去腥，捞出沥干',
                '热锅凉油，放入糖炒至糖色',
                '加入排骨翻炒上色',
                '加入醋、生抽、姜葱炒匀',
                '加水没过肉，炖煮1小时',
                '收汁后出锅装盘'
            ],
            img: 'https://tse3-mm.cn.bing.net/th/id/OIP-C.yrEBRN0yXpfmpj37knGqJQHaFC?w=275&h=187&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
        },
        {
            name: '蒜蓉西兰花',
            ingredients: ['西兰花', '蒜', '盐', '油'],
            steps: [
                '西兰花切小朵，蒜切末',
                '热锅凉油，放入蒜末炒香',
                '加入西兰花翻炒至断生',
                '加盐调味，出锅装盘'
            ],
            img: 'https://tse2-mm.cn.bing.net/th/id/OIP-C.GrcRr5T8L8BN7_6DxfZs-QHaFj?w=265&h=199&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3'
        }
    ]}),
    getters: {
        getRecipes: (state) => state.recipeList,
    },
    actions: {}
})