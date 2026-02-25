/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = app.findCollectionByNameOrId("pbc_1763078910")

  // update collection data
  unmarshal({
    "indexes": [
      "CREATE UNIQUE INDEX `idx_LGBzfa1gnL` ON `organisations` (\n  `name`,\n  `analysis_batch_id`\n)"
    ]
  }, collection)

  // remove field
  collection.fields.removeById("text2883930230")

  // remove field
  collection.fields.removeById("text2398087059")

  // remove field
  collection.fields.removeById("json854162502")

  // remove field
  collection.fields.removeById("relation1507211071")

  // add field
  collection.fields.addAt(2, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text445106729",
    "max": 0,
    "min": 0,
    "name": "analysis_batch_id",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": false,
    "system": false,
    "type": "text"
  }))

  // update field
  collection.fields.addAt(1, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text284451158",
    "max": 0,
    "min": 0,
    "name": "name",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": true,
    "system": false,
    "type": "text"
  }))

  return app.save(collection)
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_1763078910")

  // update collection data
  unmarshal({
    "indexes": [
      "CREATE UNIQUE INDEX `idx_LGBzfa1gnL` ON `organisations` (\n  `charity_name`,\n  `financial_year_end`\n)"
    ]
  }, collection)

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
  collection.fields.addAt(3, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text2398087059",
    "max": 0,
    "min": 0,
    "name": "financial_year_end",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": true,
    "system": false,
    "type": "text"
  }))

  // add field
  collection.fields.addAt(6, new Field({
    "hidden": false,
    "id": "json854162502",
    "maxSize": 0,
    "name": "governance",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "json"
  }))

  // add field
  collection.fields.addAt(13, new Field({
    "cascadeDelete": false,
    "collectionId": "pbc_2034649627",
    "hidden": false,
    "id": "relation1507211071",
    "maxSelect": 1,
    "minSelect": 0,
    "name": "rem_pkg_review_report",
    "presentable": false,
    "required": false,
    "system": false,
    "type": "relation"
  }))

  // remove field
  collection.fields.removeById("text445106729")

  // update field
  collection.fields.addAt(1, new Field({
    "autogeneratePattern": "",
    "hidden": false,
    "id": "text284451158",
    "max": 0,
    "min": 0,
    "name": "charity_name",
    "pattern": "",
    "presentable": false,
    "primaryKey": false,
    "required": true,
    "system": false,
    "type": "text"
  }))

  return app.save(collection)
})
