/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1763078910")

  // add field
  collection.fields.addAt(2, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text2883930230",
    "max": 0,
    "min": 0,
    "name": "charity_name_chi",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // add field
  collection.fields.addAt(9, new Field({
    "hidden": false,
    "id": "json2030490945",
    "maxSize": 0,
    "name": "risk",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1763078910")

  // remove field
  collection.fields.removeById("text2883930230")

  // remove field
  collection.fields.removeById("json2030490945")

  return app.save(collection)
})
