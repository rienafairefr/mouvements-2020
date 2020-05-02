<template>
  <div class="container">
    <div v-if="!loaded">
      Loading...
    </div>
    <div v-else>
      <div class="row">
        <label class="form-control-label" for="sigle-select">SIGLE</label>
        <select class="form-control" id="sigle-select" v-model="sigle">
          <option :value="undefined">--ALL--</option>
          <option v-for="sigle in sigles" :key="sigle">{{sigle}}</option>
        </select>
      </div>
      <div class="row">
        <label for="nbVacants-select">nbVacants</label>
        <select id="nbVacants-select" v-model="nbVacants" class="my-select">
          <option :value="undefined">--ALL--</option>
          <option v-for="nbVacants in nbVacantsValues" :key="nbVacants" :value="nbVacants">{{nbVacants}}</option>
        </select>
      </div>
      <div class="row">
        <label for="circonscription-select">CIRCONSCRIPTION</label>
        <select id="circonscription-select" v-model="circonscription" class="my-select">
          <option :value="undefined">--ALL--</option>
          <option v-for="circonscription in circonscriptions" :key="circonscription">{{circonscription}}</option>
        </select>
      </div>
      <div class="row">
        <label for="discipline-select">DISCIPLINE</label>
        <select id="discipline-select" v-model="discipline" class="my-select">
          <option :value="undefined">--ALL--</option>
          <option v-for="discipline in disciplines" :key="discipline.code" :value="discipline.code">{{discipline.code}}: {{discipline.name}}</option>
        </select>
      </div>
      <div class="row">
        <label for="regroupement-select">REGROUPEMENT</label>
        <select id="regroupement-select" v-model="regroupement" class="my-select">
          <option :value="undefined">--ALL--</option>
          <option v-for="regroupement in regroupements" :key="regroupement.name" :value="regroupement.name">{{regroupement.name}}</option>
        </select>
      </div>
      <div class="row">
        <label for="support-select">SUPPORT</label>
        <select id="support-select" v-model="support" class="my-select">
          <option :value="undefined">--ALL--</option>
          <option v-for="support in supports" :key="support.code" :value="support.code">{{support.code}}: {{support.name}}</option>
        </select>
      </div>
      <div class="row">
        <label for="observation-select">OBSERVATIONS</label>
        <select id="observation-select" v-model="observations" class="my-select">
          <option :value="undefined">--ALL--</option>
          <option v-for="observations in observationsValues" :key="observations" :value="observations">{{observations}}</option>
        </select>
      </div>
      <v-map ref="map" class="row" :zoom=13 :center="[50.6333, 3.0667]" style="width: 800px; height: 500px;"
             @update:zoom="update"
             @update:center="update"
             @update:bounds="update">
        <v-tilelayer url="http://{s}.tile.osm.org/{z}/{x}/{y}.png"></v-tilelayer>
        <v-marker v-for="mouv in geo_mouvements" :lat-lng="[mouv.geo.lat, mouv.geo.lng]" v-bind:key="mouv[numPoste]"
        @l-add="$event.target.openPopup()">
          <v-popup :content="`POSTE ${mouv[numPoste]}<br>${yaml.dump(mouv).replace(/\ /g,'&nbsp;').replace(/(?:\r\n|\r|\n)/g, '<br>')}`"></v-popup>
        </v-marker>
      </v-map>
      <table class="table row">
        <thead>
          <tr>
            <th scope="col" v-for="header in headers" v-bind:key="header">{{header}}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="mouvement in filtered_mouvements" v-bind:key="mouvement[numPoste]">
            <td v-for="header in headers" v-bind:key="header">{{mouvement[header]}}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'app',
  data () {
    return {
      yaml: require('js-yaml'),
      mouvements: [],
      regroupements: [],
      disciplines: [],
      supports: [],
      vacants: "Nb Postes Vacants",
      numPoste: "'N\u{00b0}POSTE'",
      nbVacants: undefined,
      sigle: undefined,
      regroupement: undefined,
      circonscription: undefined,
      discipline: undefined,
      support: undefined,
      observations: undefined,
      bounds: {},
      loaded: false,
      discipline_map: {},
      regroupement_map: new Map(),
    }
  },
  mounted () {
    this.fetchData()
  },
  computed: {
    headers () {
      return Object.keys(this.mouvements[0])
    },
    observationsValues () {
      return [... new Set(this.mouvements.map(mouv => mouv.OBSERVATIONS))];
    },
    nbVacantsValues () {
      return [... new Set(this.mouvements.map(mouv => mouv.nbVacants))].sort();
    },
    sigles () {
      return [... new Set(this.mouvements.map(mouv => mouv.SIGLE))].sort();
    },
    circonscriptions () {
      return [... new Set(this.mouvements.map(mouv => mouv.CIRCONSCRIPTION))].sort()
    },
    geo_mouvements () {
      return this.filtered_mouvements
      .filter(m => m.geo && m.geo.lat && m.geo.lng && this.inBounds(m))
    },
    filtered_mouvements () {
      return this.mouvements
        .filter(m => this.sigle? m.SIGLE === this.sigle : true)
        .filter(m => this.circonscription ? m.CIRCONSCRIPTION === this.circonscription : true)
        .filter(m => this.observations ? m.OBSERVATIONS === this.observations : true)
        .filter(m => this.discipline ? m.DISCIPLINE === this.discipline : true)
        .filter(m => this.regroupement ? m.REGROUPEMENT === this.regroupement : true)
        .filter(m => this.nbVacants ? m[this.vacants] === this.nbVacants : true)
        .filter(m => this.support ? m.SUPPORT === this.support : true)
    }
  },
  methods: {
    inBounds (m) {
      return this.bounds && 
      (this.bounds.southWest ? m.geo.lat >= this.bounds.southWest.lat && m.geo.lat <= this.bounds.northEast.lat : true) &&
      (this.bounds.northEast ? m.geo.lng >= this.bounds.southWest.lng && m.geo.lng <= this.bounds.northEast.lat : true)
    },
    fetch (name) {
      return axios.get(`/json/${name}.json`).then(response => {
        this[name] = response.data
      })
    },
    async fetchData() {
      await Promise.all([
        this.fetch('mouvements'),
        this.fetch('regroupements'),
        this.fetch('disciplines'),
        this.fetch('supports')
      ])
      this.disciplines_map = new Map(this.disciplines.map(i => [i.code, i.name]));
      this.regroupements.forEach(i => i.cities.forEach( c => { this.regroupement_map.set(c, i.name)}))

      for (var i = 0; i < this.mouvements.length; i++) {
        this.mouvements[i].REGROUPEMENT = this.regroupement_map.get(this.mouvements[i].COMMUNE)
      }
      this.loaded = true
    },
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
