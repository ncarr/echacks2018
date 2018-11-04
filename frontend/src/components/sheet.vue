<template>
  <div style="text-align:center" id="bg">
    <div class = "column">
      <v-layout id="options" class="row">
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
      <div id="pages" class="row">
        <h1 class="font-weight-light title">Page 1 of 1</h1>
      </div>
      <div id="music"></div>
    </div>
  </div>
</template>

<script>
  import dict from '../assets/notes.json';
  export default {
    data: () => ({
      items: ['Foo', 'Bar', 'Fizz', 'Buzz'],
      bpm: 120
    }),
    mounted() {
      var song = [{"note": 48, "time": 0.75}, {"note": 46, "time": 1.25}, {"note": 48, "time": 0.75}, {"note": 46, "time": 1.25}, {"note": 0, "time": 1.0}, {"note": 46, "time": 0.25}, {"note": 46, "time": 0.25}, {"note": 46, "time": 0.25}, {"note": 46, "time": 0.25}, {"note": 53, "time": 0.5}, {"note": 51, "time": 0.25}, {"note": 50, "time": 0.5}, {"note": 48, "time": 0.75}, {"note": 48, "time": 0.75}, {"note": 46, "time": 1.25}, {"note": 48, "time": 0.75}, {"note": 50, "time": 0.5}, {"note": 48, "time": 0.25}, {"note": 46, "time": 0.25}, {"note": 53, "time": 2.25}]

      console.log(song);
      console.log(dict);

      var VF = Vex.Flow;

      // Create an SVG renderer and attach it to the DIV element named "boo".
      var div = document.getElementById("music")
      var renderer = new VF.Renderer(div, VF.Renderer.Backends.SVG);
      // Size our svg:
      renderer.resize(div.clientWidth, div.clientHeight);
      // And get a drawing context:
      var context = renderer.getContext();
      // Create a stave at position 10, 40 of width 400 on the canvas.
      var stave = new VF.Stave(10, 40, div.clientWidth-20);
      // Add a clef and time signature.
      stave.addClef("bass").addTimeSignature("4/4");
      // Connect it to the rendering context and draw!
      stave.setContext(context).draw();

      var notes = [];

      for(let i = 0; i < song.length; i++){
        //Drawing notes
        var note = dict[song[i].note];
        console.log(note);
        //Flat
        if(note.length == 4){
          notes.push(new VF.StaveNote({clef: "bass", keys: [note], duration: "q" }).
          addAccidental(0, new VF.Accidental("b")));
        } else if(note.length == 3) { //Regular note
          notes.push(new VF.StaveNote({clef: "bass", keys: [note], duration: "q" }));
        } else { //flat
          notes.push(new VF.StaveNote({clef: "bass", keys: ["d/3"], duration: "qr" }));
        }

        //Measure bars
        if((i+1)%4 == 0){
          notes.push(new VF.BarNote());
        }
      }

      // Create a voice in 4/4 and add above notes
      var voice = new VF.Voice({num_beats: song.length,  beat_value: 4});
      voice.addTickables(notes);

      // Format and justify the notes to 400 pixels.
      var formatter = new VF.Formatter().joinVoices([voice]).format([voice], div.clientWidth);

      // Render voice
      voice.draw(context, stave);

      // Scroll
      /*
      while(music.scrollLeft > 0){
        music.scrollLeft
      }*/
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  .row{
    display: flex;
    flex-direction: row;
    align-items: center;
  }

  .column {
    display: flex;
    flex-direction: column;
    align-items: center;
    height: 100%;
  }

  #slider{
    width: 15%;
    margin-left: 2%;
  }

  #select{
    width:10%;
  }

  #options{
    padding: 10px;
  }

  #bpmtext{
    width: 10%;
  }

  #music{
    width: 100%;
    height: 100%;
  }

  #bg{
    height: 100%;
  }
</style>
