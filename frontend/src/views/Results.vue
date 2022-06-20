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
        }, 
        async fetchSearch() {
            const body = {
                name: this.$route.query.name,
                type: this.$route.query.type,
                city: this.$route.query.city,
            }
            const response = await fetch('api/search', {
                method: 'POST',
                headers: {
                    'Content-type': 'application/json',
                },
                body: JSON.stringify(body)
            })
            var data
            if (response.status === 200) {
                data = await response.json()
                return data
            } 
        }
    },
    async created() {
        console.log()
        if (Object.entries(this.$route.query).length > 0) {
            this.locations = await this.fetchSearch()
        } else {
            this.locations = await this.fetchResults()
        }
        
    }
}
</script>
