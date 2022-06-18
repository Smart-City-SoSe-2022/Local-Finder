<template>
<div>
    <img class="star" 
        alt="Favorisieren" src="../assets/star.png" 
        width="50" height="50"
    >
    <h1> {{this.location.name}}</h1>
    <p>{{this.location.address}}</p>
    <p>{{this.location.open}}</p>
</div>
</template>

<script>
export default {
    name: 'LocalPage',
    data() {
        return {
            location:
                {
                    "id": 1,
                    "name": "Loc1",
                    "address": "Straße Da 1",
                    "open": "17 Uhr"
                }
        }
    },
    methods: {
        async fetchLokal() {
            const response = await fetch('/api/getLokal?id='+this.$route.params.id)
            const data = await response.json()
            return data
        }
    },
    async created() {
        this.location = await this.fetchLokal()
    }
}
</script>

<style scoped>
.star {
    float: left;
    margin-top: 0 auto;
}
</style>
