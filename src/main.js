import Vue from 'vue'
import App from './App.vue'
import {LMap, LTileLayer, LMarker, LPopup } from 'vue2-leaflet';
import L from 'leaflet';
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
});

Vue.config.productionTip = false

Vue.component('v-map', LMap);
Vue.component('v-tilelayer', LTileLayer);
Vue.component('v-marker', LMarker);
Vue.component('v-popup', LPopup);

new Vue({
  render: h => h(App)
}).$mount('#app')
