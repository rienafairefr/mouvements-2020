<template>
  <div>
    {{map_window}}
    <label for="sigle-select">SIGLE</label>
    <select id="sigle-select" v-model="sigle" class="my-select">
      <option v-for="sigle in sigles" :key="sigle">{{sigle}}</option>
    </select>
    <label for="circonscription-select">CIRCONSCRIPTION</label>
    <select id="circonscription-select" v-model="circonscription" class="my-select">
      <option v-for="circonscription in circonscriptions" :key="circonscription">{{circonscription}}</option>
    </select>
    <label for="discipline-select">DISCIPLINE</label>
    <select id="discipline-select" v-model="discipline" class="my-select">
      <option v-for="discipline in disciplines" :key="discipline.code">{{discipline.code}}: {{discipline.name}}</option>
    </select>
    <v-map ref="map" :zoom=13 :center="[50.6333, 3.0667]" style="width: 1024px; height: 800px;">
      <v-tilelayer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"></v-tilelayer>
      <v-marker v-for="mouv in mouvements" :lat-lng="[mouv.geo.lat, mouv.geo.lng]" v-bind:key="mouv['N\u00b0POSTE']"
      @l-add="$event.target.openPopup()">
        <v-popup :content="`POSTE ${mouv['N\u00b0POSTE']}<br>${yaml.dump(mouv).replace(/\ /g,'&nbsp;').replace(/(?:\r\n|\r|\n)/g, '<br>')}`"></v-popup>
      </v-marker>
    </v-map>
  </div>
</template>

<script>
export default {
  name: 'app',
  components: {
  },
  data () {
    return {
      yaml: require('js-yaml'),
      data_mouvements: require('@/assets/mouvements.json'),
      sigles: require('@/assets/sigles.json'),
      circonscriptions: require('@/assets/circonscriptions.json'),
      disciplines: require('@/assets/disciplines.json'),
      sigle: null,
      circonscription: null,
      discipline: null,
    }
  },
  mounted () {
    this.circonscriptions.sort(e => e.name)
    this.disciplines.sort()
    let disciplines_map = new Map(this.disciplines.map(i => [i.code, i.name]));
    for (let mouv of this.data_mouvements) {
      mouv.DISCIPLINE = {code: mouv.DISCIPLINE, name: disciplines_map.get(mouv.DISCIPLINE) }
    }
  },
  computed: {
    map_window () {
      return this.$refs.map
    },
    mouvements () {
      return this.data_mouvements
      .filter(m => m.geo && m.geo.lat && m.geo.lng)
      .filter(m => this.sigle ? m.SIGLE === this.sigle : true)
      .filter(m => this.circonscription ? m.CIRCONSCRIPTION === this.circonscription : true)
      .filter(m => this.discipline ? m.DISCIPLINE.code === this.discipline : true)
    },
    regroupements () {
      return require('@/assets/regroupements.json')
    }
  }
}
</script>

<style>
@import "~leaflet/dist/leaflet.css";
.my-select {
  max-width: 200px;
}
</style>
