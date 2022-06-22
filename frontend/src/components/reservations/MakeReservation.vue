<template>
    <div>
        <h2 style="user-select: none; cursor: pointer" @click="this.show = !this.show"> Termin Reservieren </h2>
        <form v-show="show">
            <input type="text" v-model="date" name="date" placeholder="Datum angeben..."/>
            <input type="text" v-model="time" name="time" placeholder="Uhrzeit angeben..."/>
            <button class="button" type="button" @click="onSubmit()"> Reservieren </button>
        </form>
    </div>

</template>

<script>
export default {
    name: "MakeReservation",
    data() {
        return {
            date: '',
            time: '',
            show: false
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
