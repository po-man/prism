/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1763078910")

  // remove field
  collection.fields.removeById("json3039027576")

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1763078910")

  // add field
  collection.fields.addAt(11, new Field({
    "hidden": false,
    "id": "json3039027576",
    "maxSize": 0,
    "name": "audit_trail",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  return app.save(collection)
})
