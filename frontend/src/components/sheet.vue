

<template>
  <div style="text-align:center">
  <h1 class="headline">Dashboard</h1>
  <p> Welcome to the Sensor Baritone </p>
  <button type="button"> Enter Name and Music </button>
  <br/>
      <canvas ref="mainCanvas" width="1000" height="250" style="width: 70%; margin: 20px; height: 25%;">

      </canvas>
  <div class = "column">
    <v-layout row wrap id="options">
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

    //Todo not hardcode
    const notes = [{"note": 48, "time": 0.75}, {"note": 46, "time": 1.25}, {"note": 48, "time": 0.75}, {"note": 46, "time": 1.25}, {"note": 0, "time": 1.0}, {"note": 46, "time": 0.25}, {"note": 46, "time": 0.25}, {"note": 46, "time": 0.25}, {"note": 46, "time": 0.25}, {"note": 53, "time": 0.5}, {"note": 51, "time": 0.25}, {"note": 50, "time": 0.5}, {"note": 48, "time": 0.75}, {"note": 48, "time": 0.75}, {"note": 46, "time": 1.25}, {"note": 48, "time": 0.75}, {"note": 50, "time": 0.5}, {"note": 48, "time": 0.25}, {"note": 46, "time": 0.25}, {"note": 53, "time": 2.25}];

    export default {
        mounted(){
            let noteCanvas = this.$refs.mainCanvas.getContext("2d");
            let canvHeight = this.$refs.mainCanvas.height;
            let canvWidth = this.$refs.mainCanvas.width;
            noteCanvas.clearRect(0,0, noteCanvas.width, noteCanvas.height);
            this.drawStaff(noteCanvas, canvWidth, canvHeight);
        },

        methods: {
            drawStaff(theCanvas, cWidth, cHeight) {
                theCanvas.lineWidth = 2;
                //Draw the actual staff
                theCanvas.beginPath();
                //Draw the staff
                let centreStaff = cHeight/2;
                let staffSpace = 20;
                for (let i = -2; i <= 2; i++) {
                    theCanvas.moveTo(0, centreStaff + i * staffSpace);
                    theCanvas.lineTo(cWidth, centreStaff + i * staffSpace);
                    theCanvas.stroke();
                }
                theCanvas.closePath();

            },

            drawNote(theCanvas, cWidth, cHeight, note, length) {
                //For length, one bar = 2
                //Draw notes relative to centre staff


            }
        },


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
  }

  #select{
    width:10%;
  }

  #options{
    padding: 10px;
  }

  #bpmtext{
    width: 5%;
  }
</style>
