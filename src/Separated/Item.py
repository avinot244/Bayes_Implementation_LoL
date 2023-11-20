class Item:
    def __init__(self,
                 itemId : int,
                 stackSize : int,
                 purchaseGameTime : int,
                 cooldownRemaining : float) -> None:
        self.itemId = itemId
        self.stackSize = stackSize
        self.purchaseGameTime = purchaseGameTime
        self.cooldownRemaining = cooldownRemaining
        