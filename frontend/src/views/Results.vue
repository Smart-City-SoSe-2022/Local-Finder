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
            const response = await fetch('http://server.it-humke.de:9004/api/getLokals')
            if(response.ok){
                const data = await response.json()
                return data
            } else {
                console.log(await response.text())
                return {}
            }
        }, 
        async fetchSearch() {
            const body = {
                name: this.$route.query.name,
                type: this.$route.query.type,
                city: this.$route.query.city,
            }
            const response = await fetch('http://server.it-humke.de:9004/api/search', {
                method: 'POST',
                headers: {
                    'Content-type': 'application/json',
                },
                body: JSON.stringify(body)
            })
            var data
            if(response.ok){
                const data = await response.json()
                return data
            } else {
                console.log(await response.text())
            }
        }
    },
    async created() {
        if (Object.entries(this.$route.query).length > 0) {
            this.locations = await this.fetchSearch()
        } else {
            this.locations = await this.fetchResults()
        }
        
    }
}
</script>
