<template>
  	<div>
    	<h1>Gast Reservierungen</h1>
    	<ReservationLokalList :list="reservations" />
  	</div>
</template>

<script>
import ReservationLokalList from "@/components/reservationsLokal/ReservationLokalList.vue";

export default {
  	name: "ReservationLokal",
  	components: {
    	ReservationLokalList,
  	},
	data() {
        return {
            reservations: []
        }
    },
    watch: {
        '$route.path': async function() {
            this.reservations = await this.fetchReservation()
        }
    },
	methods: {
		async fetchReservation() {
			const response = await fetch("http://server.it-humke.de:9004/api/getLokalReservations?id="+this.$route.params.id, {
				redirect: 'follow',
                credentials: 'include'
            })
			if (response.status === 501) {
                console.log( "Lokal konnte nicht gefunden werden")
                return
            }
            if(response.ok){
                const data = await response.json()
                return data
            } else {
                console.log(await response.text())
				return null
            }
    	},
  	},
	async created() {
		this.reservations = await this.fetchReservation()
	}
};
</script>
