<template>
<div>
    <div id="liste">
        <table>
            <tr id="tablehead">
                <td></td>
                <td>Reserviert von</td>
                <td>Reserviert um</td>
            </tr>
        </table>
        <div id="loc" :key="reservation.id" v-for="reservation in list">
            <ReservationLokalEntry 
                :person="reservation"
            />
        </div>
    </div>
</div>
</template>

<script>
import ReservationLokalEntry from './ReservationLokalEntry.vue'
export default {
	name: 'ReservationList',
    props: {
        list: Array,
    },
	components: {
        ReservationLokalEntry,
	},
	methods: {
	},
	created() {
	},
}
</script>

<style>
#loc {
    margin: 5px 0;
}
#loc:nth-of-type(2n-1) {
    background: #bbf;
    border-radius: 10px;
}
#loc:nth-of-type(2n) {
    background: #ddf;
    border-radius: 10px;
}
#loc:hover {
    border: 2px solid #8cf;
    background: #8cf;
}

#tablehead {
    font-weight: 700;
}

table {
    width: 100%;
}

/* Logo */
td:nth-child(1) {
    width: 20%;
}
/* Adresse */
td:nth-child(2) {
    text-align: left;
    width: 50%;
}
/* Offen */
td:nth-child(4) {
    padding-right: 10px;
    text-align: right;
    width: 30%;
}
</style>