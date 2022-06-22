<template>
    <div>
        <h1> Neues Lokal anlegen</h1>
        <form class="inputbox">
            <input type="text" v-model="lokalname" name="lokalname" placeholder="Name des Lokals angeben..."/>
            <input type="text" v-model="street" name="street" placeholder="Straße angeben..."/>
            <input type="text" v-model="plz" name="plz" placeholder="Postleitzahl angeben..."/>
            <input type="text" v-model="city" name="city" placeholder="Stadt angeben..."/>
            <button class="button" tpye="button" @click="onSubmit()"> Reservieren </button>
        </form>
    </div>
</template>

<script>
export default {
    name: "MakeReservation",
    data() {
        return {
            lokalname: '',
            street: '',
            plz: '',
            city: ''
        }
    },
    methods: {
        async onSubmit() {
            if (!this.lokalname) {
                alert("Bitte einen Lokalnamen angeben!")
                return
            }
            if (!this.street) {
                alert("Bitte eine Straße angeben!")
                return
            }
            if (!this.plz) {
                alert("Bitte eine Postleitzahl angeben!")
                return
            }
            if (!this.city) {
                alert("Bitte eine Stadt angeben!")
                return
            }
            const response = await fetch('/api/requestLocal',{
                method: 'POST',
                headers: {
                    'Content-type': 'application/json',
                },
                body: JSON.stringify({
                    'lokalname': this.date + ', '+this.time,
                    'street': this.street,
                    'plz': this.plz,
                    'city': this.city
                })
            })
            const data = await response.text()
            if (response.status === 200) {
                alert("Anfrage zur für das Lokal wurde gesendet. Bitte warten Sie auf die Antwort der Stadtverwaltung.")
                this.$router.push({ name: 'Home' })
            } else {
                alert("Etwas ist schief gelaufen...")
            }
        }
    }
}
</script>

<style scoped>
.inputbox {
    display: flex;
    flex-direction: column;
    margin: auto;
    width: 50%;
}

.inputbox * {
    margin-top: 10px;
}
</style>