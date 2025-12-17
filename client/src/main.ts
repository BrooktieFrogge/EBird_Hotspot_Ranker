import { createApp } from 'vue';
import App from './App.vue';
import router from './router';

import { createPinia } from 'pinia';

import Toast from 'vue-toastification';
import 'vue-toastification/dist/index.css';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

import { createVuetify } from 'vuetify';
import * as components from 'vuetify/components';
import * as directives from 'vuetify/directives';
import '@mdi/font/css/materialdesignicons.css'; // Import MDI CSS
import './assets/main.css';


const vuetify = createVuetify({
  components,
  directives
});

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(Toast);
app.use(vuetify);
app.mount('#app');
