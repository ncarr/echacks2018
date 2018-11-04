<template>

<div id="column">
    <h1 class="headline" v-if="expected">Expected</h1>
    <h1 class="headline" v-else>Valves</h1>
    <v-layout row wrap>
        <v-btn fab dark large :color="valve1 ? 'blue': 'purple'">1</v-btn>
        <v-btn fab dark large :color="valve2 ? 'blue': 'purple'">2</v-btn>
        <v-btn fab dark large :color="valve3 ? 'blue': 'purple'">3</v-btn>
    </v-layout>
    <v-layout row v-if="!expected">
      <v-btn dark :color="volume ? 'blue' : 'purple'">Now playing</v-btn>
    </v-layout>
</div>

</template>

<script>
  export default {
    name: 'Valves',
    props: {
      valve1: Boolean,
      valve2: Boolean,
      valve3: Boolean,
      volume: Boolean,
      expected: Boolean
    }
  }

</script>

<style scoped>
  #column {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
</style>
