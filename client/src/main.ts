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
import '@mdi/font/css/materialdesignicons.css';
import './assets/main.css';
import './assets/responsive.css';

// light theme - grey primary for selections
const lightTheme = {
  dark: false,
  colors: {
    background: '#f4f7f9',
    surface: '#ffffff',
    primary: '#666666', // grey for list item selections
  }
}

// dark theme - darker grey primary for selections
const darkTheme = {
  dark: true,
  colors: {
    background: '#1a1a1a',
    surface: '#252525',
    primary: '#555555', // darker grey for list item selections
  }
}

// apply saved theme preference logic
const savedTheme = localStorage.getItem('user-theme');
let initialTheme = 'light';

if (savedTheme === 'dark') {
  initialTheme = 'dark';
  document.body.classList.add('theme--dark');
} else if (!savedTheme && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
  initialTheme = 'dark';
  document.body.classList.add('theme--dark');
}

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: initialTheme,
    themes: {
      light: lightTheme,
      dark: darkTheme
    }
  }
});

const app = createApp(App);

app.use(createPinia());
app.use(router);
app.use(Toast);
app.use(vuetify);
app.mount('#app');
