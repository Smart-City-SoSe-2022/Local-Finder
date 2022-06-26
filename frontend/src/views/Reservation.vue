<template>
  	<div>
    	<h1>Reservierungen</h1>
    	<ReservationList :list="reservations" />
  	</div>
</template>

<script>
import ReservationList from "@/components/reservations/ReservationList.vue";

export default {
  	name: "Reservation",
  	components: {
    	ReservationList,
  	},
	data() {
        return {
            reservations: []
        }
    },
	methods: {
		async fetchReservation() {
			const response = await fetch("http://server.it-humke.de:9004/api/getReservations", {
				redirect: 'follow',
                credentials: 'include'
            })
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
