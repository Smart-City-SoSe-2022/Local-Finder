<template>
<div>
    <div id="header">
        <img alt="Webportal" src="../assets/logo.png" width="100" height="100">
        <router-link to="/">
            <img alt="LokalFinder" src="../assets/logo.png" width="100" height="100">
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
        search: false
      }
  },
  methods: {
      toggleSearchBox() {
          this.search = !this.search;
      },
      isNotHome() {
        if (this.$route.path == "/") {
            return false
        } else {
            return true
        }
      }
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
    
</style>