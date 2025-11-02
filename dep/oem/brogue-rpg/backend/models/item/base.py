from vmath import vec2i

from backend.models.affix import AffixGroup
from backend.models.expr import Expr
from backend.models.effect import Effect
from backend.i18n import String

class ItemAction:
    def __init__(self, name: String, effect: Effect):
        self.name = name
        self.effect = effect

    def __call__(self, user, item: 'Item'):
        context: dict = item.environ.copy()
        context['user'] = user
        context['item'] = item
        return self.effect(context)

class Item:
    def __init__(
            self,
            name: String | None = None,
            icon: str | None = None,
            desc: String | None = None,
            actions: dict[String, Effect] | None = None,
            environ: dict[str, object] | None = None,
            durability: vec2i | None = None,
            quantity: int = 1):
        
        assert name is not None
        self.name = name
        self.icon = icon
        self.desc = desc

        self.actions: list[ItemAction] = []
        if actions is not None:
            for k, v in actions.items():
                self.actions.append(ItemAction(k, v))

        self.environ = {} if environ is None else environ
        self.durability = durability
        self.quantity = quantity
    
    def render_desc(self) -> str:
        if self.desc is None:
            return ''
        kv = {}
        for k, v in self.environ.items():
            if isinstance(v, Expr):
                v = v(self.environ)
            kv[k] = v
        return str(self.desc).format(**kv)

    def get_actions(self):
        return self.actions.copy()


class EquippableItem(Item):
    def __init__(
            self,
            name: String | None = None,
            icon: str | None = None,
            desc: String | None = None,
            actions: dict[String, Effect] | None = None,
            environ: dict[str, object] | None = None,
            durability: vec2i | None = None,
            quantity: int = 1,
            modifiers: dict[str, object] | None = None,
            triggers: dict[str, Effect] | None = None):
        super().__init__(
            name,
            icon,
            desc,
            actions,
            environ,
            durability,
            quantity)
        self.is_equipped = False
        self.affixes = AffixGroup.from_config(modifiers, triggers)

    def get_actions(self):
        actions = self.actions.copy()
        if self.is_equipped:
            actions.insert(0, action_unequip()) # type: ignore
        else:
            actions.insert(0, action_equip())   # type: ignore
        return actions

# class ChooseGearSlot(Task):
#     def __init__(self, output: str = 'slot'):
#         self.output = output

#     def call_async(self, context: dict):
#         from backend.schema.inventory import GearSlot
#         game = current_game()
#         game.message("Choose a gear slot to equip")
#         filter = lambda slot: (isinstance(slot, GearSlot) and slot.item is None)
#         slot = yield from game.io.choose_item_slot(filter)
#         context[self.output] = slot
#         return 0


# def action_equip():
#     def extra_step(ctx):
#         from backend.schema.inventory import GearSlot

#         slot: GearSlot | None = ctx["slot"]
#         if slot is None:
#             raise TaskInterrupt("No slot selected")
        
#         inventory = current_game().hero.inventory
#         item: Item = ctx[Item.CTX_ITEM]
#         inventory.remove(item)
#         slot.item = item
#         slot.item.is_equipped = True

#         ctx[Item.CTX_USER].update_stats()

#     return ItemAction(ui.Equip, Task.pipeline([
#         ChooseGearSlot(output='slot'),
#         Task.callback(extra_step)
#     ]))


# def action_unequip():
#     def extra_step(ctx):
#         inventory = current_game().hero.inventory
#         item: Item = ctx[Item.CTX_ITEM]
#         item_slot = inventory.first_empty_slot()
#         if item_slot is None:
#             raise TaskInterrupt("No empty slot")
#         inventory.remove(item)
#         item_slot.item = item
#         item.is_equipped = False

#         ctx[Item.CTX_USER].update_stats()

#     return ItemAction(ui.Unequip, Task.callback(extra_step))
