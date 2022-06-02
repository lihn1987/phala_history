<template>
  <div class="hello" style="min-width: 1450px">
    <div>
      <el-card>
        <el-row>
          <el-col :span="6">
            <div>全网矿机数量 {{param.all_mechines_count}}</div>
          </el-col>
          <el-col :span="6">
            <div>全网算力(V值) {{param.all_v}}</div>
          </el-col>
          <el-col :span="6">
            <div>全网质押数量 {{(param.all_stake_amount/10**12).toFixed(2)}}</div>
          </el-col>
          <el-col :span="6">
            <div>全网有效质押数量 {{(param.all_right_stake_amount/10**12).toFixed(2)}}</div>
          </el-col>
        </el-row>
        <el-row>
          <el-col :span="6">
            <div>参与挖矿账户数 {{param.all_owner_count}}</div>
          </el-col>
          <el-col :span="6">
            <div>参与质押有效用户数 {{param.all_staker_count}}</div>
          </el-col>
        </el-row>
      </el-card>
    </div>
    <el-row :gutter="20" style="margin-top:24px;">
      <el-col :span="12">
        <el-card>
          <div>Top10算力拥有者</div>
          <div style="margin:16px;">
            <el-table
              :data="top_owners"
              stripe
              style="width: 100%">
              <el-table-column
                prop="name"
                label="名称"
                width=120
                :show-overflow-tooltip="true">
              </el-table-column>
              <el-table-column
                prop="addr"
                label="地址"
                :show-overflow-tooltip="true">
              </el-table-column>
              <el-table-column
                prop="v"
                label="总算力(V值)"
                width=100>
              </el-table-column>
              <el-table-column
                prop="percent"
                label="全网占比"
                width=100>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <div style="margin:16px;">
            <div>Top10 质押者</div>
            <el-table
              :data="top_stakers"
              stripe
              style="width: 100%">
              <el-table-column
                prop="name"
                label="名称"
                width=120
                :show-overflow-tooltip="true">
              </el-table-column>
              <el-table-column
                prop="addr"
                label="地址"
                :show-overflow-tooltip="true">
              </el-table-column>
              <el-table-column
                prop="amount"
                label="总金额(pha)"
                width=100>
              </el-table-column>
              <el-table-column
                prop="percent"
                label="全网占比"
                width=100>
              </el-table-column>
            </el-table>
          </div>
        </el-card>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="12">
        <div style="margin-top:24px">V值历史曲线</div>
        <div id="v-charts" style="width:100%;height:400px;">
        </div>
      </el-col>
      <el-col :span="12">
        <div style="margin-top:24px">质押历史曲线(kw)</div>
        <div id="stake-charts" style="width:100%;height:400px;">
        </div>
      </el-col>
    </el-row>

    <el-row>
      <el-col :span="12">
        <div style="margin-top:24px">机器数量历史曲线</div>
        <div id="mechine-charts" style="width:100%;height:400px;">
        </div>
      </el-col>
      <el-col :span="12">
        <div style="margin-top:24px">机器拥有者历史曲线</div>
        <div id="owner-charts" style="width:100%;height:400px;">
        </div>
      </el-col>
    </el-row>
    <div style="margin-top:24px;">机器列表</div>
    
    <el-row>
      <el-card>
        <el-row>
          <el-checkbox v-model="mechine_condition.use_pid">使用PID条件</el-checkbox>
          <div style="line-height: 32px;margin-left:24px;">pid:</div>
          <el-input v-model="mechine_condition.pid" style = "width:200px;"></el-input>
        </el-row>
      </el-card>
      
      <el-card style="margin-left:24px">
        <el-row>
          <el-checkbox v-model="mechine_condition.use_status">使用机器状态条件</el-checkbox>
          <div style="line-height: 32px;margin-left:24px;">机器状态:</div>
          <el-select v-model="mechine_condition.status" placeholder="请选择">
            <el-option key="0" label="机器状态正常" value="0"> </el-option>
            <el-option key="1" label="机器状态异常" value="1"> </el-option>
          </el-select>
        </el-row>
      </el-card>

      <el-card style="margin-left:24px">
        <el-row>
          <el-checkbox v-model="mechine_condition.use_pubkey">使用pubkey条件</el-checkbox>
          <div style="line-height: 32px;margin-left:24px;">pubkey:</div>
          <el-input v-model="mechine_condition.pubkey" style = "width:200px;"></el-input>
        </el-row>
      </el-card>
      <el-button type="primary" style="margin-left:24px;margin-top:18px" @click="OnSearchMechine">查询</el-button>
    </el-row>
    <el-table
      :data="mechine_table.data"
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
        label = "update_time">
      </el-table-column>
    </el-table>
    <el-pagination
      @size-change="mechine_table_size_change"
      @current-change="mechine_table_cur_change"
      :current-page="mechine_table.cur_page"
      :page-size="10"
      layout="total, prev, pager, next"
      :total="mechine_table.count" 
      background
      style="justify-content:center">
    </el-pagination>
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
      mechine_table: {
        count: 0,
        data:[],
        cur_page: 1
      },
      top_owners:[],
      top_stakers:[],
      param:{
        all_mechines_count: 0,
        all_v: 0,
        all_stake_amount: 0,
        all_right_stake_amount: 0,
        all_owner_count: 0,
        all_staker_count: 0,
      },
      echarts_data: {
        v_data: {
          label_data: [],
          value_data: []
        },
        stake_data: {
          label_data: [],
          value_data1: [],
          value_data2: []
        }
      },
      mechine_condition: {
        use_pid: false,
        pid: "1",
        use_status: false,
        status: "0",
        use_pubkey: false,
        pubkey: "0x"
      }
    }
  },
  methods:{
    FlushTop10Owner: function(){
      let self = this
      axios.get("/rest/get_top10_owner").then(function(data){
        data = data.data
        self.top_owners=[]
        for (var i = 0; i < data.data.length; i++){
          self.top_owners.push({
            addr: data.data[i]['addr'],
            name: data.data[i]['name'],
            percent: (data.data[i]['percent']*100).toFixed(2)+"%",
            v: data.data[i]['v']
          })
        }
      })
    },
    FlushTop10Staker: function(){
      let self = this
      axios.get("/rest/get_top10_staker").then(function(data){
        data = data.data
        self.top_stakers=[]
        for (var i = 0; i < data.data.length; i++){
          self.top_stakers.push({
            addr: data.data[i]['addr'],
            name: data.data[i]['name'],
            percent: (data.data[i]['percent']*100).toFixed(2)+"%",
            amount: (data.data[i]['amount']/10**12).toFixed(0)
          })
        }
      })
    },
    FlushParam: function () {
      let self = this
      axios.get("/rest/get_param").then(function(data){
        data = data.data
        self.param = data.data
      })
    },
    FlushVEchart: function(){
      var chartDom = document.getElementById('v-charts');
      var myChart = echarts.init(chartDom);
      var option;
      var self = this
      axios.get("/rest/get_latest_daily_v").then(function(data){
        self.echarts_data.v_data.label_data = data.data.data.label_data
        self.echarts_data.v_data.value_data = data.data.data.value_data
        option = {
          xAxis: {
            type: 'category',
            data: self.echarts_data.v_data.label_data,
          },
          yAxis: {
            type: 'value'
          },
          tooltip: {
            trigger: 'axis'
          },
          grid: {
            left: '1%',
            right: '4%',
            top: '20px',
            bottom: '3%',
            containLabel: true
          },
          series: [
            {
              data: self.echarts_data.v_data.value_data,
              type: 'line',
              smooth: true
            }
          ]
        };
        option && myChart.setOption(option);
      })
      
    },
    FlushStakeEchart: function(){
      var chartDom = document.getElementById('stake-charts');
      var myChart = echarts.init(chartDom);
      var option;
      var self = this
      axios.get("/rest/get_latest_daily_stake").then(function(data){
        self.echarts_data.stake_data.label_data = data.data.data.label_data
        self.echarts_data.stake_data.value_data1 = data.data.data.value_data1
        self.echarts_data.stake_data.value_data2 = data.data.data.value_data2
        for (var i = 0; i < self.echarts_data.stake_data.value_data1.length; i++) {
          self.echarts_data.stake_data.value_data1[i] = self.echarts_data.stake_data.value_data1[i]/10**12/10**7
          self.echarts_data.stake_data.value_data2[i] = self.echarts_data.stake_data.value_data2[i]/10**12/10**7
        }
        option = {
          xAxis: {
            type: 'category',
            data: self.echarts_data.stake_data.label_data,
          },
          yAxis: {
            type: 'value'
          },
          tooltip: {
            trigger: 'axis',
            formatter:(params) =>{
              return params[0].name+"</br>"+ params[0].marker+   "总质押量:"+params[0].data.toFixed(2)+"kw</br>"+
                params[1].marker+   "使用的质押量:"+params[1].data.toFixed(2)+"kw</br>"
            }
          },
          grid: {
            left: '1%',
            right: '4%',
            top: '20px',
            bottom: '3%',
            containLabel: true
          },
          series: [
            {
              data: self.echarts_data.stake_data.value_data1,
              type: 'line',
              smooth: true
            },{
              data: self.echarts_data.stake_data.value_data2,
              type: 'line',
              smooth: true
            }
          ]
        };
        option && myChart.setOption(option);
      })
    },
    FlushMechineEchart: function(){
      var chartDom = document.getElementById('mechine-charts');
      var myChart = echarts.init(chartDom);
      var option;
      var self = this
      axios.get("/rest/get_latest_daily_mechine_count").then(function(data){
        self.echarts_data.v_data.label_data = data.data.data.label_data
        self.echarts_data.v_data.value_data = data.data.data.value_data
        option = {
          xAxis: {
            type: 'category',
            data: self.echarts_data.v_data.label_data,
          },
          yAxis: {
            type: 'value'
          },
          tooltip: {
            trigger: 'axis'
          },
          grid: {
            left: '1%',
            right: '4%',
            top: '20px',
            bottom: '3%',
            containLabel: true
          },
          series: [
            {
              data: self.echarts_data.v_data.value_data,
              type: 'line',
              smooth: true
            }
          ]
        };
        option && myChart.setOption(option);
      })
      
    },
    FlushMechineUserEchart: function(){
      var chartDom = document.getElementById('owner-charts');
      var myChart = echarts.init(chartDom);
      var option;
      var self = this
      axios.get("/rest/get_latest_daily_mechine_user_count").then(function(data){
        self.echarts_data.v_data.label_data = data.data.data.label_data
        self.echarts_data.v_data.value_data = data.data.data.value_data
        option = {
          xAxis: {
            type: 'category',
            data: self.echarts_data.v_data.label_data,
          },
          yAxis: {
            type: 'value'
          },
          tooltip: {
            trigger: 'axis'
          },
          grid: {
            left: '1%',
            right: '4%',
            top: '20px',
            bottom: '3%',
            containLabel: true
          },
          series: [
            {
              data: self.echarts_data.v_data.value_data,
              type: 'line',
              smooth: true
            }
          ]
        };
        option && myChart.setOption(option);
      })
    },
    mechine_table_size_change: function(val) {
      console.log("mechine_table_size_change", val)
    },
    mechine_table_cur_change: function(val) {
      this.mechine_table.cur_page = val
      this.OnSearchMechine()
    },
    OnSearchMechine: function() {
      var url = "/rest/get_mechines/"
      url += (this.mechine_condition.use_pid == true)?this.mechine_condition.pid:"-"
      url += "/"
      url += (this.mechine_condition.use_status == true)?this.mechine_condition.status:"-"
      url += "/"
      url += (this.mechine_condition.use_pubkey == true)?this.mechine_condition.pubkey:"-"
      url += "/"
      url += this.mechine_table.cur_page
      var self = this
      axios.get(url).then(function(data){
        data = data.data
        for (var i = 0; i < data.data.length; i++) {
          data.data[i].stake_amount = data.data[i].stake_amount/10**12
          data.data[i].start_time = new Date(data.data[i].start_time*1000).toLocaleString().replace(/:\d{1,2}$/, ' ')
          data.data[i].update_time = new Date(data.data[i].update_time*1000).toLocaleString().replace(/:\d{1,2}$/, ' ')
        }
        self.mechine_table.data = data.data
        self.mechine_table.count = data.count
      })
      console.log(url) 
    }
  },
  
  mounted:function(){
    console.log("?????")
    this.FlushTop10Owner()
    this.FlushTop10Staker()
    this.FlushParam()
    this.FlushVEchart()
    this.FlushStakeEchart()
    this.FlushMechineEchart()
    this.FlushMechineUserEchart()
  }
}
// path('/rest/get_latest_daily_mechine_count', views.get_latest_daily_mechine_count),
// path('/rest/get_latest_daily_mechine_user_count', views.get_latest_daily_mechine_user_count)
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
