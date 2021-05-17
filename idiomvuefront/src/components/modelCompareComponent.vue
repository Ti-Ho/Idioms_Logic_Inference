<template>
  <div style="margin-left: 10px; margin-right: 10px; height: 100%">
    <el-form ref="form" :model="comForm" label-width="120px" label-position="left">
      <el-row>
        <el-col :span="12">
          <el-row><div class="step-font">选择对比推断模型1</div></el-row>
          <el-row>
              <el-form-item label="选择模型">
                <el-radio-group v-model="comForm.model_type1" @change="modelChange">
                  <el-radio label="二分类模型" border></el-radio>
                  <el-radio label="多分类模型" border></el-radio>
                </el-radio-group>
              </el-form-item>
          </el-row>
        </el-col>
        <el-col :span="12">
          <el-row><div class="step-font">选择对比推断模型2</div></el-row>
          <el-row>
            <el-form-item label="选择模型">
              <el-radio-group v-model="comForm.model_type2" @change="modelChange">
                <el-radio label="二分类模型" border></el-radio>
                <el-radio label="多分类模型" border></el-radio>
              </el-radio-group>
            </el-form-item>
          </el-row>
        </el-col>
      </el-row>
      <el-row>
        <el-col :span="12">
          <el-form-item label="选择输出层结构">
            <el-radio-group v-model="comForm.ifPool1" @change="modelChange">
              <el-radio label="使用mean max pool输出层" border></el-radio>
              <el-radio label="使用CLS向量推断" border></el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="选择输出层结构">
            <el-radio-group v-model="comForm.ifPool2" @change="modelChange">
              <el-radio label="使用mean max pool输出层" border></el-radio>
              <el-radio label="使用CLS向量推断" border></el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>
    </el-form>
    <el-divider></el-divider>
    <div class="line-div">
      <div class="com-chart" ref="lossLineChart_ref"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "modelCompareComponent",
  data() {
    return {
      comForm: {
        model_type1: '二分类模型',
        ifPool1: '使用mean max pool输出层',
        model_type2: '二分类模型',
        ifPool2: '使用mean max pool输出层',
      },
      chartInstance: null,
      linedata: {
        bi_cls_1: {
          train_loss: [],
          xAxis_epoch: []
        },
        bi_cls_2: {
          train_loss: [],
          xAxis_epoch: []
        },
        bi_pool_1: {
          train_loss: [],
          xAxis_epoch: []
        },
        bi_pool_2: {
          train_loss: [],
          xAxis_epoch: []
        },
        multi_cls: {
          train_loss: [],
          xAxis_epoch: []
        },
        multi_pool: {
          train_loss: [],
          xAxis_epoch: []
        }
      }
    }
  },
  mounted () {
    this.initChart();
    console.log("model compare Component mounted")
  },
  methods : {
    // 初始化echartsInstance对象
    initChart () {
      this.chartInstance = this.$echarts.init(this.$refs.lossLineChart_ref);
      const initOption = {
        title: {
          text: '模型对比'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['二分类#CLS向量#并列关系', '二分类#CLS向量#转折关系', '二分类#MMP#并列关系', '二分类#MMP#转折关系', '多分类#CLS', '多分类#MMP']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '二分类#CLS向量#转折关系',
            type: 'line',
            data: [220, 182, 191, 234, 290, 330, 310]
          },
          {
            name: '二分类#MMP#并列关系',
            type: 'line',
            data: [150, 232, 201, 154, 190, 330, 410]
          },
          {
            name: '二分类#MMP#转折关系',
            type: 'line',
            data: [320, 332, 301, 334, 390, 330, 320]
          },
          {
            name: '多分类#CLS',
            type: 'line',
            data: [820, 932, 901, 934, 1290, 1330, 1320]
          },
          {
            name: '多分类#MMP',
            type: 'line',
            data: [120, 240, 500, 780, 700, 490, 982]
          }
        ]
      };
      this.chartInstance.setOption(initOption);
    },
    modelChange () {
      if (this.comForm.model_type1 === '二分类模型' && this.comForm.ifPool1 === "使用mean max pool输出层"
          && this.comForm.model_type1 === "二分类模型" && this.comForm.ifPool2 === "使用mean max pool输出层"){
        const dataOption = {
          series: [
            {
              name: '二分类#MMP#转折关系',
              type: 'line',
              data: [320, 332, 301, 334, 390, 330, 320]
            },
            {
              name: '二分类#MMP#并列关系',
              type: 'line',
              data: [150, 232, 201, 154, 190, 330, 410]
            },
          ]
        };
        this.chartInstance.setOption(dataOption);
        console.log(1)
      }
      else if (this.comForm.model_type1 === '二分类模型' && this.comForm.ifPool1 === "使用mean max pool输出层"
              && this.comForm.model_type1 === "二分类模型" && this.comForm.ifPool2 !== "使用mean max pool输出层"){
        console.log(2)
      }
      else if (this.comForm.model_type1 === '二分类模型' && this.comForm.ifPool1 === "使用mean max pool输出层"
              && this.comForm.model_type1 !== "二分类模型" && this.comForm.ifPool2 === "使用mean max pool输出层"){
        console.log(3)
      }
      else if (this.comForm.model_type1 === '二分类模型' && this.comForm.ifPool1 === "使用mean max pool输出层"
              && this.comForm.model_type1 !== "二分类模型" && this.comForm.ifPool2 !== "使用mean max pool输出层"){
        console.log(4)
      }
      else if (this.comForm.model_type1 === '二分类模型' && this.comForm.ifPool1 !== "使用mean max pool输出层"
              && this.comForm.model_type1 === "二分类模型" && this.comForm.ifPool2 === "使用mean max pool输出层"){
        console.log(5)
      }
      else if (this.comForm.model_type1 === '二分类模型' && this.comForm.ifPool1 !== "使用mean max pool输出层"
              && this.comForm.model_type1 === "二分类模型" && this.comForm.ifPool2 !== "使用mean max pool输出层"){
        console.log(6)
      }
      else if (this.comForm.model_type1 === '二分类模型' && this.comForm.ifPool1 !== "使用mean max pool输出层"
              && this.comForm.model_type1 !== "二分类模型" && this.comForm.ifPool2 === "使用mean max pool输出层"){
        console.log(7)
      }
      else if (this.comForm.model_type1 === '二分类模型' && this.comForm.ifPool1 !== "使用mean max pool输出层"
              && this.comForm.model_type1 !== "二分类模型" && this.comForm.ifPool2 !== "使用mean max pool输出层"){
        console.log(8)
      }
      else if (this.comForm.model_type1 !== '二分类模型' && this.comForm.ifPool1 === "使用mean max pool输出层"
              && this.comForm.model_type1 === "二分类模型" && this.comForm.ifPool2 === "使用mean max pool输出层"){
        console.log(9)
      }
      else if (this.comForm.model_type1 !== '二分类模型' && this.comForm.ifPool1 === "使用mean max pool输出层"
              && this.comForm.model_type1 === "二分类模型" && this.comForm.ifPool2 !== "使用mean max pool输出层"){
        console.log(10)
      }
      else if (this.comForm.model_type1 !== '二分类模型' && this.comForm.ifPool1 === "使用mean max pool输出层"
              && this.comForm.model_type1 !== "二分类模型" && this.comForm.ifPool2 === "使用mean max pool输出层"){
        console.log(11)
      }
      else if (this.comForm.model_type1 !== '二分类模型' && this.comForm.ifPool1 === "使用mean max pool输出层"
              && this.comForm.model_type1 !== "二分类模型" && this.comForm.ifPool2 !== "使用mean max pool输出层"){
        console.log(12)
      }
      else if (this.comForm.model_type1 !== '二分类模型' && this.comForm.ifPool1 !== "使用mean max pool输出层"
              && this.comForm.model_type1 === "二分类模型" && this.comForm.ifPool2 === "使用mean max pool输出层"){
        console.log(13)
      }
      else if (this.comForm.model_type1 !== '二分类模型' && this.comForm.ifPool1 !== "使用mean max pool输出层"
              && this.comForm.model_type1 === "二分类模型" && this.comForm.ifPool2 !== "使用mean max pool输出层"){
        console.log(14)
      }
      else if (this.comForm.model_type1 !== '二分类模型' && this.comForm.ifPool1 !== "使用mean max pool输出层"
              && this.comForm.model_type1 !== "二分类模型" && this.comForm.ifPool2 === "使用mean max pool输出层"){
        console.log(15)
      }else {
        console.log(16)
      }
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
.step-font{
  font-weight: bold;
  font-family: 'Microsoft YaHei';
  margin-left: 0px;
  font-size: medium;
  color: dimgrey;
}
.el-divider {
  height: 1px;
  margin-top: 0px !important;
  margin-bottom: 10px !important;
}
.line-div {
  height: 68%;
  width: 100%;
  text-align: center;
}
.com-chart {
  width: 100%;
  height: 100%;
}
</style>
