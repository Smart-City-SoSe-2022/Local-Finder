<template>
    <div>
        <h1> Favoriten </h1>
        <LocationList :list="locations" @delete="del" 
            @open-loc="openLocation"/>
    </div>
</template>

<script>
import LocationList from '@/components/results/LocationList.vue'

export default {
    name: 'Favoriten',
    components:  {
        LocationList,
    },
    data() {
        return {
            locations: []
        }
    },
    methods: {
        openLocation(id) {
            this.$router.push({ name: 'LocalPage', params: { id: id} })
        },
        async fetchResults() {
            const response = await fetch('http://server.it-humke.de:9004/api/getFavorites')
            if(response.ok){
                const data = await response.json()
                return data
            } else {
                console.log(await response.text())
                return {}
            }
        }
    },
    async created() {
        this.locations = await this.fetchResults()
    }
}
</script>

