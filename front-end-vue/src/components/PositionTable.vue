<template>
  <v-card>
    <v-simple-table fixed-header height="24em">
      <template v-slot:default>
        <thead>
          <tr>
            <th>
              <h3>{{ position.stock_name }}</h3>
            </th>
            <th colspan="1">
              <v-btn @click="toggleView()" v-if="transactionView == false">
                Transactions
              </v-btn>
              <v-btn @click="toggleView()" v-if="transactionView == true">
                Overview
              </v-btn>
            </th>
            <th colspan="2">
              <v-btn icon color="red" @click="emitClose">
                <v-icon x-large>mdi-close</v-icon>
              </v-btn>
            </th>
          </tr>
        </thead>
        <tbody v-if="!transactionView">
          <tr>
            <td>Average buy price</td>
            <td colspan="2">
              {{ position.average_buy_price }}
            </td>
          </tr>
          <tr>
            <td>Current amount</td>
            <td colspan="2">
              {{ position.current_amount }}
            </td>
          </tr>
          <tr>
            <td>Current share price</td>
            <td colspan="2">
              {{ position.current_share_price }}
            </td>
          </tr>
          <tr>
            <td>Frequency</td>
            <td colspan="2">
              {{ frequencyString(position.frequency) }}
            </td>
          </tr>
          <tr>
            <td>Profit and loss</td>
            <td colspan="2">
              {{ position.p_and_l }}
            </td>
          </tr>
          <tr>
            <td>Risk</td>
            <td colspan="2">
              {{ position.risk }}
            </td>
          </tr>
          <tr>
            <td>Total buy price</td>
            <td colspan="2">
              {{ position.total_buy_price }}
            </td>
          </tr>
        </tbody>
        <tbody v-if="transactionView">
          <tr>
            <th>Action</th>
            <th>Amount</th>
            <th>Price per share</th>
            <th>Timestamp</th>
          </tr>
          <tr v-for="transaction in transactions" :key="transaction._id">
            <td>
              {{ transaction.action }}
            </td>
            <td>
              {{ transaction.amount }}
            </td>
            <td>
              {{ transaction.price_per_share }}
            </td>
            <td>
              {{ formatDateTime(transaction.time_stamp) }}
            </td>
          </tr>
        </tbody>
      </template>
    </v-simple-table>
  </v-card>
</template>

<script>
import walletRepo from "../repo/walletRepo.js";
var dayjs = require("dayjs");

export default {
  name: "PositionTable",
  props: {
    position: {
      type: Object,
      required: true,
    },
  },

  data: () => ({
    transactionView: false,
    transactions: null,
  }),

  methods: {
    formatDateTime(dateTime) {
      return dayjs(dateTime).format("DD MMM YYYY HH:mm");
    },

    emitClose() {
      this.$emit("close");
    },

    frequencyString(frequency) {
      if (frequency === "Frequency.ONE_DAY") {
        return "1d";
      }
      if (frequency === "Frequency.ONE_HOUR") {
        return "1h";
      }
      if (frequency === "Frequency.TEN_MINUTES") {
        return "10m";
      }
      if (frequency === "Frequency.ONE_MINUTE") {
        return "1m";
      }
      if (frequency === "Frequency.ONE_WEEK") {
        return "1w";
      }
      if (frequency === "Frequency.ONE_MONTH") {
        return "1M";
      } else {
        return "unknown";
      }
    },

    async loadTransactions() {
      await walletRepo
        .getTransactions(this.position._id)
        .then((data) => {
          this.transactions = data;
        })
        .catch((error) => {
          this.handleError(error);
        });
    },

    handleError(error) {
      console.log(error);
    },

    toggleView() {
      this.transactionView = !this.transactionView;
    },
  },

  created() {
    this.loadTransactions();
  },

  watch: {
    position: function () {
      this.loadTransactions();
    },
  },
};
</script>