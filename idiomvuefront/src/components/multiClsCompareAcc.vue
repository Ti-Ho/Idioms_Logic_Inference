<template>
  <div style="margin-left: 10px; margin-right: 10px; height: 100%">
    <div class="line-div">
      <div class="com-chart" ref="accMultiLineChart_ref"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "multiClsCompareAcc",
  data () {
    return {
      chartInstance: null,
      lineData: {
        multi_cls_acc : [0.41529364, 0.44134725, 0.46472264, 0.48424142, 0.49013348,
          0.49643263, 0.49668973, 0.49844664, 0.50048208, 0.5028389 ,
          0.50178904, 0.50189617, 0.5045101 , 0.50352452, 0.50579564,
          0.50699548, 0.50648126, 0.50802391, 0.50939515, 0.50956656,
          0.50920232, 0.50958798, 0.51125919, 0.5101022 , 0.5109378 ,
          0.51098065, 0.51046644, 0.51087352, 0.50995222, 0.51226619,
          0.51393739, 0.51200908, 0.51256615, 0.5133589 , 0.5124376 ,
          0.51267328, 0.51239475, 0.51563002, 0.5141088 , 0.51556574,
          0.51614424, 0.51539434, 0.51256615, 0.5158657 , 0.51601568,
          0.51787972, 0.51423735, 0.51597283, 0.51665845, 0.51691556,
          0.5167013 ],
        multi_pool_acc: [0.46489405, 0.49981788, 0.50363165, 0.50294603, 0.50455295,
          0.50590277, 0.50823817, 0.50999507, 0.50950228, 0.51179483,
          0.51387312, 0.5149444 , 0.51723695, 0.5180297 , 0.51867247,
          0.52278619, 0.52390033, 0.52360037, 0.5253787 , 0.52842114,
          0.52951385, 0.52692135, 0.5311422 , 0.53221349, 0.53206351,
          0.53382041, 0.53298481, 0.5341418 , 0.5341418 , 0.53568444,
          0.53559874, 0.53658432, 0.53735564, 0.53711996, 0.53628436,
          0.53891972, 0.53932681, 0.53647719, 0.53720566, 0.53838408,
          0.54014098, 0.53846978, 0.54168363, 0.53774131, 0.53992672,
          0.5390697 , 0.5384912 , 0.54067662, 0.53919825, 0.54069805,
          0.54125512, 0.54003385, 0.54039809, 0.54024811, 0.54106228,
          0.54110514, 0.54170505]
      }
    };
  },
  mounted () {
    this.initChart();
  },
  methods : {
    // 初始化echartsInstance对象
    initChart () {
      this.chartInstance = this.$echarts.init(this.$refs.accMultiLineChart_ref);
      const initOption = {
        title: {
          top: '5%',
          text: '多分类模型ACC对比'
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
            'epoch50','epoch51','epoch52','epoch53','epoch54','epoch55','epoch56']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: '多分类#CLS#ACC',
            type: 'line',
            data: this.lineData.multi_cls_acc
          },
          {
            name: '多分类模型#MMP#ACC',
            type: 'line',
            data: this.lineData.multi_pool_acc
          },
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
