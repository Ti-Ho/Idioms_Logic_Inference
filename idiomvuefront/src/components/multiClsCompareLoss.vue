<template>
    <div style="margin-left: 10px; margin-right: 10px; height: 100%">
        <div class="line-div">
            <div class="com-chart" ref="multiLossLineChart_ref"></div>
        </div>
    </div>
</template>

<script>
export default {
  name: "multiClsCompareLoss",
  data () {
    return {
      chartInstance: null,
      lineData: {
        multi_cls_loss: [1.09024125, 1.0623899 , 1.0378297 , 1.01855199, 1.00708282,
            0.99995562, 0.99563378, 0.99311443, 0.99034541, 0.98837346,
            0.98703842, 0.98559544, 0.98340604, 0.98161594, 0.98147206,
            0.97889631, 0.97892533, 0.97664821, 0.97536475, 0.97452495,
            0.97346063, 0.9730385 , 0.97167261, 0.96967415, 0.97014967,
            0.96956534, 0.96894987, 0.96788465, 0.96782416, 0.96682636,
            0.9661805 , 0.96613373, 0.96664346, 0.96523445, 0.96462047,
            0.96592017, 0.96464219, 0.96363319, 0.96351703, 0.96245498,
            0.96293088, 0.96266475, 0.96273651, 0.96167047, 0.96267364,
            0.96163786, 0.96102894, 0.961822  , 0.9617052 , 0.96191596,
            0.96162592],
        multi_pool_loss: [1.0373688 , 0.99954391, 0.99157605, 0.98784667, 0.98525307,
            0.98253595, 0.9795602 , 0.97716979, 0.97400375, 0.9717297 ,
            0.96852497, 0.96594896, 0.96277808, 0.96013765, 0.95749585,
            0.95400866, 0.95047928, 0.94869281, 0.94654232, 0.94384885,
            0.94037837, 0.9404654 , 0.93891471, 0.93619817, 0.93507252,
            0.9339158 , 0.93241709, 0.93136947, 0.93092031, 0.92868649,
            0.92832957, 0.92697858, 0.9269564 , 0.92483477, 0.92520076,
            0.92430654, 0.92382296, 0.92351595, 0.92368185, 0.92206069,
            0.92183608, 0.92243669, 0.92140265, 0.92124816, 0.919753  ,
            0.9197892 , 0.91907641, 0.91991825, 0.91937882, 0.91795984,
            0.9183317 , 0.91937876, 0.91783003, 0.91867194, 0.91816645,
            0.91813608, 0.91858871]
      }
    }
  },
  mounted () {
    this.initChart();
  },
  methods: {
      // 初始化echartsInstance对象
      initChart () {
          this.chartInstance = this.$echarts.init(this.$refs.multiLossLineChart_ref);
          const initOption = {
              title: {
                  top: '5%',
                  text: '多分类模型Loss对比'
              },
              tooltip: {
                  trigger: 'axis'
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
                  boundaryGap: false,
                  data: ['epoch0', 'epoch1', 'epoch2', 'epoch3', 'epoch4', 'epoch5', 'epoch6', 'epoch7',
                      'epoch8','epoch9','epoch10','epoch11','epoch12','epoch13','epoch14',
                      'epoch15','epoch16','epoch17','epoch18','epoch19','epoch20','epoch21',
                      'epoch22','epoch23','epoch24','epoch25','epoch26','epoch27','epoch28',
                      'epoch29','epoch30','epoch31','epoch32','epoch33','epoch34','epoch35',
                      'epoch36','epoch37','epoch38','epoch39','epoch40','epoch41','epoch42',
                      'epoch43','epoch44','epoch45','epoch46','epoch47','epoch48','epoch49',
                      'epoch50','epoch51','epoch52','epoch53','epoch54','epoch55','epoch56', 'epoch57']
              },
              yAxis: {
                  type: 'value'
              },
              series: [
                  {
                      name: '多分类#CLS#Loss',
                      type: 'line',
                      data: this.lineData.multi_cls_loss
                  },
                  {
                      name: '多分类#MMP#Loss',
                      type: 'line',
                      data: this.lineData.multi_pool_loss
                  }
              ]
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

