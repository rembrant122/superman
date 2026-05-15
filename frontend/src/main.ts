import { createApp } from 'vue'
import './styles/App.css'
import {saveTokenFromUrl} from "./api";
import App from "./App.vue";

saveTokenFromUrl()

createApp(App).mount('#app')//запуск прилы.