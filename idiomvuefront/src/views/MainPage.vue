<template>
  <div class="screen-container">
    <el-container>
      <el-header>
        <div>
          汉语成语逻辑关系推断可视化面板
        </div>

        <a href="https://github.com/Ti-Ho/Idioms_Logic_Inference">
          <div class="head-right">
              <img src="/static/img/github.png" style="height: 30px;" >
          </div>
          <div class="head-right-text">
              GitHub
          </div>
        </a>
      </el-header>
      <el-container>
        <el-aside width="200px">
          <el-menu
                  default-active="2"
                  class="el-menu-vertical-demo"
                  @open="handleOpen"
                  @close="handleClose"
                  background-color="#545c64"
                  text-color="#fff"
                  active-text-color="#ffd04b">
            <el-menu-item index="1">
              <i class="el-icon-search"></i>
              <span slot="title">成语逻辑推断</span>
            </el-menu-item>
            <el-menu-item index="2">
              <i class="el-icon-monitor"></i>
              <span slot="title">模型对比</span>
            </el-menu-item>
            <el-submenu index="3">
              <template slot="title">
                <i class="el-icon-picture-outline"></i>
                <span>模型结构</span>
              </template>
              <el-menu-item-group>
                <template slot="title">二分类</template>
                <el-menu-item index="3-1">二分类 MeanMaxPool</el-menu-item>
                <el-menu-item index="3-2">二分类 CLS分类</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group>
                <template slot="title">多分类</template>
                <el-menu-item index="3-3">多分类 MeanMaxPool</el-menu-item>
                <el-menu-item index="3-4">多分类 CLS分类</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
          </el-menu>
        </el-aside>
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
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    }
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
  background-color: #505050;
  color: #eeeeee;
  text-align: center;
  line-height: 60px;
  font-weight: bold;
  font-size: larger;
  /*border-radius: 15px;*/
  margin-bottom: 5px;
  letter-spacing: 4px;
}
.el-main {
  padding: 0px !important;
}
.head-right {
  position: absolute;
  right: 120px;
  cursor: pointer;
  top: 7px;
}
.head-right-text {
  position: absolute;
  right: 30px;
  cursor: pointer;
  top: 1px;
  /*color: white;*/
  font-size: medium;
}
a:link {
  color: black;
  text-decoration:underline;
}
a:visited {
  color: black;
  text-decoration:none;
}
a:hover {
  color: white;
  text-decoration:none;
}
a:active {
  color:#FFFFFF;
  text-decoration:none;
}
</style>
