<template>
  <v-container>
    <v-row justify="center">
      <v-col :cols="1" v-if="!posDrawerVisible" align-self="center">
        <v-btn icon color="blue" @click="togglePosDrawerVisible" style="padding-right: 2em">
          <v-icon x-large>mdi-chevron-right</v-icon>
        </v-btn>
      </v-col>
      <v-col :cols="11">
        <positionsDrawer
          v-if="posDrawerVisible"
          :positions="positions"
          @selectedPosition="emitPosition"
          @close="togglePosDrawerVisible"
        />
      </v-col>
    </v-row>
    <v-row justify="center"
    style="padding-top: 10px"
    >
      <overlay :position="selectedPosition" />
    </v-row>
  </v-container>
</template>

<script>
import walletRepo from "../repo/walletRepo.js";
import PositionsDrawer from "../components/PositionsDrawer";
import Overlay from "../components/Overlay";

export default {
  name: "Position",

  data: () => ({
    wallet: Object,
    posDrawerVisible: true,
    positions: [],
    selectedPosition: {
      _id: "0",
      stock_name: "loading",
      frequency: "loading",
      current_transactions: [],
      current_amount: 0,
      total_buy_price: 0,
      average_buy_price: 0,
      p_and_l: 0,
      stop_loss: 0,
      risk: 0,
      current_share_price: 0,
    },
  }),
  methods: {
    async loadData() {
      await walletRepo
        .getWallet()
        .then((data) => {
          console.log(data);
          this.wallet = data;
        })
        .catch((error) => {
          this.handleError("Loading wallet failed", error);
        });
      await walletRepo
        .getPositions()
        .then((data) => {
          console.log(data);
          this.positions = data;
          this.selectedPosition = data[0];
        })
        .catch((error) => {
          this.handleError("Loading positions failed", error);
        });
    },

    emitPosition(position) {
      this.selectedPosition = position;
      this.$emit("setPositionForChart", position);
    },

    emitPositionCols() {
      if (this.posDrawerVisible) {
        return this.$emit("positionCols", true);
      } else {
        return this.$emit("positionCols", false);
      }
    },

    togglePosDrawerVisible() {
      this.posDrawerVisible = !this.posDrawerVisible;
      this.emitPositionCols();
    },
    togglePosTableVisible() {
      this.posTableVisible = !this.posTableVisible;
      this.emitPositionCols();
    },

    handleError(error) {
      console.log(error);
    },
  },

  created() {
    this.loadData();
  },

  watch: {
    selectedPosition: function (newVal) {
      this.$emit("setPositionForChart", newVal);
    },
  },

  components: {
    positionsDrawer: PositionsDrawer,
    overlay: Overlay,
  },
};
</script>