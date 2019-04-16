<template>
  <div>
    <label for="sigle-select">SIGLE</label>
    <select id="sigle-select" v-model="sigle" class="my-select">
      <option :value="undefined">--ALL--</option>
      <option v-for="sigle in sigles" :key="sigle">{{sigle}}</option>
    </select>
    <label for="circonscription-select">CIRCONSCRIPTION</label>
    <select id="circonscription-select" v-model="circonscription" class="my-select">
      <option :value="undefined">--ALL--</option>
      <option v-for="circonscription in circonscriptions" :key="circonscription">{{circonscription}}</option>
    </select>
    <label for="discipline-select">DISCIPLINE</label>
    <select id="discipline-select" v-model="discipline" class="my-select">
      <option :value="undefined">--ALL--</option>
      <option v-for="discipline in disciplines" :key="discipline.code" :value="discipline.code">{{discipline.code}}: {{discipline.name}}</option>
    </select>
    <label for="regroupement-select">REGROUPEMENT</label>
    <select id="regroupement-select" v-model="regroupement" class="my-select">
      <option :value="undefined">--ALL--</option>
      <option v-for="regroupement in regroupements" :key="regroupement.name" :value="regroupement.name">{{regroupement.name}}</option>
    </select>
    <label for="support-select">SUPPORT</label>
    <select id="support-select" v-model="support" class="my-select">
      <option :value="undefined">--ALL--</option>
      <option v-for="support in supports" :key="support.code" :value="support.code">{{support.code}}: {{support.name}}</option>
    </select>
    <v-map ref="map" :zoom=13 :center="[50.6333, 3.0667]" style="width: 1024px; height: 800px;"
           v-on:update:zoom="update" v-on:update:center="update" v-on:update:bounds="update">
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
      regroupements: require('@/assets/regroupements.json'),
      supports: require('@/assets/supports.json'),
      sigle: null,
      regroupement: null,
      circonscription: null,
      discipline: null,
      support: null,
      bounds: {},
    }
  },
  mounted () {
    this.update()
    this.circonscriptions.sort(e => e.name)
    this.disciplines.sort()
    let disciplines_map = new Map(this.disciplines.map(i => [i.code, i.name]));
    for (let mouv of this.data_mouvements) {
      mouv.DISCIPLINE = {code: mouv.DISCIPLINE, name: disciplines_map.get(mouv.DISCIPLINE) }
    }
    let regroupement_map = new Map()
    this.regroupements.forEach(i => i.cities.forEach( c => { regroupement_map.set(c, i.name)}))
    for (let mouv of this.data_mouvements) {
      mouv.REGROUPEMENT = regroupement_map.get(mouv.COMMUNE)
    }
  },
  computed: {
    mouvements () {
      return this.data_mouvements
        .filter(m => m.geo && m.geo.lat && m.geo.lng)
        .filter(m => this.bounds && this.bounds.southWest ? m.geo.lat >= this.bounds.southWest.lat && m.geo.lat <= this.bounds.northEast.lat : true)
        .filter(m => this.bounds && this.bounds.northEast ? m.geo.lng >= this.bounds.southWest.lng && m.geo.lng <= this.bounds.northEast.lat : true)
        .filter(m => this.sigle ? m.SIGLE === this.sigle : true)
        .filter(m => this.circonscription ? m.CIRCONSCRIPTION === this.circonscription : true)
        .filter(m => this.discipline ? m.DISCIPLINE.code === this.discipline : true)
        .filter(m => this.regroupement ? m.REGROUPEMENT === this.regroupement : true)
        .filter(m => this.support ? m.SUPPORT === this.support : true)
    }
  },
  methods: {
    update () {
      this.bounds = this.$refs.map.mapObject.getBounds()
    },
  }
}
</script>

<style>
@import "~leaflet/dist/leaflet.css";

.leaflet-fade-anim .leaflet-tile,.leaflet-zoom-anim .leaflet-zoom-animated { will-change:auto !important; }
.my-select {
  max-width: 200px;
}
</style>
