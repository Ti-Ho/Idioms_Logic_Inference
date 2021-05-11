<template>
  <div style="width: 100%; height: 100%; margin: 0px">
    <div style="width: 70%; height: 100%; margin: 10px;" class="com-chart" ref="multiPieChart_ref"></div>
  </div>
</template>

<script>
export default {
  name: "MultiClsChart",
  data() {
    return {
      chartInstance: null,
    }
  },
  props: {
    p0: Number,
    p1: Number,
    p2: Number
  },
  mounted () {
    this.initChart();
  },
  methods: {
    // 初始化echartsInstance对象
    initChart () {
      this.chartInstance = this.$echarts.init(this.$refs.multiPieChart_ref)
      const initOption = {
        title: {
          text: '多分类模型推断结果',
          subtext: '纯属虚构',
          left: 'center',
          top: '5%',
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: '5%'
        },
        series: [
          {
            name: '访问来源',
            type: 'pie',
            radius: '50%',
            data: [
              {value: this.p0, name: '无逻辑关系'},
              {value: this.p1, name: '并列关系'},
              {value: this.p2, name: '转折关系'},
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };
      this.chartInstance.setOption(initOption)
    },
  }
}
</script>

<style scoped>
.com-chart {
  width: 100%;
  height: 100%;
  overflow: hidden;
  /*border-radius: 20px;*/
}
</style>
