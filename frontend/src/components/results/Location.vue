<template>
    <table>
        <tr @click="openLocation(location.id)">
            <td>
                <img alt="Webportal" src="@/assets/logo.png" width="100" height="100">
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
	name: 'Location',
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
    },
	methods: {
      openLocation(id) {
          this.$emit('open-loc', location.id)
      }
	},
    emits: ['open-loc']
}
</script>


<style scoped>
#lokal * {
    margin: 0 auto;
}
</style>