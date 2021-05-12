<template>
    <div style="width: 100%; height: 100%; margin: 0px">
        <el-row style="padding-left: 15%;">
            <el-col :span="14">
                <div class="com-chart" ref="multiPieChart_ref"></div>
            </el-col>
            <el-col :span="7">
                <div class="res-div">
                    <el-tag effect="dark" v-if="this.res==='无逻辑关系'" color="#C23531">{{this.res}}</el-tag>
                    <el-tag effect="dark" v-else-if="this.res==='并列关系'" color="#2F4554">{{this.res}}</el-tag>
                    <el-tag effect="dark" v-else color="#61A0A8">{{this.res}}</el-tag>
                </div>
            </el-col>
        </el-row>
    </div>
</template>

<script>
export default {
  name: "MultiClsChart",
  data() {
    return {
      chartInstance: null,
      res: ''
    }
  },
  props: {
    p0: Number,
    p1: Number,
    p2: Number
  },
  mounted () {
    this.initChart();
    if (this.p0 >= this.p1 && this.p0 >= this.p2)
        this.res = "无逻辑关系";
    else if (this.p1 >= this.p0 && this.p1 >= this.p2)
        this.res = "并列关系";
    else this.res = "转折关系";
  },
  methods: {
    // 初始化echartsInstance对象
    initChart () {
      this.chartInstance = this.$echarts.init(this.$refs.multiPieChart_ref)
      const initOption = {
        title: {
          text: '多分类模型推断结果',
          subtext: '成语推断',
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
            radius: '60%',
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
            },
            center: ['50%', '65%'],
            label: {
              formatter: '{b} {d}%'
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
