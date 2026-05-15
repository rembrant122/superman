<template>
  <!-- подгрузка модуля слов-->
  <main class="app">
    <WordCard />
  </main>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'

import WordCard from './components/WordCard.vue'

import { saveTokenFromUrl } from './api'

import {
  loadNew,
  wordStudySession,
} from './services/cardsManger'

import { StudyState } from './models/words'

import type { StageType } from './models/general'

function getStartStageType(): StageType {
  const params = new URLSearchParams(window.location.search)
  const repeat = params.get('repeat')

  if (repeat === 'true') return 'REPEAT'
  if (repeat === 'false') return 'MEMORIZE'

  return 'REPEAT'
}

//запуск прилы
onMounted(async (): Promise<void> => {
  try {
    saveTokenFromUrl()//сохр токен в локал сторидж

    const stageType = getStartStageType()//определяем что делаем (запомин, повтор)

    await loadNew(stageType)//загрузка слов и показ

  } catch (error) {//ошибка
    console.error(error)

    wordStudySession.value.state = StudyState.ERROR
  }
})
</script>
