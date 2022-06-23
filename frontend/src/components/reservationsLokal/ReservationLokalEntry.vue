<template>
    <table>
        <tr>
            <td>
                <img alt="Webportal" src="@/assets/placeholder.png" width="100" height="100">
            </td>
            <td id="lokal">
                <p style="font-weight: 700;"> {{person.reservedName}} </p>
            </td>
            <td>
                <p> {{person.datetime}} </p>
            </td>
        </tr>
    </table>
</template>

<script>
export default {
	name: 'ReservationLokalEntry',
	props: {
        person: Object,
	},
    data() {
        return {
            show: false,
            name: "",
            date: "",
            name_list: [],
        }
    }
}
</script>


<style scoped>
#lokal * {
    margin: 0 auto;
}
</style>