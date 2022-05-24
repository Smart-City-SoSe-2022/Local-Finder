<template>
    <div>
        <LocationList :list="locations" @delete="del" 
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
            locations: [
                {
                    "id": 1,
                    "name": "Loc1",
                    "address": "Straße Da 1",
                    "open": "17 Uhr"
                },
                {
                    "id": 2,
                    "name": "Loc2",
                    "address": "Straße Dort 7",
                    "open": "10 Uhr biss 3 oder so"
                },
                {
                    "id": 3,
                    "name": "Loc3",
                    "address": "Weg ist weg 9001",
                    "open": "Wenn's passt."
                },
                {
                    "id": 4,
                    "name": "Loc1",
                    "address": "Straße Da 1",
                    "open": "17 Uhr"
                },
                {
                    "id": 5,
                    "name": "Loc2",
                    "address": "Straße Dort 7",
                    "open": "10 Uhr biss 3 oder so"
                },
                {
                    "id": 6,
                    "name": "Loc3",
                    "address": "Weg ist weg 9001",
                    "open": "Wenn's passt."
                }
            ]
        }
    },
    methods: {
        openLocation(id) {
            this.$router.push({ name: 'LocalPage', params: { id: id} })
        }
    }
}
</script>
