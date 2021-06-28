<template>
  <div>
    <apexchart
      ref="chart"
      type="candlestick"
      height="500"
      :options="chartOptions"
      :series="stockData"
    ></apexchart>
  </div>
</template>

<script>
export default {
  name: "CandleStick",
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
  },

  data: () => ({
    series: [],
    chartOptions: {
      chart: {
        type: "candlestick",
        height: 500,
      },
      title: {
        text: "Stock data",
        align: "left",
      },
      annotations: {
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
      },
    },
  }),

  methods: {
    async refreshAnnotations() {
      var newOptions = this.chartOptions;
      newOptions.annotations.xaxis = this.annotations;
      this.$refs.chart.updateOptions(newOptions);
    },

    refreshData() {
      var newSeries = [
        { name: "Stock data", type: "candlestick", data: [] },
      ];
      newSeries[0].data = this.stockData[0].data;
      this.series = newSeries;
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

    getFormattedTimeStamp(transaction) {
      if (transaction.frequency === "1d" || transaction.frequency === "Frequency.ONE_DAY") {
        return "DD MMM";
      }
      if (transaction.frequency === "1h" || transaction.frequency === "Frequency.ONE_HOUR") {
        return "DD MMM HH";
      }
      if (transaction.frequency === "1m" || transaction.frequency === "Frequency.ONE_MINUTE") {
        return "DD MMM HH:mm";
      }
      if (transaction.frequency === "1w" || transaction.frequency === "1m" || transaction.frequency === "Frequency.ONE_WEEK" || transaction.frequency === "Frequency.ONE_MONTH") {
        return "DD MMM YYYY";
      }
    },
  },

  created() {},

  watch: {
    annotations: function (newVal, oldVal) {
      if (newVal.length > 0) {
        this.dateTimeFormat = this.getFormattedTimeStamp(newVal[0]);
      }
      console.log("Transactions changed! " + newVal.length + oldVal.length);
      this.refreshAnnotations();
    },
    stopLoss: function () {
      this.refreshData()
    },
  },
};
</script>