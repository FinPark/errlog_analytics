import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/pages/HomePage.vue'
import UploadPage from '@/pages/UploadPage.vue'
import DashboardPage from '@/pages/DashboardPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomePage
    },
    {
      path: '/upload',
      name: 'upload',
      component: UploadPage
    },
    {
      path: '/dashboard',
      name: 'dashboard',
      component: DashboardPage
    }
  ]
})

export default router