<template>
  <div class="hello" style="min-width: 1450px;text-align:left">
    <div>摘要</div>
    <div>成都4核机器: &nbsp;&nbsp; 正常:{{abstract["4"]["right"]}} &nbsp;&nbsp; 异常:{{abstract["4"]["error"]}}</div>
    <div>成都6核机器: &nbsp;&nbsp;正常:{{abstract["6"]["right"]}}  &nbsp;&nbsp;异常:{{abstract["6"]["error"]}}</div>
    <div>海外机器: &nbsp;&nbsp;正常:{{abstract["abroad"]["right"]}} &nbsp;&nbsp; 异常:{{abstract["abroad"]["error"]}}</div>
    <div>未知: &nbsp;&nbsp;正常:{{abstract["0"]["right"]}} &nbsp;&nbsp; 异常:{{abstract["0"]["error"]}}</div>
    <div style="color:#f00">{{error_pid}}</div>

    <div style="margin-top:48px">详情</div>
    <div v-for="(value, key) in abstract['detail'] " :key="key">
        pid:{{key}} &nbsp;&nbsp;正常:{{value["right"] }} &nbsp;&nbsp;异常:{{value["error"] }}
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import axios from 'axios'
import * as echarts from 'echarts';
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data: function(){
    return {
      abstract: {
          "4": {"right": 0, "error": 0},
          "6": {"right": 0, "error": 0},
          "0": {"right": 0, "error": 0},
          "abroad": {"right": 0, "error": 0},
          "detail": {"413": {"right": 100, "error": 100}, "414": {"right": 100, "error": 100}, "415": {"right": 99, "error": 99}, "416": {"right": 100, "error": 100}, "417": {"right": 40, "error": 40}, "418": {"right": 8, "error": 8}, "421": {"right": 89, "error": 89}, "422": {"right": 43, "error": 43}, "423": {"right": 86, "error": 86}, "424": {"right": 86, "error": 86}, "451": {"right": 96, "error": 96}, "453": {"right": 94, "error": 94}, "455": {"right": 95, "error": 95}, "457": {"right": 105, "error": 105}, "460": {"right": 87, "error": 87}, "461": {"right": 100, "error": 100}, "462": {"right": 100, "error": 100}, "463": {"right": 96, "error": 96}, "467": {"right": 100, "error": 100}, "468": {"right": 100, "error": 100}, "469": {"right": 99, "error": 99}, "470": {"right": 100, "error": 100}, "471": {"right": 83, "error": 83}, "472": {"right": 72, "error": 72}, "473": {"right": 99, "error": 99}, "474": {"right": 99, "error": 99}, "475": {"right": 99, "error": 99}, "476": {"right": 99, "error": 99}, "1922": {"right": 44, "error": 44}, "1923": {"right": 96, "error": 96}, "1924": {"right": 88, "error": 88}, "1925": {"right": 88, "error": 88}, "1926": {"right": 88, "error": 88}, "1934": {"right": 88, "error": 88}}
      },
      error_pid:"",
      special_mechines:[],
      mechines:[]
    }
  },
  methods:{
    FlushErrorPid: function(){
      
    },
  },
  
  mounted:function(){
      let self = this
      axios.get("/rest/get_bml_xq").then(function(data){
        data = data.data
        console.log(data)
        self.abstract = data.data
        // self.abstract["4"] = data.data["4"]
        // self.abstract["6"] = data.data["6"]
        // self.abstract["0"] = data.data["0"]
        // self.abstract["abroad"] = data.data["abroad"]
      })
  }
}
// path('/rest/get_latest_daily_mechine_count', views.get_latest_daily_mechine_count),
// path('/rest/get_latest_daily_mechine_user_count', views.get_latest_daily_mechine_user_count)
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
