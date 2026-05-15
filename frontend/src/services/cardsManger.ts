/*

  помечаем результат:

    если toTranslateWord:
      то  wordToTranslateResult=true
    else:
      wordToTranslateResult=True

  не вспомнил:
    если повторение:
      если isRepeatResultSent=False - то поменять на труе, а также отправить сообщение об этом на бек

  кончислся список:

    если toTranslateWord=True
      toTranslateWord = False
    else:
      если заопмниенание:
        если times_shown<2
          times_shown+1
        иначе:
          вызов функц конец запомниния
      если повторение:
        то вызов функции конец повторерения

повторение:
*/

import { ref } from 'vue'
import { request } from '../api'
import { StudyState } from '../models/words'

import type { StageType } from '../models/general'
import type {
  ListWordsModelApi,
  WordModelApi,
  WordStudySession,
  WordStudyState,
} from '../models/words'

export const wordStudySession = ref<WordStudySession>({
  toTranslateWord: false,
  cards: [],
  currentCard: null,
  timesShown: null,
  stage_type: null,
  isShownBack: false,
  state: StudyState.LOADING,
})

function getLoadUrl(stageType: StageType): string {
  if (stageType === 'REPEAT') return '/get_list_words_for_repeat'
  return '/get_list_words_for_memorize'
}

function createWordState(word: WordModelApi): WordStudyState {
  return {
    card: word,
    wordToTranslateResult: null,
    translateToWordResult: null,
    isRepeatResultSent: false,
  }
}

function resetCardsResult(): void {
  const session = wordStudySession.value

  session.cards.forEach((word: WordStudyState): void => {
    word.wordToTranslateResult = null
    word.translateToWordResult = null
  })
}

export async function sendRepeatResult(wordId: number): Promise<void> {
  await request({
    url: '/save_result_repeat_word',
    method: 'POST',
    body: { id_word: wordId },
  })
}

export function getNextCard(): WordStudyState | null {
  const session = wordStudySession.value

  const card = session.cards.find((word: WordStudyState): boolean => {
    if (session.toTranslateWord) {
      //анг-ру
      return word.wordToTranslateResult !== true
    }

    return word.translateToWordResult !== true
  })

  return card ?? null
}

export async function loadNew(stageType: StageType): Promise<boolean> {
  const session = wordStudySession.value

  session.state = StudyState.LOADING
  session.isShownBack = false
  session.toTranslateWord = true
  session.currentCard = null

  const listWords: ListWordsModelApi = await request({
    url: getLoadUrl(stageType),
    method: 'GET',
  })

  session.stage_type = listWords.stage_type
  session.cards = listWords.words.map(createWordState)

  if (stageType === 'MEMORIZE') {
    session.timesShown = 0
  } else {
    session.timesShown = null
  }

  // NO_WORDS
  if (session.cards.length === 0) {
    if (stageType === 'REPEAT') {
      session.state = StudyState.NO_WORDS
    } else {
      session.state = StudyState.ASK_NEW_WORDS
    }

    return false
  }

  session.currentCard = getNextCard()
  session.state = StudyState.STUDY

  return true
}

async function listCardsFinish(): Promise<void> {
  const session = wordStudySession.value

  // в любом случае
  if (session.toTranslateWord) {
    session.toTranslateWord = false
    await setNextWord()
    return
  }

  //запомин
  if (session.stage_type === 'MEMORIZE') {
    if ((session.timesShown ?? 0) >= 2) {
      session.state = StudyState.ASK_NEW_WORDS //здесь мы не ставим сразу на загржку новых, тк нужно нажжать кнопку подтвреждениея
      return
    }

    session.timesShown = (session.timesShown ?? 0) + 1
    session.toTranslateWord = true
    resetCardsResult()
    await setNextWord()
    return
  }

  // повторение
  const newWords = await loadNew('REPEAT')

  if (!newWords) {
    session.state = StudyState.NO_WORDS
  }
}

export async function setNextWord(): Promise<void> {
  const session = wordStudySession.value

  session.isShownBack = false

  const nextCard = getNextCard()

  if (nextCard !== null) {
    session.currentCard = nextCard
    session.state = StudyState.STUDY
    return
  }

  // конился список
  await listCardsFinish()
}

export async function resultWord(result: boolean): Promise<void> {
  const session = wordStudySession.value
  const wordState = session.currentCard

  // if (!wordState) return
  if (wordState === null) return

  // помечаем результат
  if (session.toTranslateWord) {
    wordState.wordToTranslateResult = result
  } else {
    wordState.translateToWordResult = result
  }

  // если не вспомнил
  if (!result) {
    session.isShownBack = true

    if (session.stage_type === 'REPEAT' && wordState.isRepeatResultSent !== true) {
      wordState.isRepeatResultSent = true
      await sendRepeatResult(wordState.card.id)
    }
  }
}