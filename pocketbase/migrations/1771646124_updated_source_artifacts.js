/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_2034649627")

  // add field
  collection.fields.addAt(4, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text3060840465",
    "max": 0,
    "min": 0,
    "name": "gemini_file_uri",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // add field
  collection.fields.addAt(5, new Field({
    "hidden": false,
    "id": "date3878414091",
    "max": "",
    "min": "",
    "name": "gemini_file_uploaded",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "date"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_2034649627")

  // remove field
  collection.fields.removeById("text3060840465")

  // remove field
  collection.fields.removeById("date3878414091")

  return app.save(collection)
})
