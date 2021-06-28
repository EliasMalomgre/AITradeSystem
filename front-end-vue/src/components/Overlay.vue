<template>
  <v-dialog transition="dialog-bottom-transition" max-width="50%">
    <template v-slot:activator="{ on, attrs }">
      <v-btn color="primary" v-bind="attrs" v-on="on" fab small>
          <v-icon>mdi-information-variant</v-icon>
      </v-btn>
    </template>

    <template v-slot:default="dialog">
      <v-card>
        <positionTable :position="position" 
        @close="dialog.value = false"/>
      </v-card>
    </template>
  </v-dialog>
</template>
<script>
import PositionTable from "./PositionTable";
export default {
  name: "Overlay",
  props: {
    position: {
      type: Object,
      required: false,
    },
  },
  data: () => ({
    dialog: false,
  }),

  methods: {
    closeDialog() {
      this.dialog = false;
    },
  },

  components: {
    positionTable: PositionTable,
  },
};
</script>