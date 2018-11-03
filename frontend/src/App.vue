<template>
  <v-app>
    <v-toolbar app color="#c8a415">
      <v-toolbar-title class="headline text-uppercase">
        <span>ECHacks</span>
        <span class="font-weight-light">PROJECT NAME</span>
      </v-toolbar-title>
    </v-toolbar>

    <v-content>
      <sheet/>
      <dashboard/>
      <Valves/>
      <!--<Valves/>
      <dashboard/>-->
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
      //
    }
  }
}
</script>
