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
        multi_cls_acc : [0.41821201, 0.4643741 , 0.4893674 , 0.49679147, 0.50150517,
            0.50287643, 0.50586534, 0.50791151, 0.50912207, 0.51079329,
            0.51309658, 0.5162569 , 0.5186566 , 0.51984573, 0.52000643,
            0.52404521, 0.52288821, 0.52330602, 0.52513793, 0.52588784,
            0.52759119, 0.5278483 , 0.52841609, 0.52765547, 0.52816969,
            0.52746264, 0.52951952, 0.52896245, 0.52996947, 0.52905887,
            0.53116932, 0.52996947, 0.53091221, 0.53116932, 0.5306551 ,
            0.53126573, 0.53147999, 0.53141572, 0.53303337, 0.53211206,
            0.53339761, 0.53233703, 0.53260485, 0.53288339, 0.53444748,
            0.53309765, 0.53246558, 0.53432964, 0.53502598, 0.53419037,
            0.53457604, 0.53292624, 0.53472602, 0.53450104, 0.53500455,
            0.53360116, 0.53409395, 0.53395468, 0.53467245],
        multi_pool_acc: [0.48691414, 0.50430125, 0.50667952, 0.50890782, 0.51084686,
            0.51387862, 0.51631046, 0.51756388, 0.52090632, 0.52358455,
            0.5251165 , 0.52669131, 0.52859821, 0.53037656, 0.53039799,
            0.53309765, 0.53385827, 0.53341904, 0.53559377, 0.53739354,
            0.53817559, 0.53826129, 0.54018962, 0.5400075 , 0.54013605,
            0.54275001, 0.54285714, 0.54219294, 0.5434035 , 0.54466763,
            0.54497831, 0.5462103 , 0.54542825, 0.54631742, 0.54501045,
            0.5463817 , 0.54660667, 0.5483636 , 0.54989555, 0.54868499,
            0.54715303, 0.54783866, 0.55028121, 0.54933848, 0.54917778,
            0.54776367, 0.55034549, 0.54837431, 0.55074187, 0.55090257,
            0.5499384 , 0.55059189, 0.54854572, 0.54947774, 0.55050619,
            0.55035621, 0.55038834, 0.55104183, 0.55003482, 0.55141679,
            0.55120253, 0.5511811 , 0.55028121, 0.54972414, 0.55132037,
            0.55045262, 0.55088114, 0.5501848 , 0.55003482, 0.55158819,
            0.55173818, 0.5505169 , 0.55085971, 0.55047405, 0.55008838,
            0.54947774, 0.55037763, 0.5509347 , 0.55050619, 0.55092399]
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
              'epoch50','epoch51','epoch52','epoch53','epoch54','epoch55','epoch56',
              'epoch57', 'epoch58','epoch59','epoch60','epoch61','epoch62','epoch63',
              'epoch64', 'epoch65', 'epoch66','epoch66','epoch67','epoch68','epoch69',
              'epoch70','epoch71', 'epoch72', 'epoch73','epoch74','epoch75','epoch76',
              'epoch77','epoch78','epoch79', 'epoch80']
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
