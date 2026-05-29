import {BaseCardModel, StageType} from "./general";
// api.ts

export type WordModelApi = BaseCardModel & {
  word: string
  translate: string
  transcription?: string | null
  context?: string | null//тематика
}

export type ListWordsModelApi = {
    // stage_type: StageType
    // REPEAT='REPEAT'
    // MEMORIZE='MEMORIZE'

  words: WordModelApi[]
}
export type ListWordsModelApiOutput = {
  words: BaseCardModel[]
}
export type ListWordsIdModel = {
  words_id: number[]
}
export type WordStudyState = {

  card: WordModelApi

  wordToTranslateResult:boolean | null     // слово -> перевод true=успешно вспомнен
  translateToWordResult: boolean | null      // перевод -> слово

  isRepeatResultSent: boolean| null //уже отправлено инфо о состоянии

}
export enum StudyState {
  LOADING = 'LOADING',
  STUDY = 'STUDY',
  NO_WORDS = 'NO_WORDS',
  ASK_NEW_WORDS = 'ASK_NEW_WORDS',//ЗАПРОС НУЖНО ЛИ ЕЩЁ СЛОВА ДЛЛЯ ЗАПОМНН
  ERROR='ERROR'
}

export type WordStudySession = {

  toTranslateWord:boolean//если да -> то анг-ру

  cards: WordStudyState[]
  currentCard: WordStudyState | null // карточка сейчас показываемая
  // isFinished: boolean

  timesShown?:number|null //если стадия запомниания - то тут устанавливаем сколько раз уже была показана
  stageType: StageType|null

  isShownBack:boolean|null//если true то показывается целиковая карточка

  state: StudyState

}
