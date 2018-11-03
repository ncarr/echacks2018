<template>
  <div style="text-align:center">
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
  </div>
</template>

<script>
  export default {
    data: () => ({
      items: ['Foo', 'Bar', 'Fizz', 'Buzz'],
      bpm: 96
    }),
    mounted() {
      var VF = Vex.Flow;

      // Create an SVG renderer and attach it to the DIV element named "boo".
      var div = document.getElementById("music")
      var renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);

      // Size our svg:
      renderer.resize(500, 500);

      // And get a drawing context:
      var context = renderer.getContext();

      // Create a stave at position 10, 40 of width 400 on the canvas.
      var stave = new VF.Stave(10, 40, 400);

      // Add a clef and time signature.
      stave.addClef("treble").addTimeSignature("4/4");

      // Connect it to the rendering context and draw!
      stave.setContext(context).draw();
    }
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

  #music{
    width: 100%;
  }
</style>
