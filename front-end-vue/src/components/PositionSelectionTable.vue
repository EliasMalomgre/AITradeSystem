<template>
    <v-simple-table fixed-header height="25em">
          <template>
            <thead>
              <tr>
                <th>Stock</th>
                <th>Frequency</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="position in positions" :key="position._id">
                <td>
                  {{ position.stock_name }}
                </td>
                <td>
                  {{ position.frequency }}
                </td>
                <td>Coming soon to StonksBot!</td>
                <td>
                  <v-btn @click="selectedPosition = position">SELECT</v-btn>
                </td>
              </tr>
            </tbody>
          </template>
        </v-simple-table>
</template>

<script>
export default {
    name: "PositionSelectionTable",
    props:{
        positions:{
            type: Array,
            required: true,
        },

        data: () =>({
            selectedPosition: {},
        }),
    }
}
</script>