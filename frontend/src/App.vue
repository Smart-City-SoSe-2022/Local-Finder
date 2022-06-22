<template>
<div id="body">
    <Header/>
    <div v-show="this.debug" style="background: pink">
        <router-link to="/results">Ergebnisse</router-link>
    </div>
    <router-view/>
    <div class="footer">
        <router-link to="/about">SmartCityCorp&copy;</router-link> 
    </div>
</div>
</template>

<script>
import Header from '@/components/Header.vue'

export default {
name: 'App',
components: {
    Header
},
    data() {
        return {
            debug: true,
        }
    }
}
</script>

<style>
html {
    background: #eef;
}
#app {
    font-family: Avenir, Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;
}

#body {
    max-width: 80ch;
    padding: 3em 1em;
    margin: auto;
    line-height: 1.75;
    font-size: 1.3em;
}
/* Optional Header Margins
h1,h2,h3,h4,h5,h6 {
  margin: 3em 0 1em;
}

p,ul,ol {
  margin-bottom: 2em;
  color: #1d1d1d;
  font-family: sans-serif;
}

*/

/* Refactor Nav somewhere else */
#nav {
    padding: 30px;
}

#nav a {
    font-weight: bold;
    color: #2c3e50;
}

#nav a.router-link-exact-active {
    color: #42b983;
}

.button {
    background: cornflowerblue;
    padding: 5px;
    border-radius: 5px;
    font-weight: 500;
    font-size: 1.5ch;
}

.footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    font-size: 10px;
    text-align: left;
    margin-left: 20px;
    color:#ddf;
}

a {
     text-decoration: none;
}

a:visited {
    color:#2c3e50;
    text-decoration: none;
}

input {
    padding: 5px;
    border: 2px solid black;
    margin: 0 5px;
    border-radius: 10px;
}


</style>
