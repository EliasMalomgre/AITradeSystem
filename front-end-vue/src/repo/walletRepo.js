import axios from 'axios'

const RESOURCE_PATH = 'http://localhost:3000/'

export default{
   getWallet(){
        return axios.get(RESOURCE_PATH+"getWallet")
        .then(result=>result.data)
    },
    getPositions(){
        return axios.get(RESOURCE_PATH+"getPositions")
        .then(result=>result.data)
    },
    getPosition(positionId){
        return axios.get(RESOURCE_PATH+"getPosition?positionId="+positionId)
        .then(result=>result.data)
    },
    getTransactions(positionId){
        return axios.get(RESOURCE_PATH+"getTransactions?positionId="+positionId)
        .then(result=>result.data)
    },
    getAnnotations(positionId){
        return axios.get(RESOURCE_PATH+"getAnnotations?positionId="+positionId)
        .then(result => result.data)
    },
    getBeginEnd(positionId){
        return axios.get(RESOURCE_PATH+"getBeginEnd?positionId="+positionId)
        .then(result=> result.data)
    },
    getStopLoss(positionId){
        return axios.get(RESOURCE_PATH+"getStopLoss?positionId="+positionId)
        .then(result=>result.data)
    },
    getPositionStats(positionId){
        return axios.get(RESOURCE_PATH+"getPositionStats?positionId"+positionId)
        .then(result=>result.data)
    }
}