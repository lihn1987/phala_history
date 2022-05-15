const error_unknow = -1
const error_unknow_url = -2


import { 
    decodeAddress, 
    signatureVerify
  } from '@polkadot/util-crypto';
import { u8aToHex } from '@polkadot/util';
import { ApiPromise, WsProvider } from '@polkadot/api';
import {khala, khalaDev} from '@phala/typedefs';
var api = null
var wsProvider = new WsProvider('wss://khala.api.onfinality.io/public-ws'); // 这个是rpc地址，需要根据实际修改
//var wsProvider = new WsProvider('ws://35.220.221.140:9944'); // 这个是rpc地址，需要根据实际修改
  ApiPromise.create({ provider: wsProvider ,
  types:khalaDev
}).then((api_tmp) => {
    console.log("api created")
    api = api_tmp
})
function verify(msg){
    const msg_addr = msg.address
    const msg_timestamp = parseInt(msg.timestamp)
    const msg_sign = msg.sign;
    const publicKey = decodeAddress(msg_addr);
    const hexPublicKey = u8aToHex(publicKey);
    return signatureVerify(JSON.stringify({address:msg_addr, timestamp:msg_timestamp}), msg_sign, hexPublicKey).isValid
}

function handle_post(url, param, cb){
}
function handle_get(path, param, cb){
    if(path == "/api/get_pool"){
        var pid = param.pid
        api.query.phalaStakePool.stakePools(pid).then((data)=>{
            cb(data.toString())
        })
    }if(path == "/api/get_pool_count"){
        api.query.phalaStakePool.poolCount().then((data)=>{
            cb(data.toString())
        })
    }else if(path == "/api/get_miner"){
      var pubkey = param.pubkey
      api.query.phalaMining.workerBindings(pubkey).then((data)=>{
          api.query.phalaMining.miners(data.toString()).then((v)=>{
              cb(v.toString())
          })
      })
    }else if(path == "/api/get_miner_detail"){
        var pubkey = param.pubkey
        api.query.phalaMining.workerBindings(pubkey).then((data)=>{
            api.query.phalaMining.miners(data.toString()).then((v)=>{
                cb(v.toString())
            })
        })
    }else if(path == "/api/get_stake_list"){
        console.log("here")
        api.query.phalaStakePool.poolStakers.keys().then((data)=>{
            var user_list = []
            console.log(data.length)
            data.map(({ args: [key] }) => {
                user_list.push({
                    pid: key[0].toString(),
                    user: key[1].toString()
                })   
            })
            console.log(user_list.length)
            cb(JSON.stringify(user_list))
        })
    } else if(path == "/api/get_stake_detail"){
        var pid = param.pid
        var addr = param.addr
        api.query.phalaStakePool.poolStakers([pid, addr]).then((data)=>{
            cb(data.toString())
        })
    } else if(path == "/api/get_mechine_stake"){
        var pubkey = param.pubkey
        api.query.phalaMining.workerBindings(pubkey).then((data)=>{
            api.query.phalaMining.stakes(data.toString()).then((v)=>{
                cb(v.toString())
            })
        })
    }
    //cb("1122");
}


export {handle_post, handle_get};