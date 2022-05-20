<template>
  <div class="hello">
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
                width=180>
              </el-table-column>
              <el-table-column
                prop="addr"
                label="地址">
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
                width=180>
              </el-table-column>
              <el-table-column
                prop="addr"
                label="地址">
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
    
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data: function(){
    return {
      top_owners:[],
      top_stakers:[],
      param:{
        all_mechines_count: 0,
        all_v: 0,
        all_stake_amount: 0,
        all_right_stake_amount: 0,
        all_owner_count: 0,
        all_staker_count: 0,
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
    }
  },
  mounted:function(){
    console.log("?????")
    this.FlushTop10Owner()
    this.FlushTop10Staker()
    this.FlushParam()
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
