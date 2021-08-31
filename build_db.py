from lupa import LuaRuntime
from pathlib import Path
import sqlite3

lua = LuaRuntime(unpack_returned_tuples=True)

def pairs(it):
    it = iter(it)
    return zip(it, it)

ITEM_SQL = """\
    INSERT INTO items (
        id,
        name,
        type,
        grid_index,
        stack_size,
        can_build,
        build_index,
        is_fluid,
        energy,
        fuel_chamber_boost,
        unlock_key,
        explicit_tech_dep,
        mining_from,
        explicit_produce_from,
        description,
        disabled,
        image
    )
    VALUES (
        :id,
        :name,
        :type,
        :grid_index,
        :stack_size,
        :can_build,
        :build_index,
        :is_fluid,
        :energy,
        :fuel_chamber_boost,
        :unlock_key,
        :explicit_tech_dep,
        :mining_from,
        :explicit_produce_from,
        :description,
        :disabled,
        :image
    )
"""

RECIPE_SQL = """\
    INSERT INTO recipes (
        id,
        name,
        type,
        grid_index,
        handcraft,
        seconds,
        explicit,
        description,
        disabled,
        image
    )
    VALUES (
        :id,
        :name,
        :type,
        :grid_index,
        :handcraft,
        :seconds,
        :explicit,
        :description,
        :disabled,
        :image
    )
"""

RECIPE_INPUT_SQL = """\
    INSERT INTO recipe_inputs (
        id,
        item_id,
        count
    )
    VALUES (
        :id,
        :item_id,
        :count
    )
"""

RECIPE_OUTPUT_SQL = """\
    INSERT INTO recipe_outputs (
        id,
        item_id,
        count
    )
    VALUES (
        :id,
        :item_id,
        :count
    )
"""

def item_data(id, data):
    result = {"id": id}
    cols = (
        "name",
        "type",
        "grid_index",
        "stack_size",
        "can_build",
        "build_index",
        "is_fluid",
        "energy",
        "fuel_chamber_boost",
        "unlock_key",
        "explicit_tech_dep",
        "mining_from",
        "explicit_produce_from",
        "description",
        "disabled",
        "image",
    )
    for col in cols:
        result[col] = data[col]
    return result

def recipe_data(data):
    result = {"id": data["id"]}
    cols = (
        "name",
        "type",
        "grid_index",
        "handcraft",
        "seconds",
        "explicit",
        "description",
        "disabled",
        "image"
    )
    for col in cols:
        result[col] = data[col]
    return result

def recipe_inputs(data):
    id = data["id"]
    for item, count in pairs(data["inputs"].values()):
        yield {"id": id, "item_id": item, "count": count}

def recipe_outputs(data):
    id = data["id"]
    for item, count in pairs(data["outputs"].values()):
        yield {"id": id, "item_id": item, "count": count}

def import_data(data_file, db_file):
    data = lua.execute(Path(data_file).read_text(encoding="utf-8"))
    with sqlite3.connect(db_file) as db:
        db.executemany(
            ITEM_SQL,
            (
                item_data(id, val)
                for id, val in data["game_items"].items()
            )
        )
        db.executemany(
            RECIPE_SQL,
            (
                recipe_data(val)
                for val in data["game_recipes"].values()
            )
        )
        db.executemany(
            RECIPE_INPUT_SQL,
            (
                obj
                for val in data["game_recipes"].values()
                for obj in recipe_inputs(val)
            )
        )
        db.executemany(
            RECIPE_OUTPUT_SQL,
            (
                obj
                for val in data["game_recipes"].values()
                for obj in recipe_outputs(val)
            )
        )


if __name__ == "__main__":
    import sys
    data, db = sys.argv[1:]
    import_data(data, db)
