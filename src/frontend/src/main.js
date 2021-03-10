import { createApp } from 'vue';

import App from './App.vue';
import Birthday from './components/Birthday.vue';
import NewBirthday from './components/NewBirthday.vue';

const app = createApp(App);

app.component('birthday', Birthday);
app.component('new-birthday', NewBirthday);

app.mount('#app');
