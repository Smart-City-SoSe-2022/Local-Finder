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
			console.log("insanity check 1")
			const response = await fetch("api/getReservations")
			const data = await response.json()
			console.log(data)
			return data;
    	},
  	},
	async created() {
		console.log("insanity check 0")
		this.reservations = await this.fetchReservation()
	}
};
</script>
