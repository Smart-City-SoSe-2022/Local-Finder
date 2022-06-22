import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Results from '../views/Results.vue'
import About from '../views/About.vue'
import LocalPage from '../views/LocalPage.vue'
import Favoriten from '../views/Favoriten.vue'
import Reservation from '../views/Reservation.vue'
import NewLocation from '../views/NewLocation.vue'

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
    },
    {
        path: '/favoriten',
        name : 'Favoriten',
        component: Favoriten
    },
    {
        path: '/reservierungen',
        name : 'Reservation',
        component: Reservation
    },
    {
        path: '/newLocation',
        name: 'NewLocation',
        component: NewLocation
    }
]

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes
})

export default router
