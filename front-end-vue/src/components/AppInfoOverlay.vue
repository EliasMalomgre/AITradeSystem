<template>
  <v-dialog transition="dialog-bottom-transition" max-width="50%">
    <template v-slot:activator="{ on, attrs }">
      <v-list-item v-bind="attrs" v-on="on" link @click="setView('pos')">
        <v-list-item-icon>
          <v-icon>mdi-information-outline</v-icon>
        </v-list-item-icon>
        <v-list-item-title>info</v-list-item-title>
      </v-list-item>
    </template>

    <template v-slot:default="dialog">
      <v-card>
        <v-container>
          <v-row justify="center">
            <v-col :cols="10">
              <h2>App information</h2>
            </v-col>
            <v-col cols="1" align-self="right">
              <v-btn @click="dialog.value = false" icon>
                <v-icon color="red">mdi-close</v-icon>
              </v-btn>
            </v-col>
          </v-row>
          <v-row justify="center">
            <p>
              <b>Pages:</b> <br />
              Historic data: <br />
              Use this page to view a candlestick chart of the stock, frequency
              and dates you selected. <br />
              If no data shows up on the chart, press request to download the
              data from Yahoo finance. <br />
              To bring incomplete data up-to-date, press quick update. <br />
              To view general information about the company behind the stock,
              press <v-icon>mdi-information-variant</v-icon> <br />
              <br />
              Positions: <br />
              This page will load all the positions in your wallet. <br />
              Use the list on the left to select the position you want to view.
              <br />
              Press the <v-icon>mdi-information-variant</v-icon> button to view
              all the details about the selected position. <br />
              <br />
              <br />
              <b>Label legend:</b> <br />
              Format: <i>amount of shares</i> x <i>price per share</i> $ <br />
              Stop-loss is shown using blue dots <br />
              <v-chip text-color="white" color="#80e27e">Buy</v-chip>
              <v-chip text-color="white" color="#ff7961">Sell</v-chip>
              <v-chip text-color="white" color="#63a4ff">Short</v-chip>
              <v-chip text-color="white" color="#ffd95a">Cover</v-chip>
            </p>
          </v-row>
          <v-row justify="center">
            <lottie-player
          src="https://assets4.lottiefiles.com/packages/lf20_VuglDs.json"
          background="transparent"
          speed="1"
          style="width: 300px; height: 300px"
          loop
          autoplay
        ></lottie-player>
          </v-row>
          <v-row justify="center">
            <h4>Stonksbot by Elias Malomgré, Laurien Cools and Tim Schelpe</h4>
          </v-row>
        </v-container>
      </v-card>
    </template>
  </v-dialog>
</template>

<script>
export default {
  name: "AppInfoOverlay",
};
</script>