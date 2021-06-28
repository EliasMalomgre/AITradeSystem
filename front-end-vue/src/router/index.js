import Vue from 'vue'
import VueRouter from 'vue-router'
import ShareHistory from '../views/ShareHistory.vue'
import Positions from '../views/Positions.vue'


Vue.use(VueRouter)

const routes = [
  {
    path: '/home',
    name: 'ShareHistory',
    component: ShareHistory
  },
  {
    path: '/positions',
    name: 'Positions',
    component: Positions
  }
]

const router = new VueRouter({
  routes
})
router.replace({path:'/', redirect:'/home'})

export default router
