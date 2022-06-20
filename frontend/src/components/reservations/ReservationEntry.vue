<template>
    <table>
        <tr>
            <td>
                <img alt="Webportal" src="@/assets/placeholder.png" width="100" height="100">
            </td>
            <td id="lokal">
                <p style="font-weight: 700;"> {{location.name}} </p>
                <p style="margin-left: 20px"> {{location.address}} </p>
            </td>
            <td>
                <p> 300 km </p>
            </td>
            <td>
                <p> {{location.open}} </p>
            </td>
        </tr>
    </table>
</template>

<script>
export default {
	name: 'ReservationEntry',
	props: {
        location: Object,
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