<template>
  <div class="home">
    <h1> Willkommen beim Local Finder!</h1>
    <h2> Zum Finden von Lokalen in Ihrer Nähe </h2>
    <Search />
  </div>
</template>

<script>
import Search from '@/components/Search.vue'

export default {
  name: 'Home',
  components: {
    Search
  }
}
</script>
