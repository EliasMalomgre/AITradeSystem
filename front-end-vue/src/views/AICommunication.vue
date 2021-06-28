<template>
  <v-card style="padding-left: 25px" width="100%">
    <v-container>
      <v-row>
        <v-col :cols="5">
          <v-row justify="center">
            <h1>AI communication</h1>
          </v-row>
          <v-row>
            <v-col :cols="5">
              <v-row justify="center"><h2>Begin</h2></v-row>
              <v-row justify="center">
                <v-date-picker
                  v-model="startDate"
                  first-day-of-week="1"
                ></v-date-picker>
              </v-row>
            </v-col>
            <v-col :cols="1"></v-col>
            <v-col :cols="5">
              <v-row justify="center"><h2>End</h2></v-row>
              <v-row justify="center">
                <v-date-picker
                  v-model="endDate"
                  first-day-of-week="1"
                ></v-date-picker>
              </v-row>
            </v-col>
          </v-row>
          <v-row justify="center">
            <h2>Name and frequency</h2>
          </v-row>
          <v-row justify="center">
            <v-text-field
              label="Stock name"
              v-model="stockName"
              style="padding-left: 2em"
            ></v-text-field>
          </v-row>
          <v-row justify="center" style="padding-left: 2em">
            <v-select
              :items="frequencies"
              label="Frequency"
              v-model="freq"
            ></v-select>
          </v-row>

          <v-row justify="center">
            <h2>Amount of episodes</h2>
          </v-row>
          <v-row justify="center">
            <v-text-field
              label="episodes"
              v-model="episodes"
              style="padding-left: 2em"
            ></v-text-field>
          </v-row>
          <v-row justify="center">
            <h2>Agent name</h2>
          </v-row>
          <v-row justify="center" style="padding-left: 2em">
            <v-text-field label="name" v-model="moduleName"></v-text-field>
          </v-row>
          <v-row justify="center" style="padding-bottom: 25px">
            <v-btn color="#187fe0" @click="sendStart()"
              >Start standard training</v-btn
            >
            <v-btn
              style="margin-left: 50px"
              color="#63a4ff"
              @click="sendStartAdv()"
              >Start custom training</v-btn
            >
          </v-row>
        </v-col>
        <v-col :cols="6" align-self="center" style="padding-left: 25px">
          <v-lazy-image
            id="graph"
            :src="imageSrc"
            src-placeholder="https://media3.giphy.com/media/3oEjI6SIIHBdRxXI40/giphy.gif"
            height="400"
            width="540"
          ></v-lazy-image>
        </v-col>
      </v-row>
    </v-container>
  </v-card>
</template>

<script>
import pythonCom from "../repo/pythonCommunication";
import VLazyImage from "v-lazy-image";
const dayjs = require("dayjs");
export default {
  name: "AICommunication",
  props: {},
  data: () => ({
    stockName: "AAPL",
    startDate: "2021-01-01",
    endDate: dayjs(new Date()).format("YYYY-MM-DD"),
    freq: "1d",
    episodes: 5000,
    moduleName: "stock_trainer",
    frequencies: ["1m", "1h", "1d", "5d", "1M"],
    polling: null,
    imageSrc: "http://localhost:4080/sendGraph?" + performance.now(),
  }),
  methods: {
    sendStart() {
      pythonCom.startTraining();
    },
    sendStartAdv() {
      var start = new Date(this.startDate);
      var end = new Date(this.endDate);
      pythonCom.startTrainingAdv(
        this.stockName,
        start,
        end,
        this.freq,
        this.episodes,
        this.moduleName
      );
    },
    getGraph() {
      this.imageSrc =  "http://localhost:4080/sendGraph?" + performance.now();
    },
    refreshGraph() {
      this.polling = setInterval(() => {
        this.getGraph()
        console.log('Refreshed!')
      }, 15000);
    },
  },
  created() {
    this.refreshGraph();
  },
  beforeDestroy(){
    this.polling = null;
  },
  components: {
    VLazyImage,
  },
};
</script>