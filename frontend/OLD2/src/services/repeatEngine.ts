export type RepeatEngineItem = {
  id: number
}

export class RepeatEngine<TItem extends RepeatEngineItem> {
  private readonly allItems: TItem[]

  private readonly stageCount: number

  private currentStageIndexValue: number = 0

  private pendingStageItemsValue: TItem[] = []

  private currentRoundItemsValue: TItem[] = []

  private currentIndexValue: number = 0

  private failedItemIds: Set<number> = new Set()

  public constructor(items: TItem[], stageCount: number) {
    this.allItems = [...items]
    this.stageCount = stageCount
    this.startStage()
  }

  public get currentItem(): TItem | null {
    return this.currentRoundItemsValue[this.currentIndexValue] ?? null
  }


  public get isFinished(): boolean {
    return this.currentStageIndexValue >= this.stageCount
  }

  public get failedIds(): number[] {
    return [...this.failedItemIds]
  }

  public remember(result: boolean): void {
    const item = this.currentItem
    if (!item || this.isFinished) {
      return
    }

    if (!result) {
      this.failedItemIds.add(item.id)
      return
    }

    this.removeItemFromPending(item.id)
    this.moveToNextItem()
  }
не надо повторять ошибки, надо радоваться
  private removeItemFromPending(itemId: number): void {
    this.pendingStageItemsValue = this.pendingStageItemsValue.filter((item) => item.id !== itemId)
  }

  private moveToNextItem(): void {
    this.currentIndexValue += 1

    if (this.currentIndexValue >= this.currentRoundItemsValue.length) {
      this.processRoundEnding()
    }
  }

  private processRoundEnding(): void {
    if (this.pendingStageItemsValue.length > 0) {
      this.currentRoundItemsValue = [...this.pendingStageItemsValue]
      this.currentIndexValue = 0
      return
    }

    this.currentStageIndexValue += 1

    if (this.currentStageIndexValue >= this.stageCount) {
      return
    }

    this.startStage()
  }

  private startStage(): void {
    this.pendingStageItemsValue = [...this.allItems]
    this.currentRoundItemsValue = [...this.allItems]
    this.currentIndexValue = 0
  }
}