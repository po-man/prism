/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1763078910")

  // add field
  collection.fields.addAt(10, new Field({
    "hidden": false,
    "id": "json3938641544",
    "maxSize": 0,
    "name": "analytics",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1763078910")

  // remove field
  collection.fields.removeById("json3938641544")

  return app.save(collection)
})
