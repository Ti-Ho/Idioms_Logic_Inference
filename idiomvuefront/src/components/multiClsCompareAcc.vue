<template>
  <div style="margin-left: 10px; margin-right: 10px; height: 100%">
    <div class="line-div">
      <div class="com-chart" ref="labelAccBar_ref"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "multiClsCompareAcc",
  data () {
    return {
      chartInstance: null,
    };
  },
  mounted () {
    this.initChart();
  },
  methods : {
    // 初始化echartsInstance对象
    initChart () {
      this.chartInstance = this.$echarts.init(this.$refs.labelAccBar_ref);
      const initOption = {
        legend: {},
        tooltip: {},
        dataset: {
          source: [
            ['label', '无逻辑关系', '并列关系', '转折关系'],
            ['多分类 CLS', 0.9651, 0.9508, 0.8747],
            ['多分类 Mean Max Pool', 0.9202, 0.9276, 0.9528],
            ['二分类 并列关系 CLS', 0.9764, 0.9596],
            ['二分类 并列关系 Mean Max Pool', 0.9594, 0.9733],
            ['二分类 转折关系 CLS', 0.9764, 0, 0.9596],
            ['二分类 转折关系 Mean Max Pool', 0.9567, 0, 0.9464],
          ]
        },
        xAxis: {
          type: 'category',
          axisLabel: {
            interval:0, //强制显示文字
            show: true,
          },
        },
        yAxis: {},
        // Declare several bar series, each will be mapped
        // to a column of dataset.source by default.
        series: [
          {type: 'bar'},
          {type: 'bar'},
          {type: 'bar'}
        ],
          grid: {
              left: '1%',
              right: '4%',
              bottom: '3%',
              top: '13%',
              containLabel: true
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
