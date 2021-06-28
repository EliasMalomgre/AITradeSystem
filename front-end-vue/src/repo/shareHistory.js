import axios from 'axios'

const RESOURCE_PATH = 'http://localhost:3000/'

export default{
   getStockData(stockName, frequency){
        return axios.get(RESOURCE_PATH+"getHistory?name="+stockName+"&freq="+frequency)
        .then(result=>result.data)
    },
    getStockDataDated(stockName, frequency, beginDate, endDate){
        return axios.get(RESOURCE_PATH+"getHistoryDated?name="+stockName+"&freq="+frequency+"&beginDate="+beginDate+"&endDate="+endDate)
        .then(result=>result.data)
    }
}