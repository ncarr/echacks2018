<style scoped>

#row {
    display: flex;
    flex-direction: row;
}

#column {
    display: flex;
    flex-direction: column;
    align-items: center;
}

</style>

<template>

<div id="column">
    <h1 class="headline">Valves</h1>
    <div id="row">
        <v-btn fab dark large color="purple"></v-btn>
        <v-btn fab dark large color="purple"></v-btn>
        <v-btn fab dark large color="purple"></v-btn>
    </div>
</div>

</template>

<script>
  var ws = new WebSocket("ws://192.168.9.28:6789");

  ws.onopen = function() {
    console.log("Connection started...");
  };

  ws.onmessage = function(evt) {
      var received_msg = evt.data;
      var v1 = parseInt(received_msg.substring(0, 1));
      var v2 = parseInt(received_msg.substring(2, 3));
      var v3 = parseInt(received_msg.substring(4, 5));
      console.log(v1.toString() + " " + v2.toString() + " " + v2.toString());
  };

  ws.onclose = function() {
      // websocket is closed.
      console.log("Connection is closed...");
  };
</script>
