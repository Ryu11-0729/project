<template>
  <div class="scrollable" v-loading="loading" element-loading-text="预测中请稍后~"
  element-loading-spinner="el-icon-loading">
    随机森林混淆矩阵：
    <div id="confusionMatrix"></div>
    <div id="output"></div>
  </div>
</template>

<script>
import { request } from '@/api/service'
export default {
  name: 'predict',
  data () {
    return {
      value: '',
      value1: '',
      loading: true
    }
  },
  methods: {
    handle () {
      console.log(2)
    }
  },
  created () {
    const that = this
    this.loading = true
    request({
      url: '/api/system/data_predict',
      method: 'get',
      params: {}
    }).then((res) => {
      if (res.data[0].startsWith('模型评估指标')) {
        that.value = res.data[1]
        that.value1 = res.data[0]
      } else {
        that.value = res.data[0]
        that.value1 = res.data[1]
      }
      
      let st = that.value
      st = st.trim()

      var lines = st.split('\n')

      var table = document.createElement('table')
      var headerRow = [''].concat(lines[0].trim().split(/\s{2,}/))
      var tableHeader = table.insertRow(-1)
      headerRow.forEach(function (headerText) {
        var headerCell = document.createElement('th')
        headerCell.textContent = headerText
        tableHeader.appendChild(headerCell)
      })
      for (var i = 1; i < lines.length; i++) {
        var row = lines[i].trim().split(/\s{2,}/)
        var tableRow = table.insertRow(-1)
        row.forEach(function (cellText) {
          var cell = tableRow.insertCell(-1)
          cell.textContent = cellText
        })
      }
      document.getElementById('confusionMatrix').appendChild(table)
      
      const str = that.value1
      // 将换行符替换为HTML的换行标签
      var htmlStr = str.replace(/\n/g, '<br>')
      // 设置div的innerHTML属性来显示换行的字符串
      document.getElementById('output').innerHTML = htmlStr
      that.loading = false
    })
  }
}
</script>

<style>
.scrollable {
  width: 100%; /* 设置宽度 */
  height: 100%; /* 设置高度 */
  overflow: auto; /* 超出内容显示滚动条 */
  border: 1px solid #ccc; /* 可选：给 div 添加边框以区分区域 */
}
table {
    width: 100%;
    border-collapse: collapse;
  }
  th, td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: center;
  }
  th {
    background-color: #f2f2f2;
  }
  tr:hover {
    background-color: #f5f5f5;
  }
</style>
