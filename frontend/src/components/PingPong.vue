<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p> {{ pong }} </p>
  </div>
</template>


<!-- Requests /ping from server to recive 'pong' and put it inside <p> -->
<script>
import axios from 'axios'

export default {
  name: 'PingPong',
  props: {
    msg: String
  },
  data() {
    return {
      pong: 'empty',
    }
  },
  methods: {
    getPingPong() {
      const path = 'api/ping'
      axios.get(path)
        .then((res) => {
          this.pong = res.data
        })
    }
  },
  created() {
    this.getPingPong()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a { 
  color: #42b983;
}
</style>
