<template>
  <div class="screen-container">
    <el-container>
      <el-header>Header</el-header>
      <el-main>Main</el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: "MainPage"
}
</script>

<style scoped>
  .screen-container {
    width: 100%;
    height: 100%;
    padding: 0 15px;
    color: #fff;
    box-sizing: border-box;
  }
  .el-header{
    font-size: x-large;
    text-align: center;
    line-height: 40px;
    border-radius: 10px;
    letter-spacing: 10px;
    height: 40px !important;
  }
  .el-container {
    padding-left: 0;
    padding-right: 0;
    height: 100% !important;
  }
  .el-main {
    padding: 0px !important;
  }
</style>
