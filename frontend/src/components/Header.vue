<template>
<div>
    <div id="header">
        <img alt="Webportal" @click="goToPortal" src="../assets/Portal.png" width="100" height="100">
        <router-link to="/">
            <img alt="LokalFinder" src="../assets/Home.png" width="100" height="100">
        </router-link>
        <img alt="LokalFinder" src="../assets/luppe.png" width="100" height="100"
            @click="toggleSearchBox"
            :class="{ open: search}"
            v-show="isNotHome()"
            >
        <div id="account">
            <router-link to="/favoriten" class="button">
                Favoriten
            </router-link>
            <router-link to="/reservierungen" class="button">
                Reservierungen
            </router-link>
        </div>
        <div id="own">
            Meine Lokale:
            <div class="button" 
                @click="openLocation(lokal.id)"
                v-show="owner" 
                :key="lokal.id" 
                v-for="lokal in ownedLokals"
                > {{lokal.name}}
            </div>
            <router-link to="/newLocation" class="add_lokal" data-hover="Lokal hinzufügen"> + </router-link>
        </div>
        

    </div>
    <div id="searchBox" v-show="this.search" >
        <Search />
    </div>
</div>
</template>

<script>
import Search from '@/components/Search.vue'

export default {
    name: 'Header',
    components: {
        Search
    }, 
    data() {
        return {
            search: false,
            owner: false,
            ownedLokals: []
        }
    },
    watch: {
        '$route.path': function() {
            this.search = false
        }
    },
    methods: {
        goToPortal() {
            window.location.href='http://server.it-humke.de:8001/'
        },
        toggleSearchBox() {
            this.search = !this.search;
        },
        isNotHome() {
            if (this.$route.path == "/") {
                return false
            } else {
                return true
            }
        },
        async isOwner() {
            const response = await fetch('http://server.it-humke.de:9004/api/isOwner', {
                redirect: 'follow',
                credentials: 'include'
            })
            const data = await response.text()
            if (data == "True") return true
            return false
        },
        async fetchOwnedLokals() {
            const response = await fetch('http://server.it-humke.de:9004/api/getOwningLokals', {
                redirect: 'follow',
                credentials: 'include'
            })
            if(response.ok){
                const data = await response.json()
                return data
            } else {
                console.log(await response.text())
            }
            
        },
        openLocation(id) {
            this.$router.push({ name: 'ReservationLokal', params: { id: id} })
        },
    },
    async created() {
        this.owner = await this.isOwner()
        this.ownedLokals = await this.fetchOwnedLokals()
    }
}
</script>

<style scoped>
    #header {
        position: relative;
        min-width: 70ch;
        text-align: left;
    }
    #header * {
        vertical-align: middle;
        padding: 5px;
    }

    .open {
        background: #ddf;
        border-radius: 10px 10px 0 0;
    }

    #account {
        position: absolute;
        top: 1em;
        right: 1em;
    }

    #account * {
        margin: 0 10px;
        padding: 5px 10px;
        font-size: 1em;
        color: black;
        border: 3px solid black;
    }

    #own {
        position: absolute;
        top: 3em;
        right: 1em;
        display: flex;
        flex-direction: row;
    }

    #own * {
        margin: 0 3px;
        padding: 0 3px;
        font-size: 0.8em;
        color: black;
        cursor: pointer;
        border: 2px solid black;

    }

    .add_lokal {
        background: #cce;
        border-radius: 100%;
        cursor: pointer;
        display: inline-block;
        text-align: center;
        width: 1.3em;
    }
    
</style>