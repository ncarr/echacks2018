<template>
  <v-app>
    <v-toolbar app color="#c8a415">
      <v-toolbar-title class="headline text-uppercase">
        <span>ECHacks</span>
        <span class="font-weight-light">PROJECT NAME</span>
      </v-toolbar-title>
    </v-toolbar>

    <v-content>
      <sheet :song="song"/>
      <Valves :valve1="valve1" :valve2="valve2" :valve3="valve3" />
      <!--<dashboard/>-->
    </v-content>
  </v-app>
</template>

<script>
import Valves from './components/Valves'
import dashboard from './components/dashboard'
import sheet from './components/sheet'

export default {
  name: 'App',
  components: {
    Valves,
    dashboard,
    sheet
  },
  data () {
    return {
      valve1: false,
      valve2: false,
      valve3: false,
      volume: false,
      song: null,
      current: null
    }
  },
  mounted() {
      var scope = this;
      var ws = new WebSocket("ws://localhost:6789");

      ws.onopen = function() {
        ws.send('json')
        console.log("Connection started...");
      };

      ws.onmessage = function(evt) {
          var received_msg = evt.data;
          if (received_msg.length === 7) {
            // Set the valves to booleans of the received data
            scope.valve1 = !!parseInt(received_msg.substring(0, 1));
            scope.valve2 = !!parseInt(received_msg.substring(2, 3));
            scope.valve3 = !!parseInt(received_msg.substring(4, 5));
            scope.volume = !!parseInt(received_msg.substring(6, 7));
            console.log(scope.valve1.toString() + " " + scope.valve2.toString() + " " + scope.valve3.toString());
          } else if (received_msg[0] === '[') {
            scope.song = JSON.parse(received_msg);
          } else {
            scope.current = JSON.parse(received_msg);
          }
      };

      ws.onclose = function() {
          // websocket is closed.
          console.log("Connection is closed...");
      };
  }
}
</script>
