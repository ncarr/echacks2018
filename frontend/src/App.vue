<template>
  <v-app>
    <v-toolbar app>
      <v-toolbar-title class="headline text-uppercase">
        <span>ECHacks</span>
        <span class="font-weight-light">PROJECT NAME</span>
      </v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn
        flat
        href="https://github.com/vuetifyjs/vuetify/releases/latest"
        target="_blank"
      >
        <span class="mr-2">Latest Release</span>
      </v-btn>
    </v-toolbar>

    <v-content>
      <Valves/>
    </v-content>
  </v-app>
</template>

<script>
import Valves from './components/Valves'

export default {
  name: 'App',
  components: {
    Valves
  },
  data () {
    return {
      //
    }
  }
}
</script>
