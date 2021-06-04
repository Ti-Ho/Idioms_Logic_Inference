<template>
  <div style="margin-left: 10px; margin-right: 10px; height: 100%">
    <div class="line-div">
      <div class="com-chart" ref="lossBarChart_ref"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "modelCompareComponent",
  data() {
    return {
      chartInstance: null,
      barChartData: {
        multi_cls: 0.0038,
        multi_mmp: 0.000067,
        bi_syn_cls: 0.005738,
        bi_syn_mmp: 0.007744,
        bi_ant_cls: 0.000805,
        bi_ant_mmp: 0.010322
      }
    }
  },
  mounted () {
    this.initChart();
  },
  methods : {
    // 初始化echartsInstance对象
    initChart () {
      this.chartInstance = this.$echarts.init(this.$refs.lossBarChart_ref);
      const initOption = {
        title: {
          top: '5%',
          text: '成语逻辑推断模型测试集Loss对比'
        },
        legend: {
          // data: ['二分类#CLS向量#并列关系', '二分类#CLS向量#转折关系', '二分类#MMP#并列关系', '二分类#MMP#转折关系', '多分类#CLS', '多分类#MMP']
          top: '5%'
        },
        grid: {
          left: '1%',
          right: '4%',
          bottom: '3%',
          top: '13%',
          containLabel: true
        },
        toolbox: {
          feature: {
            saveAsImage: {}
          }
        },
        xAxis: {
          type: 'category',
          data: ['多分类 CLS输出结构', '多分类 Mean Max Pool输出结构', '二分类 并列关系 CLS输出结构',
            '二分类 并列关系 Mean Max Pool输出结构', '二分类 转折关系 CLS输出结构', '二分类 转折关系 Mean Max Pool输出结构'],
          axisLabel: {
            interval:0, //强制显示文字
            show: true,
          },
        },
        yAxis: {
          type: 'value',
        },
        series: [{
          data: [{value: this.barChartData.multi_cls, itemStyle: {color: '#123456'}}, {value: this.barChartData.multi_mmp, itemStyle: {color: '#3CB371'}},
            {value: this.barChartData.bi_syn_cls, itemStyle: {color: '#CD853F'}}, {value: this.barChartData.bi_syn_mmp, itemStyle: {color: '#FF4500'}},
            {value: this.barChartData.bi_ant_cls, itemStyle: {color: '#FFD700'}}, {value: this.barChartData.bi_ant_mmp, itemStyle: {color: '#008B8B'}}],
          type: 'bar',
          showBackground: true,
          backgroundStyle: {
            color: 'rgba(180, 180, 180, 0.2)'
          }
        }],
        tooltip: {
          trigger: 'axis',
          axisPointer: {            // 坐标轴指示器，坐标轴触发有效
            type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
          }
        },
      };
      this.chartInstance.setOption(initOption);
    },
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
  height: 90%;
  width: 100%;
  text-align: center;
}
.com-chart {
  width: 100%;
  height: 100%;
}
</style>
