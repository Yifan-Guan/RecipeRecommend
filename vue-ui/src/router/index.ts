import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/pages/Home.vue'
import Chat from '@/pages/Chat.vue'
import Recipe from '@/pages/Recipe.vue'
import Recommend from '@/pages/Recommend.vue'
import Tool from '@/pages/Tool.vue'
import About from '@/pages/About.vue'

const routes = [
  {
    path: '/home',
    name: 'home',
    component: Home
  },
  {
    path: '/chat',
    name: 'chat',
    component: Chat
  },
  {
    path: '/recipe',
    name: 'recipe',
    component: Recipe 
  },
  {
    path: '/recommend',
    name: 'recommend',
    component: Recommend 
  },
  {
    path: '/tool',
    name: 'tool',
    component: Tool 
  },
  {
    path: '/about',
    name: 'about',
    component: About 
  },
  {
    path: '/',
    redirect: '/home'
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;