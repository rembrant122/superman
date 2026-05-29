import type {StageType} from "./models/general";

export function getStartStageType(): StageType {
    const params = new URLSearchParams(window.location.search)
    const repeat = params.get('repeat')

    if (repeat === 'true') return 'REPEAT'
    if (repeat === 'false') return 'MEMORIZE'

    return 'REPEAT'
}