<template>
  <v-app>
    <v-toolbar app color="#c8a415">
      <v-toolbar-title class="headline text-uppercase">
        <span>ECHacks</span>
        <span class="font-weight-light">PROJECT NAME</span>
      </v-toolbar-title>
    </v-toolbar>

    <v-content>
      <v-select :items="items" v-model="songFile" />
      <sheet :song="songJson"/>
      <Valves :valve1="valve1" :valve2="valve2" :valve3="valve3" :volume="volume" />
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
      ws: null,
      valve1: false,
      valve2: false,
      valve3: false,
      volume: false,
      songJson: null,
      songFile: 'Birdland.mid',
      current: null,
      items: [
        {
          text: 'Birdland',
          value: 'Birdland.mid'
        },
        {
          text: 'Don\'t Stop Believing',
          value: 'Don\'t_Stop_Believing.mid'
        },
        {
          text: 'Mad World',
          value: 'Mad_World.mid'
        },
        {
          text: 'Length Test',
          value: 'Length_Test.mid'
        }
      ]
    }
  },
  watch: {
    songFile(newFile) {
      if (this.ws.readyState === WebSocket.OPEN) {
        this.ws.send('json ' + newFile);
      }
    }
  },
  mounted() {
      var scope = this;
      this.ws = new WebSocket("ws://192.168.9.28:6789");

      this.ws.onopen = function() {
        scope.ws.send('json ' + scope.songFile);
        console.log("Connection started...");
      };

      this.ws.onmessage = function(evt) {
          // Update state whenever a message comes in
          var received_msg = evt.data;
          if (received_msg.length === 7) {
            // Set the valves to booleans of the received data
            scope.valve1 = !!parseInt(received_msg.substring(0, 1));
            scope.valve2 = !!parseInt(received_msg.substring(2, 3));
            scope.valve3 = !!parseInt(received_msg.substring(4, 5));
            scope.volume = !!parseInt(received_msg.substring(6, 7));
            console.log(scope.valve1.toString() + " " + scope.valve2.toString() + " " + scope.valve3.toString());
          } else if (received_msg[0] === '[') {
            scope.songJson = JSON.parse(received_msg);
          } else {
            scope.current = JSON.parse(received_msg);
          }
      };

      this.ws.onclose = function() {
          // websocket is closed.
          console.log("Connection is closed...");
      };
  }
}
</script>
