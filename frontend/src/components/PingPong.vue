<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <p> {{ pong }} </p>
  </div>
</template>


<!-- PingPong.vue is a testing component 
  Requests /api calls from server to recive 'pong' and put it inside <p> 

  getPingPong creates a DB entry
  getRabbit communicates with rabbitMQ
-->
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
    /* test function pingpong
      calls the backend and creates a test object in the database
    */
    getPingPong() {
      const path = 'api/ping'
      axios.get(path)
        .then((res) => {
          this.pong = res.data
        })
    },
    /* test function rabbit
      tests rabbitmq calls
    */
    getRabbit() {
      const path = 'api/rabbit'
      axios.get(path)
        .then((res) => {
          this.pong = res.data
        })
    }
  },
  created() {
    //this.getPingPong()
    this.getRabbit()
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
