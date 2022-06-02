<template>
  <div class="hello" style="min-width: 1450px">
    <el-row>
      <div>异常的pid：</div>
      <div style="color:#f00">{{error_pid}}</div>
    </el-row>
    <div>特别关注中的异常机器</div>
    <el-table
      :data="special_mechines"
      stripe
      style="width: 100%;margin-top:12px;">
      <el-table-column 
        prop = "name"
        label = "name"
        :show-overflow-tooltip="true"
        width=180>
      </el-table-column>
      <el-table-column 
        prop = "pid"
        label = "pid"
        width=80>
      </el-table-column>
      <el-table-column 
        prop = "p_init"
        label = "p_init"
        width=80>
      </el-table-column>
      <el-table-column 
        prop = "pubkey"
        label = "pubkey"
        :show-overflow-tooltip="true"
        min-width="180">
      </el-table-column>
      <el-table-column 
        prop = "stake_amount"
        label = "stake_amount">
      </el-table-column>
      <el-table-column 
        prop = "start_time"
        label = "start_time">
      </el-table-column>
      <el-table-column 
        prop = "status_now"
        label = "status_now">
      </el-table-column>
      <el-table-column 
        prop = "update_time"
        label = "最后查询时间">
      </el-table-column>
    </el-table>

    <div>所有的异常机器</div>
    <el-table
      :data="mechines"
      stripe
      style="width: 100%;margin-top:12px;">
      <el-table-column 
        prop = "name"
        label = "name"
        :show-overflow-tooltip="true"
        width=180>
      </el-table-column>
      <el-table-column 
        prop = "pid"
        label = "pid"
        width=80>
      </el-table-column>
      <el-table-column 
        prop = "p_init"
        label = "p_init"
        width=80>
      </el-table-column>
      <el-table-column 
        prop = "pubkey"
        label = "pubkey"
        :show-overflow-tooltip="true"
        min-width="180">
      </el-table-column>
      <el-table-column 
        prop = "stake_amount"
        label = "stake_amount">
      </el-table-column>
      <el-table-column 
        prop = "start_time"
        label = "start_time">
      </el-table-column>
      <el-table-column 
        prop = "status_now"
        label = "status_now">
      </el-table-column>
      <el-table-column 
        prop = "update_time"
        label = "最后查询时间">
      </el-table-column>
    </el-table>
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
      error_pid:"",
      special_mechines:[],
      mechines:[]
    }
  },
  methods:{
    FlushErrorPid: function(){
      let self = this
      axios.get("/rest/get_bml_error_pid").then(function(data){
        data = data.data
        for (var i = 0; i < data.data.length; i++){
          self.error_pid += data.data[i] +","
        }
      })
    },
    FlushSpecialMechines: function(){
      var self = this
      axios.get('/rest/get_bml_special_error_mechine').then(function(data){
        data = data.data
        for (var i = 0; i < data.data.length; i++) {
          data.data[i].stake_amount = data.data[i].stake_amount/10**12
          data.data[i].start_time = new Date(data.data[i].start_time*1000).toLocaleString().replace(/:\d{1,2}$/, ' ')
          data.data[i].update_time = new Date(data.data[i].update_time*1000).toLocaleString().replace(/:\d{1,2}$/, ' ')
        }
        self.special_mechines = data.data
      })
    },
    FlushMechines: function() {
      var self = this
      axios.get('/rest/get_bml_error_mechine').then(function(data){
        data = data.data
        for (var i = 0; i < data.data.length; i++) {
          data.data[i].stake_amount = data.data[i].stake_amount/10**12
          data.data[i].start_time = new Date(data.data[i].start_time*1000).toLocaleString().replace(/:\d{1,2}$/, ' ')
          data.data[i].update_time = new Date(data.data[i].update_time*1000).toLocaleString().replace(/:\d{1,2}$/, ' ')
        }
        self.mechines = data.data
      })
    }
  },
  
  mounted:function(){
    this.FlushErrorPid()
    this.FlushSpecialMechines()
    this.FlushMechines()
  }
}
// path('/rest/get_latest_daily_mechine_count', views.get_latest_daily_mechine_count),
// path('/rest/get_latest_daily_mechine_user_count', views.get_latest_daily_mechine_user_count)
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
