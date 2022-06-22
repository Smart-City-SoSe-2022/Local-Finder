<template>
<div>
    <MakeReservation/>
    <img class="star" v-show="isFav"
        alt="Favorisieren" src="../assets/star.png" 
        width="50" height="50"
        @click="toggleFav"
    >
    <img class="star" v-show="!isFav"
        alt="Favorisieren" src="../assets/star_grey.png" 
        width="50" height="50"
         @click="toggleFav"
    >
    <h1> {{this.location.name}}</h1>
    <p>{{this.location.address}}, {{this.location.plz}} {{this.location.city}}</p>
    <p>{{this.location.open}}</p>
</div>
</template>

<script>
import MakeReservation from '@/components/reservations/MakeReservation.vue'

export default {
    name: 'LocalPage',
    components: {
        MakeReservation
    },
    data() {
        return {
            location:
                {
                    "id": 1,
                    "name": "Loc1",
                    "address": "Straße Da 1",
                    "open": "17 Uhr"
                },
            isFav: Boolean,
        }
    },
    watch: {
            '$route.path': async function() {
                this.location = await this.fetchLokal()
            }
        },
    methods: {
        async fetchLokal() {
            const response = await fetch('/api/getLokal?id='+this.$route.params.id)
            const data = await response.json()
            return data
        },
        async isFaved() {
            const response = await fetch('/api/isFavorite', {
                method: 'POST',
				headers: {
					'Content-type': 'application/json',
				},
				body: JSON.stringify({
                    "accId": 1,
                    "lokId": this.$route.params.id
                })
            })
            const data = await response.text()
            if(data == "True") return true
            return false
        },
        async toggleFav() {
            const response = await fetch('/api/toggleFavorite', {
                method: 'POST',
				headers: {
					'Content-type': 'application/json',
				},
				body: JSON.stringify({
                    "AccountId": 1,
                    "lokalId": this.$route.params.id
                })
            })
            const data = await response
            this.isFav = !this.isFav
            console.log(data)
        },
    },
    async created() {
        this.location = await this.fetchLokal()
        this.isFav = await this.isFaved()
    }
}
</script>

<style scoped>
.star {
    float: left;
    margin-top: 0 auto;
}
</style>
