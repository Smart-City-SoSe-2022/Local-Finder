import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Results from '../views/Results.vue'
import About from '../views/About.vue'
import LocalPage from '../views/LocalPage.vue'

const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
    },
    {
        path: '/about',
        name: 'About',
        component: About
    },
    {
        path: '/results',
        name: 'Results',
        component: Results
    },
    {
        path: '/local/:id',
        name: 'LocalPage',
        component: LocalPage,
        params: true
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
