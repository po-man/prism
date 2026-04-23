/// <reference path="../pb_data/types.d.ts" />
migrate((app) => {
  const collection = new Collection({
    "createRule": null,
    "deleteRule": null,
    "fields": [
      {
        "autogeneratePattern": "[a-z0-9]{15}",
        "hidden": false,
        "id": "text3208210256",
        "max": 15,
        "min": 15,
        "name": "id",
        "pattern": "^[a-z0-9]+$",
        "presentable": false,
        "primaryKey": true,
        "required": true,
        "system": true,
        "type": "text"
      },
      {
        "autogeneratePattern": "",
        "hidden": false,
        "id": "text2336344884",
        "max": 0,
        "min": 0,
        "name": "evidence_key",
        "pattern": "",
        "presentable": false,
        "primaryKey": false,
        "required": true,
        "system": false,
        "type": "text"
      },
      {
        "hidden": false,
        "id": "number2761599323",
        "max": null,
        "min": null,
        "name": "multiplier",
        "onlyInt": false,
        "presentable": false,
        "required": false,
        "system": false,
        "type": "number"
      },
      {
        "autogeneratePattern": "",
        "hidden": false,
        "id": "text1843675174",
        "max": 0,
        "min": 0,
        "name": "description",
        "pattern": "",
        "presentable": false,
        "primaryKey": false,
        "required": true,
        "system": false,
        "type": "text"
      },
      {
        "autogeneratePattern": "",
        "hidden": false,
        "id": "text3114117804",
        "max": 0,
        "min": 0,
        "name": "source_citation",
        "pattern": "",
        "presentable": false,
        "primaryKey": false,
        "required": false,
        "system": false,
        "type": "text"
      },
      {
        "hidden": false,
        "id": "autodate2990389176",
        "name": "created",
        "onCreate": true,
        "onUpdate": false,
        "presentable": false,
        "system": false,
        "type": "autodate"
      },
      {
        "hidden": false,
        "id": "autodate3332085495",
        "name": "updated",
        "onCreate": true,
        "onUpdate": true,
        "presentable": false,
        "system": false,
        "type": "autodate"
      }
    ],
    "id": "pbc_2642153938",
    "indexes": [
      "CREATE INDEX `idx_wzyjzFac3o` ON `ref_evidence_discounts` (`evidence_key`)"
    ],
    "listRule": null,
    "name": "ref_evidence_discounts",
    "system": false,
    "type": "base",
    "updateRule": null,
    "viewRule": null
  });

  app.save(collection);

  const discountsCollection = app.findCollectionByNameOrId("ref_evidence_discounts");
  const discountData = [
    { "evidence_key": "RCT/Meta-Analysis", "multiplier": 1.00, "description": "Randomised control and treatment groups; highest epistemic confidence.", "source_citation": "GiveWell / ACE Baseline" },
    { "evidence_key": "Quasi-Experimental", "multiplier": 0.70, "description": "Non-randomised control group; moderate risk of selection bias.", "source_citation": "Extrapolated from GiveWell validity adjustments" },
    { "evidence_key": "Self-Reported", "multiplier": 0.3, "description": "Self-reported claims without rigorous external control groups.", "source_citation": "PRISM Standard" }
  ];

  for (const item of discountData) {
    let record;
    try {
      record = app.findFirstRecordByData(discountsCollection.id, "evidence_key", item.evidence_key);
    } catch (e) {
      record = new Record(discountsCollection);
    }
    const form = new RecordUpsertForm(app, record);
    form.load(item);
    form.submit();
  }
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_2642153938");

  return app.delete(collection);
})
