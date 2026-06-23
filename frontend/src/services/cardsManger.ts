/*

  помечаем результат:

    если toTranslateWord:ы
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
import {ListWordsIdModel, StudyState} from '../models/words'

import type {BaseCardModel, StageType} from '../models/general'
import type {
  ListWordsModelApi,
  WordModelApi,
  WordStudySession,
  WordStudyState,
} from '../models/words'
import {shuffleArray} from "./shuffleArray";

export const wordStudySession = ref<WordStudySession>({
  toTranslateWord: false,
  cards: [],
  currentCard: null,
  timesShown: null,
  stageType: null,
  isShownBack: false,
  state: StudyState.LOADING,
})

function getLoadUrl(stageType: StageType): string {

  console.log('stageType:', stageType)
  const url = stageType === 'REPEAT'
    ? '/get_list_words_for_repeat'
    : '/get_list_words_for_memorize'

  console.log('url:', url)

  return url
}

function createWordState(word: WordModelApi): WordStudyState {

  const wordStudyState = {
    card: word,
    wordToTranslateResult: null,
    translateToWordResult: null,
    isRepeatResultSent: false,
  }
  // console.log('сформирована карточка WordStudyState:', wordStudyState)
  return wordStudyState
}

function resetCardsResult(): void {

  wordStudySession.value.cards.forEach((word: WordStudyState): void => {
    word.wordToTranslateResult = null
    word.translateToWordResult = null
  })

  console.log('Объекты карточек установлен в изначальное состояние')
}

export async function sendRepeatResult(wordId: number,result:boolean): Promise<void> {
  console.log('Отправка результата слова')
  await request({
    url: '/save_result_repeat_word',
    method: 'POST',
    body: { id_word: wordId, result: result },
  })
}

export function getNextCard(): WordStudyState | null {

  const session = wordStudySession.value
  session.cards = shuffleArray(session.cards)

  const card = session.cards.find((word: WordStudyState): boolean => {
    if (session.toTranslateWord) {
      //анг-ру
      return word.wordToTranslateResult !== true
    }

    return word.translateToWordResult !== true
  })

  console.log('загрузка новой карточки: ',card)

  return card ?? null
}

export async function loadNew(): Promise<boolean> {
  console.log('Начинаем загрузку списка карточек...')
  const session = wordStudySession.value

  session.state = StudyState.LOADING
  session.isShownBack = false
  session.toTranslateWord = true
  session.currentCard = null

  const listWords: ListWordsModelApi = await request({
    url: getLoadUrl(session.stageType),
    method: 'GET',
  })

  // session.stageType = listWords.stage_type
  session.cards = listWords.words.map(createWordState)

  const stageType=session.stageType


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
      console.log('слов нет!')

    return false
  }

  console.log('session:',session)
  console.log('Слова загружены')

  session.currentCard = getNextCard()
  session.state = StudyState.STUDY


  return true
}

async function listCardsFinish(): Promise<void> {

  const session = wordStudySession.value
  console.log('Список карточек закончился (в одну сторону)! session:',session)

  // в любом случае
  if (session.toTranslateWord) {
    console.log('Переворачиваем карточки')
    session.toTranslateWord = false
    await setNextWord()
    return
  }

  //запомин
  if (session.stageType === 'MEMORIZE') {
    if ((session.timesShown ?? 0) >= 3) {
      console.log('session.timesShown: ',session.timesShown)
      await sendMemorResult()

      session.state = StudyState.ASK_NEW_WORDS //здесь мы не ставим сразу на загржку новых, тк нужно нажжать кнопку подтвреждениея
      console.log('Установили состояние ASK_NEW_WORDS (для запроса)')
      return
    }
    session.timesShown = (session.timesShown ?? 0) + 1
    console.log('session.timesShown: ',session.timesShown)

    session.toTranslateWord = true
    resetCardsResult()
    await setNextWord()
    return
  }

  // повторение
  const newWords = await loadNew()

  if (!newWords) {
    session.state = StudyState.NO_WORDS
    console.log('Установили состояние NO_WORDS')

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
export async function sendMemorResult(): Promise<void> {

      // сохран результата
      const data: ListWordsIdModel = {words_id: wordStudySession.value.cards.map
        (word => word.card.id),}

      console.log('Отправка на бек что запомнили: ',data)

      await request({
        url: '/save_result_memorize',
        method: 'POST',
        body: data,
      })
}
export async function resultWord(result: boolean): Promise<void> {
  console.log('результат ответа слова:', result)

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

    if (session.stageType === 'REPEAT' && wordState.isRepeatResultSent !== true) {
      console.log('Не вспомнил')
      wordState.isRepeatResultSent = true
      await sendRepeatResult(wordState.card.id,false)

    }
    return
  }

  // если вспомнил
  else{
    // #ставим на след стадию:
  if (session.stageType === 'REPEAT' && session.toTranslateWord == false && wordState.isRepeatResultSent !== true)
  {
    await sendRepeatResult(wordState.card.id,true)
    wordState.isRepeatResultSent = true
  }
  await setNextWord()}}
