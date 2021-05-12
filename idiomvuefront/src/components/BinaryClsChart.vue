<template>
  <div style="width: 100%; height: 100%; margin: 0px">
      <el-row>
          <el-col :span=10>
              <div class="com-chart" ref="binaryPieChart_ref"></div>
          </el-col>
      </el-row>
  </div>
</template>

<script>
export default {
  name: "BinaryClsChart",
  data() {
    return {
      chartInstance: null,
    }
  },
  props: {
    p1: Number,
    p2: Number
  },
  mounted () {
    this.initChart();
  },
  methods: {
    // 初始化echartsInstance对象
    initChart () {
      this.chartInstance = this.$echarts.init(this.$refs.binaryPieChart_ref)
      const initOption = {
        title: {
          text: '二分类模型推断结果',
          subtext: '纯属虚构',
          left: 'center',
          top: '3%',
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: '5%',
        },
        // Todo 修改grid
        grid: {
          left: "10%",
          top: "30%",
          // show: true
        },
        series: [
          {
            name: '访问来源',
            type: 'pie',
            radius: '50%',
            data: [
              {value: this.p1, name: '搜索引擎'},
              {value: this.p2, name: '直接访问'}
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
.el-row {
    margin-bottom: 0px;
    height: 100%;
}
.el-col {
    border-radius: 4px;
    height: 100%;
}
</style>
