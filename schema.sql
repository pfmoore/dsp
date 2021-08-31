CREATE TABLE items (
    id,
    name, -- Title-Cased vs. what's in the game.
    type, -- The category of the item, not the full story for buildings
    grid_index, -- Where this appears in the item grid. The format is ZXXY,
               --  where Z is 1 for components and 2 for buildings. Note that
               --  this has the same format as the grid_index for recipes, but
               --  different values - recipe grid_index is used with the
               --  replicator, while item grid_index is used with filters (for
               --  example).
    stack_size,
    can_build, -- Mostly equivalent to "is_building?", except also true for
                --Foundation.
    build_index, -- Where this appears in the build shortcut menus, in the form
                  --ZXX, where Z is the top-level and XX is the inner level.
    is_fluid, -- boolean, omitted when false.
    energy, -- This is measured in Joules.
    fuel_chamber_boost, -- This is a floating-point number, so 1.0 corresponds
                        -- to a +100% boost.
    unlock_key, -- The item ID of an item that is used to determine the tech
                -- unlock requirements of this item. For instance,
                 --Accumulator(Full) is unlocked whenever Accumulator is,
                 --without it being explicitly stated in the tech tree.
    explicit_tech_dep, -- The explicit tech dependency of this item, for display
                        --purposes.
    mining_from, -- A free-text string that sometimes includes colored spans.
    explicit_produce_from, -- A text string that should name an item. Used for
                            --items that are produced without conventional recipes.
    description, -- The in-game tooltip text. May include colored spans.
    disabled, -- If true, this item won't show up in the item grid. Set for
              -- items that are in the game data, but not accessible yet.
    image -- Included as a comment only, this is the name of the item image
           -- as stored in the game files. It should be renamed to the item's
            --name when uploaded.
);

CREATE TABLE recipes (
    id,
    name, -- Title-Cased vs. what's in the game.
    type, -- The type of building that makes the recipe
    -- outputs, -- What the recipe produces. This is an alternating array of
             -- "item_id, count, item_id, count, ..." As a result, there will
             -- always be an even number of elements.
    -- inputs, -- What the recipe requires. Same format as outputs.
    grid_index, -- Where this appears in the recipe grid. The format is ZXXY,
                -- where Z is 1 for components and 2 for buildings. Note that
                -- this has the same format as the grid_index for items, but
                -- different values - recipe grid_index is used with the
                -- replicator, while item grid_index is used with filters (for
                -- example).
    handcraft, -- Can it be made in the replicator?
    seconds, -- How long to craft at 1x speed.
    explicit, -- Whether this is an "explicit" recipe, as opposed to the
               -- implicit or "primary" recipe for an item. You can tell the
               -- difference in-game because hovering over an explicit recipe
               -- shows "(Recipe)" in front of the name, and there's other
               -- differences in the tooltip.
    description, -- The in-game tooltip text. May include colored spans.
                --  Generally only present (and used) for explicit recipes.
    disabled, -- If true, this item won't show up in the item grid. Set for
              -- items that are in the game data, but not accessible yet.
    image -- Included as a comment only, this is the name of the item image
           -- as stored in the game files. It should be renamed to the item's
           -- name when uploaded. Generally only present for explicit recipes.
);

CREATE TABLE recipe_outputs (
    id,
    item_id,
    count
);

CREATE TABLE recipe_inputs (
    id,
    item_id,
    count
);