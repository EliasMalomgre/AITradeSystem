<template>
  <div>
    <v-card>
      <apexchart
        v-if="stockData.lenght !== 0"
        ref="chart"
        type="candlestick"
        height="850"
        :options="chartOptions"
        :series="stockData"
      ></apexchart>
      <div v-else>
        <lottie-player
          src="https://assets7.lottiefiles.com/temp/lf20_V5NlNu.json"
          background="transparent"
          speed="1"
          style="width: 500px; height: 500px"
          loop
          autoplay
        ></lottie-player>
      </div>
      <v-alert v-if="showWarning" type="warning">
        Looks like there's some data missing in the database, press request to
        update. <br />
        Ignore this if you picked a begin- or end-date in a weekend or holiday.
      </v-alert>
      <v-form>
        <v-container>
          <v-row justify="left" style="padding-left:5em">
            <v-col cols="1" align-self="center">
              <h4>Edit Y-axis scale:</h4>
            </v-col>
            <v-col cols="2">
              <v-text-field v-model="min" label="minimum"></v-text-field>
            </v-col>
            <v-col cols="2">
              <v-text-field v-model="max" label="maximum"></v-text-field>
            </v-col>
            <v-col cols="1" align-self="center">
              <v-btn @click="refreshAxisOptions" color="#5894e2">Apply</v-btn>
            </v-col>
            <v-col cols="1" align-self="center">
              <v-btn @click="resetAxisOptions">Reset</v-btn>
            </v-col>
          </v-row>
          <v-row justify="left" style="padding-left:5em">
            <v-col cols="1" align-self="center">
              <h4>Edit X-axis scale:</h4>
            </v-col>
            <v-col cols="2">
              <v-btn color="#187fe0" @click="addUnits(-10)">Add -10 units</v-btn>
            </v-col>
            <v-col cols="2">
              <v-btn color="#187fe0" @click="addUnits(-5)">Add -5 units</v-btn>
            </v-col>
            <v-col cols="2">
              <v-btn color="#187fe0" @click="addUnits(5)">Add 5 units</v-btn>
            </v-col>
            <v-col cols="2">
              <v-btn color="#187fe0" @click="addUnits(10)">Add 10 units</v-btn>
            </v-col>
          </v-row>
        </v-container>
      </v-form>
    </v-card>
  </div>
</template>

<script>
export default {
  name: "CandleStickDotted",

  props: {
    stockData: {
      type: Array,
      required: true,
    },
    stopLoss: {
      type: Array,
      required: false,
    },
    annotations: {
      type: Array,
      required: false,
    },
    showWarning: {
      type: Boolean,
      required: false,
    },
  },

  data: () => ({
    min: undefined,
    max: undefined,

    series: [],
    dateTimeFormat: "DD MMM",

    chartOptions: {
      chart: {
        type: "candlestick",
        height: 700,
      },
      title: {
        text: "Stock data",
        align: "left",
      },
      annotations: {
        points: [],
        xaxis: [],
      },
      xaxis: {
        type: "category",
        labels: {
          formatter: function (val) {
            return val;
          },
        },
      },
      yaxis: {
        tooltip: {
          enabled: true,
        },
        forceNiceScale: false,
        decimalsInFloat: 2,
        formatter: function (val) {
          return val.toFixed(2);
        },
      },
    },

    chartOptionsDefault: {
      chart: {
        type: "candlestick",
        height: 700,
      },
      title: {
        text: "Stock data",
        align: "left",
      },
      annotations: {
        points: [],
        xaxis: [],
      },
      xaxis: {
        type: "category",
        labels: {
          formatter: function (val) {
            return val;
          },
        },
      },
      yaxis: {
        tooltip: {
          enabled: true,
        },
        forceNiceScale: false,
        decimalsInFloat: 2,
        formatter: function (val) {
          return val.toFixed(2);
        },
      },
    }
  }),

  methods: {
    addUnits(amount){
      this.$emit('addTimeUnits',amount)
    },
    resetAxisOptions(){
        var newOptions = this.chartOptions;
        newOptions.yaxis[0].min = undefined
        newOptions.yaxis[0].max = undefined
        this.$refs.chart.updateOptions(newOptions);
    },
    refreshAxisOptions() {
      if (this.max !== undefined && this.min !== undefined) {
        console.log('updating: min = '+this.min+' max = '+this.max)
        var newOptions = this.chartOptions;
        newOptions.yaxis[0].min = parseInt(this.min);
        newOptions.yaxis[0].max = parseInt(this.max);
        this.$refs.chart.updateOptions(newOptions);
      }
    },

    async refreshPointsAnnotations(annotations) {
      var newOptions = this.chartOptions;
      newOptions.annotations.points = annotations;
      this.$refs.chart.updateOptions(newOptions);
    },
    async refreshXaxisAnnotations() {
      var newOptions = this.chartOptions;
      newOptions.annotations.xaxis = this.annotations;
      this.$refs.chart.updateOptions(newOptions);
    },

    getFormattedTimeStamp(transaction) {
      if (
        transaction.frequency === "Frequency.ONE_DAY" ||
        transaction.frequency === "1d"
      ) {
        return "DD MMM";
      }
      if (
        transaction.frequency === "1h" ||
        transaction.frequency === "Frequency.ONE_HOUR"
      ) {
        return "DD MMM HH";
      }
      if (
        transaction.frequency === "1m" ||
        transaction.frequency === "Frequency.ONE_MINUTE"
      ) {
        return "DD MMM HH:mm";
      }
      if (
        transaction.frequency === "5d" ||
        transaction.frequency === "1M" ||
        transaction.frequency === "Frequency.ONE_WEEK" ||
        transaction.frequency === "Frequency.ONE_MONTH"
      ) {
        return "DD MMM YYYY";
      }
    },

    getBorderColor(transaction) {
      if (transaction.action === "TransactionAction.BUY") {
        return "#4caf50";
      }
      if (transaction.action === "TransactionAction.SELL") {
        return "#f32f2f";
      }
      if (transaction.action === "TransactionAction.SHORT") {
        return "#1976d2";
      }
      if (transaction.action === "TransactionAction.COVER") {
        return "#f9a825";
      }
    },

    getBackgroundColor(transaction) {
      if (transaction.action === "TransactionAction.BUY") {
        return "#80e27e";
      }
      if (transaction.action === "TransactionAction.SELL") {
        return "#ff7961";
      }
      if (transaction.action === "TransactionAction.SHORT") {
        return "#63a4ff";
      }
      if (transaction.action === "TransactionAction.COVER") {
        return "#ffd95a";
      }
    },
  },

  created() {},

  watch: {
    stopLoss: function (newVal) {
      var points = [];
      for (var point of newVal) {
        var annotation = {
          x: point.x,
          y: point.y,
          marker: { size: 3, fillColor: "#2196F3", strokeColor: "#2196F3" },
          //label: { getBorderColor: "#FF4560", text: point.y.toString(),
          //offsetX: 25, offsetY: 17},
        };
        points.push(annotation);
      }
      this.refreshPointsAnnotations(points);
    },
    annotations: function (newVal, oldVal) {
      if (newVal.length > 0) {
        this.dateTimeFormat = this.getFormattedTimeStamp(newVal[0]);
      }
      console.log(
        "Xaxis annotations changed! " + newVal.length + oldVal.length
      );
      this.refreshXaxisAnnotations();
    },
  },
};
</script>