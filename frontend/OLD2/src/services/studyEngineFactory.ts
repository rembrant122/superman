import { RepeatEngine } from './repeatEngine'
import type { QueryParamsModel, StudyItem } from '../models/study'

export function createStudyEngine(
  params: QueryParamsModel,
  items: StudyItem[],
): RepeatEngine<StudyItem> {
  const stageCount = params.repeat ? 1 : 3
  return new RepeatEngine(items, stageCount)
} потому что я хорошая