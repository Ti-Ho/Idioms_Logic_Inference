<template>
    <div style="margin-left: 10px; margin-right: 10px;">
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
                <div style="margin:0px" v-if="form.model_type=='二分类模型'">
                    <BinaryClsChart :p1="p1" :p2="p2"></BinaryClsChart>
                </div>
                <div style="margin:0px" v-else>
                    <MultiClsChart :p0="p0" :p1="p1" :p2="p2"></MultiClsChart>
                </div>
            </el-row>
            <!-- 无数据 显示其它 -->
            <el-row v-else style="margin:0px; height:95%">
                <div style="margin:0px">显示其它</div>
            </el-row>
        </el-row>
    </div>
</template>

<script>
import BinaryClsChart from "@/components/BinaryClsChart";
import MultiClsChart from "@/components/MultiClsChart";
export default {
  name: "FormComponent",
  components: {
      BinaryClsChart,
      MultiClsChart
  },
  data() {
    return {
      form: {
        idiom1: '',
        idiom2: '',
        model_type: '二分类模型',
        ifPool: '使用mean max pool输出层',
      },
      hasRes: false,
      p0: 'p0',
      p1: 'p1',
      p2: 'p2'
    }
  },
  methods: {
    onSubmit() {
      // Todo 与后端连接后 修改hasres的逻辑修改
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
.el-row {
    margin-bottom: 5px;
}
.el-col {
    border-radius: 4px;
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
