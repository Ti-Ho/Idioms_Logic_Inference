<template>
  <div id="app">
    <MainPage></MainPage>
  </div>
</template>

<script>
import MainPage from "@/views/MainPage";

export default {
  name: 'App',
  components: {
    MainPage
  }
}
</script>

<style>
  html, body, #app {
    width: 100%;
    height: 100%;
    padding: 0;
    margin: 0;
    overflow: hidden;
  }
</style>
