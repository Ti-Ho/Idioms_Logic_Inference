<template>
    <div style="margin-left: 10px; margin-right: 10px; height: 100%">
        <!--     form 表单      -->
        <el-form ref="form" :model="form" label-width="120px" label-position="left" class="demo-ruleForm" :rules="rules">
            <el-row><div class="step-font">步骤1: 输入成语</div></el-row>
            <el-row>
                <el-col :span="8">
                    <el-form-item label="成语1" prop="idiom1">
                        <el-input placeholder="请输入成语1" v-model="form.idiom1"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="2" style="margin-left: 10px; margin-right: 20px;">
                    <el-button v-if="hasRes" type="success" @click="openIdiom1msg" icon="el-icon-check" round></el-button>
                </el-col>
                <el-col :span="2" v-if="!hasRes" style="margin-left: 10px; margin-right: 20px;"><div class="grid-content"></div></el-col>
                <el-col :span="8">
                    <el-form-item label="成语2" prop="idiom2">
                        <el-input placeholder="请输入成语2" v-model="form.idiom2"></el-input>
                    </el-form-item>
                </el-col>
                <el-col :span="2" style="margin-left: 10px; margin-right: 20px;">
                    <el-button v-if="hasRes" type="success" @click="openIdiom2msg" icon="el-icon-check" round></el-button>
                </el-col>
            </el-row>
            <el-divider></el-divider>
            <el-row><div class="step-font">步骤2: 选择推断模型</div></el-row>
            <el-row>
                <el-col :span="8">
                    <el-form-item label="选择模型">
                        <el-radio-group v-model="form.model_type">
                            <el-radio label="二分类模型" border></el-radio>
                            <el-radio label="多分类模型" border></el-radio>
                        </el-radio-group>
                    </el-form-item>
                </el-col>
                <el-col :span="1"><div class="grid-content"></div></el-col>
                <el-col :span="11">
                    <el-form-item label="选择输出层结构">
                        <el-radio-group v-model="form.ifPool">
                            <el-radio label="使用mean max pool输出层" border></el-radio>
                            <el-radio label="使用CLS向量推断" border></el-radio>
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
                        <el-button type="primary" @click="onSubmit('form')">开始推断</el-button>
                        <el-button @click="clear">取消</el-button>
                    </el-form-item>
                </el-col>
            </el-row>
        </el-form>
        <el-divider></el-divider>
        <!--     结果图表      -->
        <el-row style="height: 45%">
            <el-row>
                <div class="step-font" v-if="hasRes">模型推断结果</div>
                <div class="step-font" v-else>推断结果示例</div>
            </el-row>
            <!-- 有数据 显示图表 -->
            <el-row v-if="hasRes==true" style="margin:0px; height:92%">
                <div style="margin:0px; height: 100%" v-if="form.model_type=='二分类模型'">
                    <BinaryClsChart :p1="p1" :p2="p2"></BinaryClsChart>
                </div>
                <div style="margin:0px; height: 100%" v-else>
                    <MultiClsChart :p0="p0" :p1="p1" :p2="p2"></MultiClsChart>
                </div>
            </el-row>
            <!-- 无数据 显示示例 -->
            <el-row v-else style="margin:0px; height: 92%">
                <BinaryClsChart :p1=0.89 :p2=0.87></BinaryClsChart>
            </el-row>
        </el-row>
    </div>
</template>

<script>
import BinaryClsChart from "@/components/BinaryClsChart";
import MultiClsChart from "@/components/MultiClsChart";
import qs from 'qs'
export default {
  name: "FormComponent",
  components: {
      BinaryClsChart,
      MultiClsChart
  },
  data() {
    return {
      resData: null,
      form: {
        idiom1: '',
        idiom2: '',
        model_type: '二分类模型',
        ifPool: '使用mean max pool输出层',
      },
      rules: {
        idiom1: [
            { required: true, message: '请输入成语1', trigger: 'blur'}
        ],
        idiom2: [
            { required: true, message: '请输入成语2', trigger: 'blur'}
        ]
      },
      hasRes: false,
      p0: 0.01,
      p1: 0.02,
      p2: 0.03,
      example1: 'example1',
      explanation1: 'explanation1',
      example2: 'example2',
      explanation2: 'explanation2',
    }
  },
  methods: {
    // 点击开始推断后的操作
    onSubmit(formName) {
        this.$refs[formName].validate((valid) => {
            if (valid) {
                alert('提交!');
                this.PostFunc();
            } else {
                console.log('error submit!!');
                alert('输入错误！');
                return false;
            }
        });
    },
     async PostFunc() {
         const params = qs.stringify({
             idiom1: this.form.idiom1,
             idiom2: this.form.idiom2,
             model_type: (this.form.model_type === "二分类模型") ? 1 : 0,
             ifPool: (this.form.ifPool === "使用mean max pool输出层") ? 1 : 0
         });
         var allData = null;
         await this.$http.post('/get_res', params)
             .then(function (response) {
                 // console.log(response.data);
                 allData = response.data
             })
             .catch(function (error) {
                 console.log(error);
             });
         this.resData = allData;
         if (this.resData.status === 0) {
             this.hasRes = true;
             if (this.form.model_type === '二分类模型') {
                 this.p1 = this.resData.predictions[0];
                 this.p2 = this.resData.predictions[1];
             } else {
                 this.p0 = this.resData.predictions[0];
                 this.p1 = this.resData.predictions[1];
                 this.p2 = this.resData.predictions[2];
             }
             this.explanation1 = this.resData.explanation1;
             this.explanation2 = this.resData.explanation2;
             this.example1 = this.resData.example1;
             this.example2 = this.resData.example2;
         } else if (this.resData.status === 1) {
             this.$alert(this.form.idiom1 + '不是成语', '错误提示', {
                 confirmButtonText: '确定',
             })
         } else {
             this.$alert(this.form.idiom2 + '不是成语', '错误提示', {
                 confirmButtonText: '确定',
             })
         }
         console.log(this.resData.predictions);
     },
    clear() {
      this.form.idiom1 = '';
      this.form.idiom2 = '';
      this.hasRes = false;
    },
    openIdiom1msg() {
      this.$alert("成语解释: " + this.explanation1 + '<br/>' + "成语造句: " + this.example1, this.form.idiom1 + '的相关输入', {
        confirmButtonText: '确定',
        dangerouslyUseHTMLString: true
      });
    },
    openIdiom2msg() {
      this.$alert("成语解释: " + this.explanation2 + '<br/>' + "成语造句: " + this.example2, this.form.idiom2 + '的相关输入', {
        confirmButtonText: '确定',
        dangerouslyUseHTMLString: true
      });
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
