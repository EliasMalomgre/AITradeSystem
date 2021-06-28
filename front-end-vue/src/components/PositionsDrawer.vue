<template>
  <v-card max-height="50em">
    <v-row justify="center">
      <v-subheader>
        <h2>Positions</h2>
      </v-subheader>
    </v-row>
    <v-row>
      <v-col :cols="10">
        <v-list
          v-if="positions.length !== 0"
          rounded
          v-scroll.self="onScroll"
          class="overflow-y-auto"
          max-height="45em"
        >
          <v-list-item-group
            v-model="selectedPosition"
            color="blue"
            @change="emitSelectedPosition()"
          >
            <v-list-item v-for="position in positions" :key="position._id">
              <v-list-content class="position">
                <v-row justify="center">
                  <v-col align-self="center">
                    <v-list-item-title
                      style="font-size: 14px"
                      v-text="
                        'Stock: ' +
                        position.stock_name +
                        ' | Freq: ' +
                        position.frequency
                      "
                    ></v-list-item-title>
                  </v-col>
                  <v-col align-self="center">
                    <v-list-item-title
                      style="font-size: 14px"
                      v-text="
                        'Length: ' +
                        position.posLength +
                        ' | R multiple: ' +
                        position.rMultiple
                      "
                    >
                    </v-list-item-title>
                  </v-col>
                  <v-col align-self="center">
                    <v-chip
                      small
                      v-if="position.open"
                      text-color="white"
                      color="green"
                      >OPEN</v-chip
                    >
                    <v-chip small v-else text-color="white" color="red"
                      >CLOSED</v-chip
                    >
                  </v-col>
                </v-row>
              </v-list-content>
            </v-list-item>
          </v-list-item-group>
        </v-list>
        <v-row v-else justify="center">
          <h3>Loading, please wait...</h3>
          <lottie-player
            src="https://assets4.lottiefiles.com/packages/lf20_wxoju3be.json"
            background="transparent"
            speed="1"
            style="width: 300px; height: 300px"
            loop
            autoplay
          ></lottie-player>
        </v-row>
      </v-col>
      <v-col :cols="1" align-self="center">
        <v-btn icon color="red" @click="emitClose">
          <v-icon x-large>mdi-chevron-left</v-icon>
        </v-btn>
      </v-col>
    </v-row>
  </v-card>
</template>


<script>
require("@lottiefiles/lottie-player");
export default {
  name: "PositionsDrawer",
  props: {
    positions: {
      type: Array,
      required: true,
    },
  },
  data: () => ({
    selectedPosition: 0,
  }),

  methods: {
    emitSelectedPosition() {
      this.$emit("selectedPosition", this.positions[this.selectedPosition]);
    },
    emitClose() {
      this.$emit("close");
    },
  },

  created() {
    this.selectedPosition = this.positions[0];
  },
};
</script>