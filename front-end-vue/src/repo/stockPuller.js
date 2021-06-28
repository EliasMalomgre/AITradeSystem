import axios from 'axios'

const RESOURCE_PATH = 'http://localhost:4080/'

export default{
    updateShares(stockName, frequency){
        return axios.get(RESOURCE_PATH+"updateShares?stock_name="+stockName+"&frequency="+frequency)
        .then(result=>result.data)
    },
    pullShares(stockName, frequency, beginDate, endDate){
        return axios.get(RESOURCE_PATH+"pullShares?stock_name="+stockName+"&frequency="+frequency+"&begin_date="+beginDate.toISOString()+"&end_date="+endDate.toISOString())
        .then(result=>result.data)
    },
    getShareInfo(stockName){
        return axios.get(RESOURCE_PATH+"getShareInfo?stock_name="+stockName)
        .then(result=>result.data)
    }
}