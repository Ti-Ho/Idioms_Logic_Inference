<template>
  <div class="screen-container">
    <el-container>
      <el-header>汉语成语逻辑关系推断可视化面板</el-header>
      <el-container>
        <el-aside width="200px" style="background-color: #99a9bf">Aside</el-aside>
        <el-main>
          <FormComponent></FormComponent>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import FormComponent from "@/components/FormComponent";
export default {
  name: "MainPage",
  components: {
    FormComponent
  }
}
</script>

<style scoped>
.screen-container {
    width: 100%;
    height: 100%;
    padding: 0 0px;
    /*background-color: #161522;*/
    /*color: #fff;*/
    box-sizing: border-box;
}

.el-container {
  height: 100% !important;
}
.el-header{
  background-color: #000;
  color: white;
  text-align: center;
  line-height: 60px;
  font-weight: bolder;
  font-size: larger;
  /*border-radius: 15px;*/
  margin-bottom: 5px;
}
.el-main {
  padding: 0px !important;
}
</style>
