import { createApp } from 'vue'
import './styles/App.css'
import {saveTokenFromUrl} from "./api";
import App from "./AppWords.vue";
import AppWords from "./AppWords.vue";

saveTokenFromUrl()

const app = new URLSearchParams(window.location.search).get('app')

switch (app) {
  case 'skills':
    createApp(AppSkills).mount('#app')
    break

  case 'words':
    createApp(AppWords).mount('#app')
    break

  default:
    createApp(AppZoar).mount('#app')
}
