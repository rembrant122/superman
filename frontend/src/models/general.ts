export type BaseCardModel = {
  id: number
  //
  // title: string
  // text?: string | null
  // imageUrl?: string | null
  // description?: string | null

}

export type CardListModel = {
  cards: BaseCardModel[]
}

export type WordDirection = 'word_to_translate' | 'translate_to_word'
export type AuthToken = string
export type StageType = 'REPEAT' | 'MEMORIZE'
