<template>
  <apexchart
    ref="chart"
    type="candlestick"
    height="500"
    :options="chartOptions"
    :series="stockData"
  ></apexchart>
</template>

<script>
export default {
  name: "ComboChart",

  props: {
    stockData: {
      type: Array,
      required: true,
    },
    stopLoss: {
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

  created() {
    this.series[0] = {
      name: "Stock data",
      type: "candlestick",
      data: this.stockData[0].data,
    };
    if (this.stopLoss !== undefined){
        this.series[1] = {
        name: "Stop loss",
        type: "line",
        data: this.stopLoss,
      };
    } else {
        this.series[1] = {}
    }
  },

  watch: {
    stockData: function (newVal) {
      this.series[0] = {
        name: "Stock data",
        type: "candlestick",
        data: newVal[0].data,
      };
    },
    stopLoss: function (newVal) {
      this.series[1] = {
        name: "Stop loss",
        type: "line",
        data: newVal,
      };
    },
  },
};
</script>