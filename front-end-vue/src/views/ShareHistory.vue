<template>
  <v-card>
    <v-container>
      <v-col :cols="1">
        <v-row>
          <v-col v-if="!histDrawerVisible" align-self="center">
            <v-btn icon color="blue" @click="toggleHistDrawerVisible">
              <v-icon x-large>mdi-chevron-right</v-icon>
            </v-btn>
          </v-col>
          <v-col v-if="histDrawerVisible">
            <v-btn icon color="red" @click="toggleHistDrawerVisible">
              <v-icon x-large>mdi-chevron-left</v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
      <v-col :cols="11" v-if="histDrawerVisible">
        <v-row justify="center"><h2>Begin</h2></v-row>
        <v-row justify="center">
          <v-date-picker v-model="beginDate"></v-date-picker>
        </v-row>
        <v-row justify="center"><h2>End</h2></v-row>
        <v-row justify="center">
          <v-date-picker v-model="endDate"></v-date-picker>
        </v-row>
        <v-row justify="center">
          <h2>Name and frequency</h2>
        </v-row>
        <v-row justify="center">
          <v-text-field @change="emitName"
            label="Stock name"
            v-model="stockName"
            style="padding-left: 2em"
          ></v-text-field>
        </v-row>
        <v-row justify="center" style="padding-left: 2em">
          <v-select
            :items="frequencies"
            label="Frequency"
            v-model="frequency"
          ></v-select>
        </v-row>
        <v-row justify="center">
          <v-col :cols="6">
            <v-btn @click="emitData()" color="#187FE0" style="color:white;">Show</v-btn>
          </v-col>
          <v-col :cols="4">
            <stockInfoOverlay :infoData="stockInfo" />
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col :cols="6">
            <v-btn @click="emitUpdate()" color="#187fe0">Quick update</v-btn>
          </v-col>
          <v-col :cols="4">
            <v-btn @click="emitPull()" color="#187fe0">Request</v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-container>
  </v-card>
</template>

<script>
import StockInfoOverlay from "../components/StockInfoOverlay";
var dayjs = require("dayjs");

export default {
  name: "ShareHistory",

  props: {
    stockInfo: {
      type: Object,
      required: false,
    },
  },

  data: () => ({
    histDrawerVisible: true,
    infoOverlayVisible: false,

    stockName: "AAPL",
    frequency: "1d",
    beginDate: "2020-09-01",
    endDate: dayjs(new Date()).format("YYYY-MM-DD"),
    frequencies: ["1m", "1h", "1d", "5d", "1M"],
  }),
  methods: {
    toggleHistDrawerVisible() {
      this.histDrawerVisible = !this.histDrawerVisible;
      this.emitHistoryCols();
    },

    emitHistoryCols() {
      if (this.histDrawerVisible) {
        return this.$emit("historyCols", true);
      } else {
        return this.$emit("historyCols", false);
      }
    },

    emitData() {
      this.$emit(
        "setStock",
        this.stockName,
        this.frequency,
        this.beginDate,
        this.endDate
      );
    },
    emitPull() {
      this.$emit(
        "pullStock",
        this.stockName,
        this.frequency,
        this.beginDate,
        this.endDate
      );
    },
    emitUpdate() {
      this.$emit(
        "updateStock",
        this.stockName,
        this.frequency,
        this.beginDate,
        this.endDate
      );
    },
    emitName(){
      this.$emit(
        "updateName",
        this.stockName
      );
    },
  },

  created() {},

  components: {
    stockInfoOverlay: StockInfoOverlay,
  },
};
</script>
