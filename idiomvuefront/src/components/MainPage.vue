<template>
  <div class="screen-container">
    <el-container>
      <el-header>汉语成语逻辑关系推断可视化面板</el-header>
      <el-main>
<!--        <el-row>*步骤1: 输入成语</el-row>-->
<!--        <el-row>-->
<!--          <el-col :span="12"><div class="grid-content bg-purple"></div></el-col>-->
<!--          <el-col :span="12"><div class="grid-content bg-purple-light"></div></el-col>-->
<!--        </el-row>-->
<!--        <el-divider></el-divider>-->
<!--        <el-row>*步骤2: 选择模型</el-row>-->
<!--        <el-row>-->
<!--          <el-col :span="12"><div class="grid-content bg-purple"></div></el-col>-->
<!--          <el-col :span="12"><div class="grid-content bg-purple-light"></div></el-col>-->
<!--        </el-row>-->
<!--        <el-divider></el-divider>-->
<!--        <el-row>-->
<!--          <el-col :span="24"><div class="grid-content bg-purple-dark">步骤3：开始推断</div></el-col>-->
<!--        </el-row>-->
<!--        <el-divider></el-divider>-->
<!--        <el-row>-->
<!--          图表-->
<!--        </el-row>-->

        <el-form ref="form" :model="form" label-width="80px">
          <el-row>*步骤1: 输入成语</el-row>
          <el-row>
            <el-col :span="7">
              <el-form-item label="成语1">
                <el-input v-model="form.idiom1"></el-input>
              </el-form-item>
            </el-col>
            <el-col :span="7">
              <el-form-item label="成语2">
                <el-input v-model="form.idiom2"></el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-divider></el-divider>
          <el-row>*步骤2: 选择模型</el-row>

          <el-form-item label="活动名称">
            <el-input v-model="form.name"></el-input>
          </el-form-item>
          <el-form-item label="活动区域">
            <el-select v-model="form.region" placeholder="请选择活动区域">
              <el-option label="区域一" value="shanghai"></el-option>
              <el-option label="区域二" value="beijing"></el-option>
            </el-select>
          </el-form-item>
          <el-form-item label="活动时间">
            <el-col :span="11">
              <el-date-picker type="date" placeholder="选择日期" v-model="form.date1" style="width: 100%;"></el-date-picker>
            </el-col>
            <el-col class="line" :span="2">-</el-col>
            <el-col :span="11">
              <el-time-picker placeholder="选择时间" v-model="form.date2" style="width: 100%;"></el-time-picker>
            </el-col>
          </el-form-item>
          <el-form-item label="即时配送">
            <el-switch v-model="form.delivery"></el-switch>
          </el-form-item>
          <el-form-item label="活动性质">
            <el-checkbox-group v-model="form.type">
              <el-checkbox label="美食/餐厅线上活动" name="type"></el-checkbox>
              <el-checkbox label="地推活动" name="type"></el-checkbox>
              <el-checkbox label="线下主题活动" name="type"></el-checkbox>
              <el-checkbox label="单纯品牌曝光" name="type"></el-checkbox>
            </el-checkbox-group>
          </el-form-item>
          <el-form-item label="特殊资源">
            <el-radio-group v-model="form.resource">
              <el-radio label="线上品牌商赞助"></el-radio>
              <el-radio label="线下场地免费"></el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item label="活动形式">
            <el-input type="textarea" v-model="form.desc"></el-input>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="onSubmit">立即创建</el-button>
            <el-button>取消</el-button>
          </el-form-item>
        </el-form>
      </el-main>
    </el-container>
  </div>
</template>

<script>
export default {
  name: "MainPage",
  data() {
    return {
      form: {
        name: '',
        region: '',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        desc: '',
        idiom1: '',
        idiom2: ''
      }
    }
  },
  methods: {
    onSubmit() {
      console.log('submit!');
      console.log(this.form);
    }
  }
}
</script>

<style scoped>
.screen-container {
    width: 100%;
    height: 100%;
    padding: 0 50px;
    /*background-color: #161522;*/
    /*color: #fff;*/
    box-sizing: border-box;
}

.el-container {
  height: 100% !important;
}
.el-header{
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
  line-height: 60px;
}
.el-main {
  padding: 0px !important;
}

.el-row {
  margin-bottom: 10px;
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
  height: 2px;
  /*background-color: #003366;*/
  margin-top: 0px !important;
  margin-bottom: 0px !important;
}
</style>
