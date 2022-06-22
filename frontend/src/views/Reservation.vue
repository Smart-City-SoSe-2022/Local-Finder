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
			const response = await fetch("api/getReservations")
			const data = await response.json()
			return data;
    	},
  	},
	async created() {
		this.reservations = await this.fetchReservation()
	}
};
</script>
