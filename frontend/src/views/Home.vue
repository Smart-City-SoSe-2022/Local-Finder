<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png">
    <PingPong msg="Ping Pong!"/>
  </div>
</template>

<script>
import PingPong from '@/components/PingPong.vue'

export default {
  name: 'Home',
  components: {
    PingPong
  }
}
</script>
