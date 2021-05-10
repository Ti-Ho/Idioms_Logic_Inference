<template>
  <div class="screen-container">
    <el-container>
      <el-header>汉语成语逻辑关系推断可视化面板</el-header>
      <el-container>
        <el-aside width="200px" style="background-color: #99a9bf">Aside</el-aside>
        <el-main>
          <!--     form 表单      -->
          <el-form ref="form" :model="form" label-width="120px" label-position="left">
            <el-row><div class="step-font">步骤1: 输入成语</div></el-row>
            <el-row>
              <el-col :span="7">
                <el-form-item label="成语1">
                  <el-input v-model="form.idiom1"></el-input>
                </el-form-item>
              </el-col>
              <el-col :span="2"><div class="grid-content"></div></el-col>
              <el-col :span="7">
                <el-form-item label="成语2">
                  <el-input v-model="form.idiom2"></el-input>
                </el-form-item>
              </el-col>
            </el-row>
            <el-divider></el-divider>
            <el-row><div class="step-font">步骤2: 选择推断模型</div></el-row>
            <el-row>
              <el-col :span="7">
                <el-form-item label="选择模型">
                  <el-radio-group v-model="form.model_type">
                    <el-radio label="二分类模型"></el-radio>
                    <el-radio label="多分类模型"></el-radio>
                  </el-radio-group>
                </el-form-item>
              </el-col>
              <el-col :span="2"><div class="grid-content"></div></el-col>
              <el-col :span="10">
                <el-form-item label="选择输出层结构">
                  <el-radio-group v-model="form.ifPool">
                    <el-radio label="使用mean max pool输出层"></el-radio>
                    <el-radio label="使用CLS向量推断"></el-radio>
                  </el-radio-group>
                </el-form-item>
              </el-col>
            </el-row>
            <el-divider></el-divider>
            <el-row>
              <el-col :span=7>
                <div class="step-font">步骤3: 开始推断</div>
              </el-col>
              <el-col :span="12">
                <el-form-item>
                  <el-button type="primary" @click="onSubmit">开始推断</el-button>
                  <el-button @click="clear">取消</el-button>
                </el-form-item>
              </el-col>
            </el-row>
          </el-form>
          <el-divider></el-divider>
          <!--     结果图表      -->
          <el-row style="height: 55%">
            <el-row>
              <div class="step-font">模型推断结果</div>
            </el-row>
            <!-- 有数据 显示图表 -->
            <el-row v-if="hasRes==true" style="margin:0px; height:95%">
              <div style="margin:0px">显示图表</div>
            </el-row>
            <!-- 无数据 显示其它 -->
            <el-row v-else style="margin:0px; height:95%">
              <div style="margin:0px">显示其它</div>
            </el-row>
          </el-row>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: "MainPage",
  data() {
    return {
      form: {
        idiom1: '',
        idiom2: '',
        model_type: '二分类模型',
        ifPool: '使用mean max pool输出层',
      },
      hasRes: false
    }
  },
  methods: {
    onSubmit() {
      this.hasRes = !this.hasRes;
      console.log('submit!');
      console.log(this.form);
    },
    clear() {
      this.form.idiom1 = '';
      this.form.idiom2 = '';
      this.hasRes = false;
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

.el-row {
  margin-bottom: 5px;
}
.el-col {
  border-radius: 4px;
}
.bg-purple-dark {
  background: #99a9bf;
}
.bg-purple {
  background: #d3dce6;
}
.bg-purple-light {
  background: #e5e9f2;
}
.grid-content {
  border-radius: 4px;
  min-height: 36px;
}

.el-divider {
  height: 1px;
  /*background-color: #003366;*/
  margin-top: 0px !important;
  margin-bottom: 10px !important;
}
.step-font{
  font-weight: bold;
  font-family: 'Microsoft YaHei';
  margin-left: 0px;
  font-size: medium;
  color: dimgrey;
}
</style>
