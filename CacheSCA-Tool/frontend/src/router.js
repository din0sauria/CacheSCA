import { createRouter, createWebHistory } from 'vue-router'
import Home from '@/views/Home.vue'
import Performance from '@/views/Performance.vue'
import Evaluation from '@/views/Evaluation.vue'

const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/performance',
    name: 'Performance',
    component: Performance
  },
  {
    path: '/evaluation',
    name: 'Evaluation',
    component: Evaluation
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
