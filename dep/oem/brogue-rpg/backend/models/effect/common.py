from .base import Effect

class DeleteItem(Effect):
    def __call__(self, context: dict):
        item = context['item']
        current_game().hero.inventory.remove(item)
