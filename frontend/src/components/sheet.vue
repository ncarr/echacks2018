<template>
  <div class = "column">
    <v-layout id="options">
      <h1 class="font-weight-light title">Music Selector</h1>
      <div id="slider">
        <v-slider
        v-model="bpm"
        max="218"
        min="40"
        label="bpm"
        ></v-slider>
      </div>
      <div id="bpmtext">
        <v-text-field
          v-model="bpm"
          type="number"
        ></v-text-field>
      </div>
      <v-spacer></v-spacer>
      <div id="select">
        <v-select :items="items" label="Music" ></v-select>
      </div>
    </v-layout>
    <div id="music"></div>
  </div>

</template>

<script>
  export default {
    data: () => ({
      items: ['Foo', 'Bar', 'Fizz', 'Buzz'],
      bpm: 96
    })
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  #column {
    display: flex;
    flex-direction: column;
    align-items: center;
  }

  #slider{
    width: 15%;
    margin-left: 2%;
  }

  #select{
    width:10%;
  }

  #options{
    display: flex;
    flex-direction: row;
    align-items: center;
    padding: 10px;
  }

  #bpmtext{
    width: 5%;
  }
</style>
