/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1763078910")

  // add field
  collection.fields.addAt(10, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text3850079453",
    "max": 0,
    "min": 0,
    "name": "gemini_cache_name",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // add field
  collection.fields.addAt(11, new Field({
    "hidden": false,
    "id": "date3810514494",
    "max": "",
    "min": "",
    "name": "gemini_cached",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "date"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1763078910")

  // remove field
  collection.fields.removeById("text3850079453")

  // remove field
  collection.fields.removeById("date3810514494")

  return app.save(collection)
})
