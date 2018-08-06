<template>
  <div id="app">
    <div id="nav">
      <router-link to="/">Demo page</router-link> |
      <router-link to="/about">Demo graphics</router-link>
    </div>
    <hr>
    <router-view class="content"/>
    <hr>
    <div class="footer">
      Developed by Silence & Befezdow 2k18
    </div>
  </div>
</template>

<style lang="scss">
html, body {
  height: 100%;
}
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  display: flex;
  flex-direction: column;
  height: 100%;
  color: #2c3e50;
}
#nav {
  padding: 30px;
  background: cadetblue;
  a {
    font-weight: bold;
    color: #2c3e50;
    &.router-link-exact-active {
      color: #42b983;
    }
  }
}
.content {
  padding: 20px;
  flex: 1 0 auto;
}

.footer {
  flex-shrink: 0;
  padding: 20px;
  background: aqua;
}

</style>
