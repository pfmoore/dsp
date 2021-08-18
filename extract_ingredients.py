import lupa
from lupa import LuaRuntime
from pathlib import Path
from collections import defaultdict, Counter

lua = LuaRuntime(unpack_returned_tuples=True)

def pairs(it):
    it = iter(it)
    return dict(zip(it, it))

data = lua.execute(Path("recipe_data.lua").read_text(encoding="utf-8"))

lua_items = data["game_items"]
lua_recipes = data["game_recipes"]

items = {id: val["name"] for id, val in lua_items.items()}

class Recipe:
    def __init__(self, id, lua_recipe):
        self.name = lua_recipe["name"]
        self.id = id
        self.inputs = pairs(lua_recipe["inputs"].values())
        self.outputs = pairs(lua_recipe["outputs"].values())
        self.lua_recipe = lua_recipe
    def print(self):
        i = ", ".join(f"{items[it]} ({n})" for (it, n) in self.inputs.items())
        o = ", ".join(f"{items[it]} ({n})" for (it, n) in self.outputs.items())
        return f"{self.name}: {o} <- {i}"
    def is_simple(self):
        return len(self.outputs) == 1
    def target(self):
        if self.is_simple():
            return list(self.outputs)[0]
        return None

recipes = {id: Recipe(id, val) for id, val in lua_recipes.items()}

item_recipes = defaultdict(list)
for r in recipes.values():
    target = r.target()
    if target:
        item_recipes[target].append(r)
simple_recipes = {target: recipes[0] for target, recipes in item_recipes.items() if len(recipes) == 1}

print(len(simple_recipes))
print(list(simple_recipes))
ingredients = Counter(i for r in simple_recipes.values() for i in r.inputs)
for i, n in ingredients.most_common():
    print(f"{items[i]}: {n}")