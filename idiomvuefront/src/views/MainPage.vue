<template>
  <div class="screen-container">
    <el-container>
      <el-header>
        <div>
          汉语成语逻辑关系推断可视化面板
        </div>
        <a href="https://github.com/Ti-Ho/Idioms_Logic_Inference">
          <div class="head-right">
              <img src="/static/img/github.png" style="height: 25px;" >
          </div>
          <div class="head-right-text">
              GitHub
          </div>
        </a>
      </el-header>
      <el-divider></el-divider>
      <el-container style="margin-left: 30px; margin-right: 30px;">
        <el-aside width="200px">
          <el-menu
                  default-active="1"
                  class="el-menu-vertical-demo"
                  @open="handleOpen"
                  @close="handleClose"
                  @select="changeComponent"
                  background-color="#545c64"
                  text-color="#fff"
                  active-text-color="#ffd04b">
            <el-menu-item index="1">
              <i class="el-icon-search"></i>
              <span slot="title">成语逻辑推断</span>
            </el-menu-item>
            <el-submenu index="2">
              <template slot="title">
                <i class="el-icon-picture-outline"></i>
                <span>模型对比</span>
              </template>
              <el-menu-item-group>
                <template slot="title">二分类</template>
                <el-menu-item index="2-1" style="font-size: x-small">二分类模型loss对比</el-menu-item>
                <el-menu-item index="2-2" style="font-size: x-small">二分类模型准确率对比</el-menu-item>
              </el-menu-item-group>
              <el-menu-item-group>
                <template slot="title">多分类</template>
                <el-menu-item index="2-3" style="font-size: x-small">多分类模型loss对比</el-menu-item>
                <el-menu-item index="2-4" style="font-size: x-small">多分类模型准确率对比</el-menu-item>
              </el-menu-item-group>
            </el-submenu>
          </el-menu>
        </el-aside>
        <el-main>
          <FormComponent v-if="this.componentId==='1'"></FormComponent>
          <modelCompareLoss v-else-if="this.componentId==='2-1'"></modelCompareLoss>
          <modelCompareAcc v-else-if="this.componentId==='2-2'"></modelCompareAcc>
          <multiClsCompareLoss v-else-if="this.componentId==='2-3'"></multiClsCompareLoss>
          <multiClsCompareAcc v-else-if="this.componentId==='2-4'"></multiClsCompareAcc>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import FormComponent from "@/components/FormComponent";
import modelCompareLoss from "@/components/modelCompareLoss";
import modelCompareAcc from "@/components/modelCompareAcc";
import multiClsCompareLoss from "@/components/multiClsCompareLoss";
import multiClsCompareAcc from "@/components/multiClsCompareAcc";
export default {
  name: "MainPage",
  components: {
    FormComponent,
    modelCompareLoss,
    modelCompareAcc,
    multiClsCompareLoss,
    multiClsCompareAcc,
  },
  data() {
    return {
      componentId : '1',
    }
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    },
    changeComponent(index) {
      this.componentId = index;
      console.log(this.componentId);
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
  background-color: white;
  color: #202020;
  text-align: center;
  line-height: 60px;
  font-weight: bold;
  font-size: larger;
  /*border-radius: 15px;*/
  margin-bottom: 0px;
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
  right: 50px;
  cursor: pointer;
  top: 2px;
  /*color: white;*/
  font-size: medium;
  letter-spacing: 1px;
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
  color: #999999;
  text-decoration:none;
}
a:active {
  color: #999999;
  text-decoration:none;
}
.el-divider {
    margin-top: 0px;
    margin-bottom: 3px;
    height: 3px;
}
</style>
