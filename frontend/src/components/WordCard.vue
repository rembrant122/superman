<template>
  <div class="study-card">
    <!-- загрузка -->
    <div v-if="session.state === StudyState.LOADING" class="study-card__main-text">
      Загрузка...
    </div>

    <!-- слов нет -->
    <div v-else-if="session.state === StudyState.NO_WORDS" class="study-card__main-text">
      Слов нет
    </div>

    <!-- слова закончились, можно подгрузить ещё -->
    <template v-else-if="session.state === StudyState.ASK_NEW_WORDS">
      <div class="study-card__main-text">
        Слова закончились
      </div>

      <div class="study-card__buttons">
        <button class="study-card__button" :disabled="isProcessing" @click="runAction(() => loadNew())">
          Подгрузить ещё
        </button>
      </div>
    </template>

    <!-- карточка -->
    <template v-else>
      <div class="study-card__main-text">
        {{ mainText }}
      </div>

      <div v-if="session.isShownBack" class="study-card__answer-block">
        <div v-if="currentWord?.word" class="study-card__answer-word">
          {{ currentWord.word }}
        </div>

        <div v-if="currentWord?.translate" class="study-card__answer-translate">
          {{ currentWord.translate }}
        </div>

        <div v-if="currentWord?.transcription" class="study-card__answer-transcription">
          {{ currentWord.transcription }}
        </div>

        <div v-if="currentWord?.context" class="study-card__answer-context">
          {{ currentWord.context }}
        </div>
      </div>

      <div v-if="!session.isShownBack" class="study-card__buttons">
        <button class="study-card__button" :disabled="isProcessing" @click="runAction(() => resultWord(true))">
          Помню
        </button>

        <button class="study-card__button" :disabled="isProcessing" @click="runAction(() => resultWord(false))">
          Не помню
        </button>
      </div>

      <div v-else class="study-card__buttons">
        <button class="study-card__button" :disabled="isProcessing" @click="runAction(setNextWord)">
          Дальше
        </button>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import '../styles/WordCard.css'

import {computed, ref} from 'vue'
import { StudyState } from '../models/words'

import {
  loadNew,
  resultWord,
  setNextWord,
  wordStudySession,
} from '../services/cardsManger'

const isProcessing = ref(false)

async function runAction(action: () => Promise<unknown>): Promise<void> {
  if (isProcessing.value) return

  isProcessing.value = true

  try {
    await action()
  } finally {
    isProcessing.value = false
  }
}

const session =  wordStudySession

const currentWord = computed(() => session.value.currentCard?.card ?? null)

const mainText = computed((): string => {
  const word = currentWord.value
  if (!word) return ''

  if (session.value.toTranslateWord)
    return word.word
    return word.translate

})

</script>