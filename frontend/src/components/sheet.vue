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
      </v-layout>
      <div id="overflow">
          <div id="music"></div>
          <div id="line"></div>
      </div>
    </div>
  </div>
</template>

<script>
  import dict from '../assets/notes.json';
  export default {
    data: () => ({
      items: ['Foo', 'Bar', 'Fizz', 'Buzz'],
      bpm: 120,
      group: null,
      context: null,
      stave: null,
      renderer: null,
      div: null,
    }),
    props: ['song'],
    mounted(){
      // Create an SVG renderer and attach it to the DIV element named "boo".
      var VF = Vex.Flow;
      this.div = document.getElementById("music")
      this.renderer = new VF.Renderer(this.div, VF.Renderer.Backends.SVG);
      // Size our svg:
      this.renderer.resize(this.div.clientWidth, this.div.clientHeight);
      // And get a drawing context:
      this.context = this.renderer.getContext();
      // Create a stave at position 10, 40 of width 400 on the canvas.
      this.stave = new VF.Stave(10, 40, this.div.clientWidth-20);
      // Add a clef and time signature.
      this.stave.addClef("bass").addTimeSignature("4/4");
      // Connect it to the rendering context and draw!
      this.stave.setContext(this.context).draw();
      //Create group
      this.group = this.context.openGroup();
      this.context.closeGroup();
    },
    watch: {
        song(song) {
        //Remove group when needed
        this.context.svg.removeChild(this.group);
        this.group = this.context.openGroup();
        console.log(dict);

        var VF = Vex.Flow;

        let notes = [];
        let ties = [];
        let tieToLastNote;

        let timeInBar = 0;
        let totalBeats = 0;

        //ugly hack
        let barFlag = false;

        for(let i = 0; i < song.length; i++){
            //Drawing notes
            var noteName = dict[song[i].note];
            var note = song[i];
            totalBeats += note.time;
            console.log(noteName);

            const noteMap = {
                0.25 : "8",
                0.5 : "4",
                1 : "2",
                2 : "1"
            };

            let duration;

            //Determine note length
            //Note that one bar = 2s
            //notes :w :h :q :8 :16 :32 :64
            // notes :hd :qd :8d :16d :32d :64d (Adding a d for dotted notes)

            console.log("Initiated note.");
            console.log("Beats in note:" + note.time);
            console.log("Beats in bar so far: " + timeInBar);
            if (timeInBar + note.time <= 2) {
                //Ensure there's enough room left in the current bar
                console.log("Enough left in current bar");
                timeInBar += note.time;
                if (noteMap[note.time] !== undefined) {
                    //Straight add the note, nothing else is required
                    console.log("This note makes sense");
                    duration = noteMap[note.time];
                } else if (noteMap[(note.time / 3) * 2] !== undefined) {
                    console.log("This is a dotted note");
                    duration = noteMap[(note.time / 3) * 2] + "d";
                } else {
                    //Tied note
                    console.log("Tied note");
                    let noteLengths = Object.keys(noteMap);
                    let noteDurations = [];
                    let timeLeftToFill = note.time;
                    let biggestWholeFit = 0;
                    //Keep figuring out which notes we need to tie together
                    while (timeLeftToFill > 0) {
                        console.log("Trying to fill " + timeLeftToFill);
                        for (let i = 0; i < noteLengths.length; i++) {
                            console.log("Checking " + noteLengths[i]);
                            if ((noteLengths[i] <= timeLeftToFill) && (noteLengths[i] > biggestWholeFit)) {
                                console.log(noteLengths[i] + " is less than " + timeLeftToFill);
                                biggestWholeFit = noteLengths[i];
                            }
                        }
                        noteDurations.push(biggestWholeFit);
                        console.log("Biggest whole fit to " + timeLeftToFill + ": " + biggestWholeFit);
                        timeLeftToFill = (timeLeftToFill- biggestWholeFit);
                        console.log(timeLeftToFill);
                        biggestWholeFit = 0;
                    }
                    console.log(noteDurations);
                    for (let i = 0; i < noteDurations.length - 1; i++) {
                        let currentNote = new VF.StaveNote({clef: "bass", keys: [noteName], duration: noteMap[noteDurations[i]]});
                        if (tieToLastNote) {
                            ties.push(new VF.StaveTie({
                                first_note: tieToLastNote,
                                last_note: currentNote,
                                first_indices: [0],
                                last_indices: [0]
                            }));
                        }
                        tieToLastNote = currentNote;
                        notes.push(currentNote);
                    }
                    duration = noteMap[noteDurations[noteDurations.length - 1]];
                }
            } else {
                console.log("Current bar almost over");
                let firstNoteLength = 2-timeInBar;
                timeInBar += firstNoteLength;
                //We're at the end of the measure. Add the last note and then move on
                if (noteMap[firstNoteLength] !== undefined) {
                    //Straight add the note, nothing else is required
                    console.log("This note makes sense");
                    duration = noteMap[firstNoteLength];
                } else if (noteMap[(firstNoteLength / 3) * 2] !== undefined) {
                    console.log("This is a dotted note");
                    duration = noteMap[(firstNoteLength / 3) * 2] + "d";
                } else {
                    //Tied note
                    console.log("Tied note");
                    let noteLengths = Object.keys(noteMap);
                    let noteDurations = [];
                    let timeLeftToFill = firstNoteLength;
                    let biggestWholeFit = 0;
                    //Keep figuring out which notes we need to tie together
                    while (timeLeftToFill > 0) {
                        console.log("Trying to fill " + timeLeftToFill);
                        for (let i = 0; i < noteLengths.length; i++) {
                            console.log("Checking " + noteLengths[i]);
                            if ((noteLengths[i] <= timeLeftToFill) && (noteLengths[i] > biggestWholeFit)) {
                                console.log(noteLengths[i] + " is less than " + timeLeftToFill);
                                biggestWholeFit = noteLengths[i];
                            }
                        }
                        noteDurations.push(biggestWholeFit);
                        console.log("Biggest whole fit to " + timeLeftToFill + ": " + biggestWholeFit);
                        timeLeftToFill = (timeLeftToFill- biggestWholeFit);
                        console.log(timeLeftToFill);
                        biggestWholeFit = 0;
                    }
                    console.log(noteDurations);
                    for (let i = 0; i < noteDurations.length - 1; i++) {
                        let currentNote = new VF.StaveNote({clef: "bass", keys: [noteName], duration: noteMap[noteDurations[i]]});
                        if (tieToLastNote) {
                            ties.push(new VF.StaveTie({
                                first_note: tieToLastNote,
                                last_note: currentNote,
                                first_indices: [0],
                                last_indices: [0]
                            }));
                        }
                        tieToLastNote = currentNote;
                        notes.push(currentNote);
                    }
                    duration = noteMap[noteDurations[noteDurations.length - 1]];
                }

                barFlag = true;

                console.log("Note to play: " + note.time);
                console.log("Length of last note in bar: " + firstNoteLength);
                if (note.time > firstNoteLength) {
                    console.log("Not enough left in current bar");
                    barFlag = false;
                    console.log(duration);

                    //Flat
                    let currentNote;
                    if(noteName.length === 4){
                        currentNote = new VF.StaveNote({clef: "bass", keys: [noteName], duration: duration});
                        currentNote.addAccidental(0, new VF.Accidental("b"));
                    } else {
                        //rest
                        duration += "r";
                        currentNote = new VF.StaveNote({clef: "bass", keys: [noteName], duration: duration});
                    }
                    tieToLastNote = currentNote;
                    notes.push(currentNote);
                    console.log("aaaa");
                    let secondNoteLength = note.time - firstNoteLength;
                    console.log("First note of next bar: " + secondNoteLength);
                    timeInBar = secondNoteLength;
                    if (noteMap[secondNoteLength] !== undefined) {
                        //Straight add the note, nothing else is required
                        console.log("This note makes sense");
                        duration = noteMap[secondNoteLength];
                    } else if (noteMap[(secondNoteLength / 3) * 2] !== undefined) {
                        console.log("This is a dotted note");
                        duration = noteMap[(secondNoteLength / 3) * 2] + "d";
                    } else {
                        //Tied note
                        console.log("Tied note");
                        let noteLengths = Object.keys(noteMap);
                        let noteDurations = [];
                        let timeLeftToFill = secondNoteLength;
                        let biggestWholeFit = 0;
                        //Keep figuring out which notes we need to tie together
                        while (timeLeftToFill > 0) {
                            console.log("Trying to fill " + timeLeftToFill);
                            for (let i = 0; i < noteLengths.length; i++) {
                                console.log("Checking " + noteLengths[i]);
                                if ((noteLengths[i] <= timeLeftToFill) && (noteLengths[i] > biggestWholeFit)) {
                                    console.log(noteLengths[i] + " is less than " + timeLeftToFill);
                                    biggestWholeFit = noteLengths[i];
                                }
                            }
                            noteDurations.push(biggestWholeFit);
                            console.log("Biggest whole fit to " + timeLeftToFill + ": " + biggestWholeFit);
                            timeLeftToFill = (timeLeftToFill- biggestWholeFit);
                            console.log(timeLeftToFill);
                            biggestWholeFit = 0;
                        }
                        console.log(noteDurations);
                        for (let i = 0; i < noteDurations.length - 1; i++) {
                            let currentNote = new VF.StaveNote({clef: "bass", keys: [noteName], duration: noteMap[noteDurations[i]]});
                            if (tieToLastNote) {
                                ties.push(new VF.StaveTie({
                                    first_note: tieToLastNote,
                                    last_note: currentNote,
                                    first_indices: [0],
                                    last_indices: [0]
                                }));
                            }
                            tieToLastNote = currentNote;
                            notes.push(currentNote);
                        }
                        duration = noteMap[noteDurations[noteDurations.length - 1]];
                    }
                } else {
                    console.log("Exactly enough left in current bar");
                    timeInBar = 0;
                }
            }

            console.log("Note duration: " + duration);
                if (duration == 1) {
                    notes.push(new VF.BarNote());
                }
            let currentNote = new VF.StaveNote({clef: "bass", keys: [noteName], duration: duration});

            if (duration.charAt(duration.length - 1) == 'd') {
                currentNote.addDotToAll();
            }
            //Flat
            if(noteName.length === 4){
                //Flat
            currentNote.addAccidental(0, new VF.Accidental("b"));
            } else {
                //rest
                console.log("Rest");
            }

            if (tieToLastNote) {
                ties.push(new VF.StaveTie({
                    first_note: tieToLastNote,
                    last_note: currentNote,
                    first_indices: [0],
                    last_indices: [0]
                }));
            }
            tieToLastNote = false;

            notes.push(currentNote);
            if (barFlag || timeInBar === 2) {
                notes.push(new VF.BarNote());
                timeInBar = 0;
                barFlag = false;
            }

        }
        console.log("Added all notes. Moving on to voice.");

        console.log("Total beats in piece: " + (totalBeats * 2).toString());
        // Create a voice in 4/4 and add above notes
        var voice = new VF.Voice({num_beats: totalBeats * 2,  beat_value: 4});
        voice.addTickables(notes);

        console.log("notes length:");
        console.log(notes.length);
        console.log(notes.length*50);
        // Size our svg:
        this.renderer.resize(notes.length*50, this.div.clientHeight);
        // And get a drawing context:
        var context = this.renderer.getContext();
        // Create a stave at position 10, 40 of width 400 on the canvas.
        var stave = new VF.Stave(10, 40, notes.length*50);
        // Add a clef and time signature.
        stave.addClef("bass").addTimeSignature("4/4");
        // Connect it to the rendering context and draw!
        stave.setContext(context).draw();

        // Format and justify the notes to 400 pixels.
        var formatter = new VF.Formatter().joinVoices([voice]).format([voice], notes.length*50);

        //Create group
        //const group = context.openGroup();

        // Render voice
        voice.draw(this.context, this.stave);
        ties.forEach((t) => {t.setContext(this.context).draw()})
        //group
        this.context.closeGroup();
        this.context.svg.appendChild(this.group)

        // Scroll
        /*
        while(music.scrollLeft > 0){
            music.scrollLeft
        }*/
        }
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
  }

  #slider{
    width: 15%;
    margin-left: 2%;
  }

  #options{
    padding: 10px;
  }

  #bpmtext{
    width: 10%;
  }

  #music{
    overflow: visible;
    height: 100%;
    transition: transform 5s linear;
  }
  #music:hover{
    transform: translateX(-2000px);
  }

  #overflow{
    width: 100%;
  }

  #bg{
  }

  #line{
    border-left: 6px solid green;
    height: 100px;
    position: absolute;
    left: 40;
    top: 10;
  }
</style>
