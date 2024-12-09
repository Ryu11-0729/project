<template>
  <div id="div1" style="width: 100%; height: 100%; overflow-y: auto;" v-loading="loading" element-loading-text="数据分析中~~" >
    <el-carousel :interval="10000" type="card" style="width: 100%; height: 90%; background-color: white">
      <el-carousel-item v-for="item in imgsurl" :key="item" style="width: 70%; height: 250%;  margin-left: -10%;">
        <img :src="item" style="width: 100%; height: 100%;"/>
      </el-carousel-item>
    </el-carousel>
      Kruskal-Wallis H检验:
      <el-table
      :data="tableData1"
      style="width: 100%;">
      <el-table-column
        prop="Feature"
        label="Feature"
        width="180">
      </el-table-column>
      <el-table-column
        prop="H"
        label="H-statistic"
        width="180">
      </el-table-column>
      <el-table-column
        prop="p"
        label="p-value"
        width="180">
      </el-table-column>
    </el-table>
    卡方检验:
    <el-table
      :data="tableData2"
      style="width: 100%">
      <el-table-column
        prop="Feature"
        label="Feature"
        width="180">
      </el-table-column>
      <el-table-column
        prop="chi2"
        label="chi2"
        width="180">
      </el-table-column>
      <el-table-column
        prop="p"
        label="p-value"
        width="180">
      </el-table-column>
      <el-table-column
        prop="dof"
        label="dof"
        width="180">
      </el-table-column>
    </el-table>
    </div>
</template>
<script>
import { request } from '@/api/service'
export default {
  name: 'ordinaryUser',
  data () {
    return {
      hApp: {},
      hScreen: {},
      hBattery: {},
      hNumber: {},
      hData: {},
      hAge: {},
      kafang: {},
      loading: true,
      imgsurl: [
        'http://4322fb9a.r15.cpolar.top/images/xiangxiantu1.png',
        'http://4322fb9a.r15.cpolar.top/images/fenbutu1.png',
        'http://4322fb9a.r15.cpolar.top/images/xingwei_and_shebeileixingfenbu.png',
        'http://4322fb9a.r15.cpolar.top/images/xingwei_and_caozuoxitongfenbu.png',
        'http://4322fb9a.r15.cpolar.top/images/xingwei_and_meitianyidongfenbu.png',
        'http://4322fb9a.r15.cpolar.top/images/xingwei_and_pingmumeitianfenbu.png',
        'http://4322fb9a.r15.cpolar.top/images/xingwei_and_meiridianchifenbu.png',
        'http://4322fb9a.r15.cpolar.top/images/xingwei_and_shebeishanganzhuangfenbu.png',
        'http://4322fb9a.r15.cpolar.top/images/xingwei_and_meitianyidongfenbu.png',
        'http://4322fb9a.r15.cpolar.top/images/xingwei_and_yonghunianlingfenbu.png',
        'http://4322fb9a.r15.cpolar.top/images/xingwei_and_yonghuxingbiefenbu.png',
        'http://4322fb9a.r15.cpolar.top/images/bianliangzhijianrelitu.png'
      ],
      tableData1: [],
      tableData2: []
    }
  },
  methods: {
    handle () {
      console.log(1)
    }
  },
  created () {
    const that = this
    this.loading = true
    request({
      url: '/api/system/data_analyze',
      method: 'get',
      params: {}
    }).then((res) => {
      that.loading = false
      that.hApp = res.data.Kruska.App
      that.hScreen = res.data.Kruska.Screen
      that.hBattery = res.data.Kruska.Battery
      that.hNumber = res.data.Kruska.Number
      that.hData = res.data.Kruska.Data
      that.hAge = res.data.Kruska.Age
      that.kafang = res.data.kafang

      that.tableData1 = [
        {
          Feature: 'App Usage Time (min/day)',
          H: that.hApp.hh,
          p: that.hApp.p
        },
        {
          Feature: 'Screen On Time (hours/day)',
          H: that.hScreen.hh,
          p: that.hScreen.p
        },
        {
          Feature: 'Battery Drain (mAh/day)',
          H: that.hBattery.hh,
          p: that.hBattery.p
        },
        {
          Feature: 'Number of Apps Installed',
          H: that.hNumber.hh,
          p: that.hNumber.p
        },
        {
          Feature: 'Data Usage (MB/day)',
          H: that.hData.hh,
          p: that.hData.p
        },
        {
          Feature: 'Age',
          H: that.hAge.hh,
          p: that.hAge.p
        }
      ]
      that.tableData2 = [
        {
          Feature: 'Device Model',
          chi2: that.kafang.Device.chi2,
          p: that.kafang.Device.p,
          dof: that.kafang.Device.dof
        },
        {
          Feature: 'Operating System',
          chi2: that.kafang.Operating.chi2,
          p: that.kafang.Operating.p,
          dof: that.kafang.Operating.dof
        },
        {
          Feature: 'Gender',
          chi2: that.kafang.Gender.chi2,
          p: that.kafang.Gender.p,
          dof: that.kafang.Gender.dof
        }
      ]
    })
  }
}
</script>

<style>
.el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
}
.el-carousel__item:nth-child(2n) {
  background-color: #99a9bf;
}
.el-carousel__item:nth-child(2n+1) {
  background-color: #d3dce6;
}

table {
    width: 100%;
    border-collapse: collapse;
}
th, td {
    border: 1px solid black;
    padding: 8px;
    text-align: center;
}
th {
    background-color: #f2f2f2;
}
</style>
