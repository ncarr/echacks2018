<template>

<div id="column">
    <h1 class="headline">Valves</h1>
    <v-layout row wrap>
        <v-btn fab dark large :color="vc1">1</v-btn>
        <v-btn fab dark large :color="vc2">2</v-btn>
        <v-btn fab dark large :color="vc3">3</v-btn>
    </v-layout>
</div>

</template>

<script>
  export default {
    name: 'Valves',
    props: {
      msg: String
    },
    data() {
      return {
        vc1 : "purple",
        vc2 : "purple",
        vc3 : "purple"
      }
    },
    mounted() {
      var scope = this;
      var ws = new WebSocket("ws://192.168.137.1:6789");

      ws.onopen = function() {
        //ws.send("0 1 1");
        ws.send("ping");
        console.log("Connection started...");
      };

      ws.onmessage = function(evt) {
          var received_msg = evt.data;
          var v1 = parseInt(received_msg.substring(0, 1));
          var v2 = parseInt(received_msg.substring(2, 3));
          var v3 = parseInt(received_msg.substring(4, 5));
          console.log(v1.toString() + " " + v2.toString() + " " + v3.toString());

          if(v1==1){
            scope.vc1 = "blue";
          } else {
            scope.vc1 = "purple";
          }

          if(v2==1){
            scope.vc2 = "blue";
          } else {
            scope.vc2 = "purple";
          }

          if(v3==1){
            scope.vc3 = "blue";
          } else {
            scope.vc3 = "purple";
          }
      };

      ws.onclose = function() {
          // websocket is closed.
          console.log("Connection is closed...");
      };
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
