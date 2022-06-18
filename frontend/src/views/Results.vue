<template>
    <div>
        <h1> Ergebnisse </h1>
        <LocationList :list="locations" 
            @open-loc="openLocation"/>
    </div>
</template>

<script>
import LocationList from '@/components/results/LocationList.vue'

export default {
    name: 'Results',
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
            const response = await fetch('api/getLokals')
            const data = await response.json()
            if (response.status === 200) {
                return data
            }
            return {}
        }
    },
    async created() {
        this.locations = await this.fetchResults()
    }
}
</script>
