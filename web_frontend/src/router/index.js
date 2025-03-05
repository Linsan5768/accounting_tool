import { createRouter, createWebHistory } from 'vue-router'
import Home from '../components/Home.vue' // 或你自定义的主页组件
import AddRecord from '../components/AddRecord.vue'
import RecordList from '../components/RecordList.vue'
import Statistics from '../components/Statistics.vue'

const routes = [
  { path: '/', name: 'HomePage', component: Home },
  { path: '/add', name: 'AddRecord', component: AddRecord },
  { path: '/records', name: 'RecordList', component: RecordList },
  { path: '/statistics', name: 'StatisticsPage', component: Statistics },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router