<template>
  <v-app>
    <navDrawer :drawer="drawer" @setView="setView" />
    <v-app-bar app color="blue" dark height="40em">
      <v-app-bar-nav-icon @click.stop="toggleDrawer()" />
      <v-btn icon @click="darkmode()" class="ml-auto"
        ><v-icon>mdi-theme-light-dark</v-icon></v-btn
      >
    </v-app-bar>

    <v-main>
      <v-row style="height: 25px"></v-row>
      <v-row justify="center" v-if="view!=='ai'">
        <v-col
          :cols="getCols().small"
          align-self="center"
          style="padding-left: 2em"
        >
          <shareHistory
            v-if="view == 'hist'"
            :stockInfo="infoData"
            @setStock="setStock"
            @historyCols="setHistCols"
            @pullStock="pullStock"
            @updateStock="updateStock"
            @updateName="updateNameForInfo"
          />
          <positions
            v-if="view == 'pos'"
            @setPositionForChart="loadPositionForChart"
            @positionCols="setCols"
          />
        </v-col>
        <v-col :cols="getCols().big">
          <dottedChart
            :stockData="stockData"
            :stopLoss="positionStopLoss"
            :annotations="positionAnnotations"
            :showWarning="showWarning"
            @addTimeUnits="addTimeUnits"
          />
        </v-col>
      </v-row>
      <v-row v-if="view=='ai'">
       <aiCommunicationVue 
       />
      </v-row>
    </v-main>
  </v-app>
</template>

<script>
import ShareHistory from "./views/ShareHistory";
import Positions from "./views/Positions";
import shareHistory from "./repo/shareHistory";
import WalletRepo from "./repo/walletRepo";
import NavDrawer from "./components/NavDrawer";
import stockPuller from "./repo/stockPuller";
import AICommunicationVue from './views/AICommunication.vue'

import CandleStickDotted from "./components/CandleStickDotted";

var dayjs = require("dayjs");
const moment = require("moment");
export default {
  name: "App",

  data: () => ({
    drawer: true,
    view: "hist",
    showPositionTab: true,
    showHistTab: true,

    positionView: false,
    shareHistory: null,
    stockData: [],
    positionTransactions: [],
    positionAnnotations: [],
    positionStopLoss: [],
    dateTimeFormat: "DD MMM",
    infoData: {},

    stockName: "AAPL",
    frequency: "1d",
    beginDate: "2020-09-01",
    endDate: "2021-02-01",
    showWarning: false,
  }),
  methods: {
    addTimeUnits(amount) {
      if (amount < 0) {
        var copy = new Date(this.beginDate);
        var copyResult;
        if (this.frequency === "1m") {
          copyResult = moment(copy)
            .subtract(Math.abs(amount), "minutes")
            .toDate();
        } else if (this.frequency === "1d") {
          copyResult = moment(copy).subtract(Math.abs(amount), "days").toDate();
        }
        else if (this.frequency === "1h") {
          copyResult = moment(copy).subtract(Math.abs(amount), "hours").toDate();
        }
        else if (this.frequency === "1w") {
          copyResult = moment(copy).subtract(Math.abs(amount), "weeks").toDate();
        }
        else if (this.frequency === "1M") {
          copyResult = moment(copy).subtract(Math.abs(amount), "months").toDate();
        }

        this.beginDate = dayjs(copyResult).format("YYYY-MM-DD");
      } else {
        var copy2 = new Date(this.endDate);
        var copyResult2;
        if (this.frequency === "1m") {
          copyResult2 = moment(copy2).add(Math.abs(amount), "minutes").toDate();
        } else if (this.frequency === "1d") {
          copyResult2 = moment(copy2).add(Math.abs(amount), "days").toDate();
        }
        else if (this.frequency === "1h") {
          copyResult = moment(copy).add(Math.abs(amount), "hours").toDate();
        }
        else if (this.frequency === "1w") {
          copyResult = moment(copy).add(Math.abs(amount), "weeks").toDate();
        }
        else if (this.frequency === "1M") {
          copyResult = moment(copy).add(Math.abs(amount), "months").toDate();
        }

        this.endDate = dayjs(copyResult2).format("YYYY-MM-DD");
      }

      this.loadChartDataDated();
    },

    async testMethode(positionId) {
      var data = await WalletRepo.getPosition(positionId);
      this.loadPositionForChart(data);
    },

    getCols() {
      if (
        (this.showPositionTab && this.view === "pos") ||
        (this.showHistTab && this.view === "hist")
      ) {
        return { big: 9, small: 3 };
      } else {
        return { big: 11, small: 1 };
      }
    },

    setCols(value) {
      this.showPositionTab = value;
    },

    setHistCols(value) {
      this.showHistTab = value;
    },

    toggleDrawer() {
      this.drawer = !this.drawer;
    },

    darkmode() {
      this.$vuetify.theme.dark = !this.$vuetify.theme.dark;
    },

    async loadPositionForChart(position) {
      var result = [];
      await WalletRepo.getTransactions(position._id).then((data) => {
        result = data;
      });
      this.positionTransactions = result;

      var result2 = [];
      await WalletRepo.getAnnotations(position._id).then((data) => {
        result2 = data;
      });
      this.positionAnnotations = result2;

      var dates = null;
      await WalletRepo.getBeginEnd(position._id).then((data) => {
        dates = data;
      });

      var stopLoss = null;
      await WalletRepo.getStopLoss(position._id).then((data) => {
        stopLoss = data;
      });
      this.positionStopLoss = stopLoss;

      function compareTransactions(a, b) {
        if (a.time_stamp > b.time_stamp) return 1;
        if (a.time_stamp < b.time_stamp) return -1;
        return 0;
      }

      result.sort(compareTransactions);
      this.beginDate = dates.beginDate;
      this.endDate = dates.endDate;
      this.stockName = position.stock_name;
      this.frequency = position.frequency;
      this.loadChartDataDated();
    },

    getFormattedTimeStamp() {
      if (this.frequency === "1d" || this.frequency === "Frequency.ONE_DAY") {
        return "DD MMM";
      }
      if (this.frequency === "1h" || this.frequency === "Frequency.ONE_HOUR") {
        return "DD MMM HH";
      }
      if (
        this.frequency === "1m" ||
        this.frequency === "Frequency.ONE_MINUTE"
      ) {
        return "DD MMM HH:mm";
      }
      if (
        this.frequency === "1w" ||
        this.frequency === "1m" ||
        this.frequency === "Frequency.ONE_WEEK" ||
        this.frequency === "Frequency.ONE_MONTH"
      ) {
        return "DD MMM YYYY";
      }
    },

    loadChartDataDated() {
      this.dateTimeFormat = this.getFormattedTimeStamp();
      shareHistory
        .getStockDataDated(
          this.stockName,
          this.frequency,
          this.beginDate,
          this.endDate
        )
        .then((data) => {
          this.stockData = [];
          this.showWarning = this.checkIfMissingData(
            data[0],
            data[data.length - 1]
          );

          for (var dat of data) {
            dat.x = dayjs(dat.x).format(this.dateTimeFormat);
          }
          this.stockData.push({ data: data });
        })
        .catch((error) => {
          this.handleError("Loading stock data failed", error);
        });
    },

    checkIfMissingData(first, last) {
      if (this.view !== "hist") {
        return false;
      }
      if (
        first === null ||
        first === undefined ||
        last === null ||
        last === undefined
      ) {
        return true;
      }
      if (
        dayjs(first.x).format(this.getFormattedTimeStamp()) !==
        dayjs(this.beginDate).format(this.getFormattedTimeStamp())
      ) {
        return true;
      } else if (
        dayjs(last.x).format(this.getFormattedTimeStamp()) !==
        dayjs(this.endDate).format(this.getFormattedTimeStamp())
      ) {
        return true;
      } else {
        return false;
      }
    },

    updateNameForInfo(name) {
      this.stockName = name;
      this.getInfo();
    },

    setStock(name, freq, beginDate, endDate) {
      this.stockName = name;
      this.frequency = freq;
      this.beginDate = beginDate;
      this.endDate = endDate;
      this.loadChartDataDated();
      this.getInfo();
    },

    async pullStock(name, freq, beginDate, endDate) {
      await stockPuller.pullShares(
        name,
        freq,
        new Date(beginDate),
        new Date(endDate)
      );
      this.setStock(name, freq, beginDate, endDate);
    },

    async updateStock(name, freq, beginDate, endDate) {
      await stockPuller.updateShares(name, freq);
      this.setStock(name, freq, beginDate, endDate);
    },

    async getInfo() {
      var info = await stockPuller.getShareInfo(this.stockName);
      this.infoData = info;
    },

    togglePositionView() {
      this.positionView = !this.positionView;
    },

    setView(view) {
      this.view = view;
      this.showHistTab = true;
      this.showPositionTab = true;
    },

    handleError(error) {
      console.log(error);
    },
  },

  created() {
    this.loadChartDataDated();
    this.getInfo();
  },

  components: {
    shareHistory: ShareHistory,
    positions: Positions,
    navDrawer: NavDrawer,
    aiCommunicationVue: AICommunicationVue,

    dottedChart: CandleStickDotted,
  },
};
</script>
