const error_unknow = -1
const error_unknow_url = -2



import { ApiPromise, WsProvider } from '@polkadot/api';

import {khala, khalaDev} from '@phala/typedefs';
var api = null
var wsProvider = new WsProvider('wss://khala-api.phala.network/ws'); // 这个是rpc地址，需要根据实际修改
// var wsProvider = new WsProvider('ws://35.220.221.140:9944');
try{
  ApiPromise.create({ provider: wsProvider ,
  types: khalaDev
  }).then((api_tmp) => {
    console.log("=====================")
    console.log("api created")
    api = api_tmp
    var pubkeys = [
      1,2,3,4
    ]
    console.log("muti")
    api.query.phalaStakePool.stakePools.multi(pubkeys, (data)=>{
      console.log("data")
      console.log(data.length)
      for (var i = 0; i < data.length; i++){
        console.log(data[i].toHuman())
        console.log(data[i].toString())
      }
    })
    // api.query.phalaStakePool.poolStakers.keys().then((data)=>{
    //     var user_list = []
    //     console.log(data.length)
    //     data.map(({ args: [key] }) => {
    //         user_list.push({
    //             pid: key[0].toString(),
    //             user: key[1].toString()
    //         })   
    //     })
    //     console.log(user_list.length)
    // })
    
  }).catch((e)=>{
    console.log("=====================")
    console.log("api faild", e)
  })
  console.log("???????????????")
} catch(error) {
  console.log("!!!!!!!!!!!!!! error", error)
}