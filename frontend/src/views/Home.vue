<template>
  <div class="home">
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
