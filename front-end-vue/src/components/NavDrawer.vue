<template>
    <v-navigation-drawer app v-model="drawer">
      <v-list-item>
          <v-list-item-avatar>
              <v-img src="../resources/stonks.png"></v-img>
          </v-list-item-avatar>
        <v-list-item-content>
          <v-list-item-title class="title">
            Stonksbot
          </v-list-item-title>
          <v-list-item-subtitle>
            A trade simulation AI
          </v-list-item-subtitle>
        </v-list-item-content>
      </v-list-item>

      <v-divider></v-divider>

       <v-list
          nav
          dense
        >
        <v-list-item link @click="setView('hist')">
            <v-list-item-icon>
              <v-icon>mdi-history</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Historic data</v-list-item-title>
          </v-list-item>
          <v-list-item link @click="setView('pos')">
            <v-list-item-icon>
              <v-icon>mdi-trending-up</v-icon>
            </v-list-item-icon>
            <v-list-item-title>Positions</v-list-item-title>
          </v-list-item>
          <v-list-item link @click="setView('ai')">
            <v-list-item-icon>
              <v-icon>mdi-robot</v-icon>
            </v-list-item-icon>
            <v-list-item-title>AI controller</v-list-item-title>
          </v-list-item>
          <appInfoOverlay/>
       </v-list>
    </v-navigation-drawer>
</template>

<script>
import AppInfoOverlay from "./AppInfoOverlay"
export default {
    name: "NavDrawer",
    props:{
        drawer:{
            type: Boolean,
            required: true,
        },
    },
    methods: {
        setView(view){
            this.$emit("setView", view)
        },
    },

    components:{
      appInfoOverlay: AppInfoOverlay,
    },
}
</script>