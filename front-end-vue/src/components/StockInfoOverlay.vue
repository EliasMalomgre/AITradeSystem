<template>
  <v-dialog transition="dialog-bottom-transition" max-width="50%">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="primary" v-bind="attrs" v-on="on" small>
        <v-icon>mdi-information-variant</v-icon>
      </v-btn>
    </template>

    <template v-slot:default="dialog">
      <v-card height="300px">
        <v-container>
          <v-row justify="center">
            <v-col :cols="10">
              <h2>{{ infoData.longName }}</h2>
            </v-col>
            <v-col :cols="1">
              <v-btn @click="dialog.value = false" icon> <v-icon color="red">
                  mdi-close</v-icon></v-btn>
            </v-col>
          </v-row>
          <v-row justify="center">
              <v-col align-self="center" :cols="5">
                  <v-card color="" height="150px">
                        <p><b>Company info:</b> <br>
                            Sector: {{infoData.sector}} <br>
                           Industry: {{infoData.industry}} <br>
                           Fulltime employees: {{infoData.fullTimeEmployees}}
                        </p>
                  </v-card>
              </v-col>
            <v-col align-self="center" :cols="3">
              <v-card color="" height="150px">
                <p>
                  <b>Address:</b> <br />
                  {{ infoData.address1 }} <br />
                  {{ infoData.zip }} {{ infoData.city }} <br />
                  {{ infoData.country }} <br />
                  <a :href="infoData.website"> Website</a>
                </p>
              </v-card>
            </v-col>
            <v-col align-self="center" cols="3">
              <v-card color="" height="150px">
                <p>
                  <b>Regular market info:</b> <br />
                  High: {{ infoData.regularMarketDayHigh }} <br />
                  Low: {{ infoData.regularMarketDayLow }} <br />
                  Open: {{ infoData.regularMarketOpen }} <br />
                  Close: {{ infoData.regularMarketPreviousClose }} <br />
                  Volume: {{ infoData.regularMarketVolume }}
                </p>
              </v-card>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </template>
  </v-dialog>
</template>

<script>
export default {
  name: "stockInfoOverlay",
  props: {
    infoData: {
      type: Object,
      required: true,
    },
  },
  data: () => ({
    dialog: false,
  }),
  methods:{
      closeOverlay(){
          this.dialog = false;
      }
  }
};
</script>