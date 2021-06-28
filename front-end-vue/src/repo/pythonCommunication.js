import axios from 'axios'
const RESOURCE_PATH = 'http://localhost:4080/'

export default{
    //start training with default settings
    startTraining(){
        return axios.get(RESOURCE_PATH+"startTraining")
        .then(result => result.data)
    },
    startTrainingAdv(stockName, startDate, endDate, freq, episodes, modelName){
        return axios.get(RESOURCE_PATH+"startTrainingAdv?stock_name="+stockName+"&start_date="+startDate.toISOString()
        +"&end_date="+endDate.toISOString()+"&frequency="+freq+"&episodes="+episodes+"&model_name="+modelName
        ).then(result => result.data)
    },
    getGraph(){
        return axios.get(RESOURCE_PATH+"sendGraph")
        .then(result=>result.data)
    }
}