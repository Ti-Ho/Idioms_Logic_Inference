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
        multi_cls_loss: [1.08806571, 1.04140255, 1.01207557, 0.99851547, 0.99130438,
            0.98662469, 0.98295968, 0.97858671, 0.97428849, 0.96964623,
            0.96621126, 0.96101802, 0.95701721, 0.95346571, 0.95157601,
            0.94765653, 0.94605409, 0.94457544, 0.94217206, 0.94014134,
            0.9381985 , 0.93669155, 0.93502686, 0.93483647, 0.93322577,
            0.93250242, 0.93143952, 0.93023255, 0.9304097 , 0.92972161,
            0.92842759, 0.92827425, 0.92722423, 0.92696247, 0.92622689,
            0.92511042, 0.92558466, 0.92445677, 0.92334698, 0.92293686,
            0.92257893, 0.92243647, 0.92181137, 0.92256625, 0.92163353,
            0.92115766, 0.92093488, 0.92134903, 0.92038368, 0.91915936,
            0.92026866, 0.9198995 , 0.91991821, 0.9193992 , 0.91973889,
            0.9186527 , 0.92012262, 0.91929454, 0.91913995],
        multi_pool_loss: [1.01429281, 0.98997294, 0.98427478, 0.97976763, 0.97502065,
            0.97001523, 0.96505002, 0.96063375, 0.95584962, 0.95123284,
            0.94750163, 0.94356613, 0.94027853, 0.93758734, 0.93544807,
            0.93227385, 0.93042882, 0.92926373, 0.92572761, 0.92417624,
            0.92184534, 0.92108911, 0.91942252, 0.91870909, 0.91766496,
            0.91616081, 0.9150956 , 0.91444451, 0.91359668, 0.9127166 ,
            0.9115486 , 0.91070634, 0.91011978, 0.91041399, 0.90936643,
            0.90905133, 0.90758344, 0.90707776, 0.9073    , 0.90553473,
            0.90630462, 0.90563113, 0.90389784, 0.90450047, 0.90391622,
            0.90374554, 0.90349772, 0.90386773, 0.90294266, 0.90273718,
            0.90275678, 0.9024383 , 0.90292336, 0.90319387, 0.90213398,
            0.90283895, 0.9032495 , 0.90172369, 0.90348971, 0.90315453,
            0.90287111, 0.90314023, 0.9027786 , 0.90274359, 0.90245005,
            0.90253959, 0.90229496, 0.90301705, 0.90299999, 0.90209461,
            0.9022348 , 0.90239395, 0.90279404, 0.90282088, 0.90311949,
            0.90297404, 0.90290459, 0.90283592, 0.90250003, 0.90184949]
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

