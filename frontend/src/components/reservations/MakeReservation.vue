<template>
    <div>
        <input type="text" v-model="date" name="date" placeholder="Datum angeben..."/>
        <input type="text" v-model="time" name="time" placeholder="Uhrzeit angeben..."/>
        <button class="button" tpye="button" @click="onSubmit()"> Reservieren </button>
    </div>
</template>

<script>
export default {
    name: "MakeReservation",
    data() {
        return {
            date: '',
            time: ''
        }
    },
    methods: {
        async onSubmit() {
            const response = await fetch('/api/requestReservation',{
                method: 'POST',
                headers: {
                    'Content-type': 'application/json',
                },
                body: JSON.stringify({
                    'datetime': this.date + ', '+this.time,
                    'localId': this.$route.params.id
                })
            })
            const data = await response.text()
            console.log(data)
        }
    }
}

</script>
