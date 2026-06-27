<template>
  <!-- подгрузка модуля слов-->
  <main class="app">
    <WordCard />
  </main>
</template>

<script setup lang="ts">
import {onMounted} from 'vue'

import WordCard from './components/WordCard.vue'

import {loadNew, wordStudySession,} from './services/cardsManger'

import {getStartStageType} from "./getStartStageType";
import {StudyState} from "@/models/StudyState";

//запуск прилы
onMounted(async (): Promise<void> => {
  console.log('Приложение запущено')
  wordStudySession.value.stageType = getStartStageType() // определяем что делаем
  console.log('Тип режима:', wordStudySession.value.stageType)

  await loadNew() // загрузка слов и показ

})
</script>
