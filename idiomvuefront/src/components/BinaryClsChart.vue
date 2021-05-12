<template>
  <div style="width: 100%; height: 100%; margin: 0px">
      <el-row>
          <el-col :span="9">
              <div class="com-chart" ref="binaryPieChart_ref"></div>
          </el-col>
          <el-col :span="9">
              <div class="com-chart" ref="binaryPieChart_ref2"></div>
          </el-col>
          <el-col :span="6">
              <div class="res-div">
                  <el-tag effect="dark" v-if="this.res==='无逻辑关系'" color="#334B5C">{{this.res}}</el-tag>
                  <el-tag effect="dark" v-else-if="this.res==='并列关系'" color="#5C7BD9">{{this.res}}</el-tag>
                  <el-tag effect="dark" v-else color="#7ED3F4">{{this.res}}</el-tag>
              </div>
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
      chartInstance2: null,
      res: ''
    }
  },
  props: {
    p1: Number,
    p2: Number
  },
  mounted () {
    this.initChart();
    if (this.p1 < 0.5 && this.p2 < 0.5)
        this.res = '无逻辑关系';
    else if (this.p1 < this.p2)
        this.res = '转折关系';
    else this.res = '并列关系';
  },
  methods: {
    // 初始化echartsInstance对象
    initChart () {
      // 并列关系图表option
      this.chartInstance = this.$echarts.init(this.$refs.binaryPieChart_ref)
      const initOption = {
        title: {
          text: '二分类模型推断结果',
          subtext: '并列关系',
          left: 'center',
          top: '5%',
        },
        tooltip: {
          trigger: 'item'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: '5%',
        },
        series: [
          {
            name: '访问来源',
            type: 'pie',
            radius: '60%',
            minAngle: 5,
            data: [
              {value: this.p1, name: '并列关系', itemStyle: {color: '#5C7BD9'}},
              {value: 1 - this.p1, name: '无逻辑关系', itemStyle: {color: '#334B5C'}}
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            center: ['50%', '65%'],
            label: {
                formatter: '{b} {d}%'
            }
          }
        ]
      };
      this.chartInstance.setOption(initOption)
      // 转折关系图表option
      this.chartInstance2 = this.$echarts.init(this.$refs.binaryPieChart_ref2)
      const initOption2 = {
        title: {
            text: '二分类模型推断结果',
            subtext: '转折关系',
            left: 'center',
            top: '5%',
        },
        tooltip: {
            trigger: 'item'
        },
        legend: {
            orient: 'vertical',
            left: 'left',
            top: '5%',
        },
        series: [
            {
                name: '访问来源',
                type: 'pie',
                radius: '60%',
                minAngle: 5,
                data: [
                    {value: this.p2, name: '转折关系', itemStyle: {color: '#7ED3F4'}},
                    {value: 1 - this.p2, name: '无逻辑关系', itemStyle: {color: '#334B5C'}}
                ],
                emphasis: {
                    itemStyle: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                },
                center: ['50%', '65%'],
                label: {
                    formatter: '{b} {d}%'
                }
            }
        ]
    };
      this.chartInstance2.setOption(initOption2)
    },
  }
}
</script>

<style scoped>
.com-chart {
  width: 100%;
  height: 100%;
  /*overflow: hidden;*/
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
.res-div {
    width: 100%;
    height: 100%;
}
.el-tag{
    position: relative;
    top: 50%;
    left: 30%;
    height: 20%;
    width: 35%;
    font-size: medium;
    display: -moz-box;/*兼容Firefox*/
    display: -webkit-box;/*兼容FSafari、Chrome*/
    -moz-box-align: center;/*兼容Firefox*/
    -webkit-box-align: center;/*兼容FSafari、Chrome */
    -moz-box-pack: center;/*兼容Firefox*/
    -webkit-box-pack: center;/*兼容FSafari、Chrome */
}
</style>
