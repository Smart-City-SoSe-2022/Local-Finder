<template>
<div>
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
}
</script>
