<template>
  <div style="margin-left: 10px; margin-right: 10px; height: 100%">
    <el-form ref="form" :model="comForm" label-width="120px" label-position="left">
      <el-row>
        <el-col :span="12">
          <el-row><div class="step-font">选择对比推断模型1</div></el-row>
          <el-row>
              <el-form-item label="选择模型">
                <el-radio-group v-model="comForm.model_type1">
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
              <el-radio-group v-model="comForm.model_type2">
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
            <el-radio-group v-model="comForm.ifPool1">
              <el-radio label="使用mean max pool输出层" border></el-radio>
              <el-radio label="使用CLS向量推断" border></el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="选择输出层结构">
            <el-radio-group v-model="comForm.ifPool2">
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
    }
  },
  mounted () {
    this.initChart();
  },
  methods : {
    // 初始化echartsInstance对象
    initChart () {
      this.chartInstance = this.$echarts.init(this.$refs.lossLineChart_ref);
      const initOption = {
        title: {
          text: '折线图堆叠'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['邮件营销', '联盟广告', '视频广告', '直接访问', '搜索引擎']
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
            name: '邮件营销',
            type: 'line',
            data: [120, 132, 101, 134, 90, 230, 210]
          },
          {
            name: '联盟广告',
            type: 'line',
            data: [220, 182, 191, 234, 290, 330, 310]
          },
          {
            name: '视频广告',
            type: 'line',
            data: [150, 232, 201, 154, 190, 330, 410]
          },
          {
            name: '直接访问',
            type: 'line',
            data: [320, 332, 301, 334, 390, 330, 320]
          },
          {
            name: '搜索引擎',
            type: 'line',
            data: [820, 932, 901, 934, 1290, 1330, 1320]
          }
        ]
      };
      this.chartInstance.setOption(initOption)
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
