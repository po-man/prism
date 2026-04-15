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
        "id": "text896622048",
        "max": 0,
        "min": 0,
        "name": "intervention_key",
        "pattern": "",
        "presentable": false,
        "primaryKey": false,
        "required": true,
        "system": false,
        "type": "text"
      },
      {
        "hidden": false,
        "id": "number4154937389",
        "max": null,
        "min": null,
        "name": "baseline_probability",
        "onlyInt": false,
        "presentable": false,
        "required": true,
        "system": false,
        "type": "number"
      },
      {
        "autogeneratePattern": "",
        "hidden": false,
        "id": "text258142582",
        "max": 0,
        "min": 0,
        "name": "region",
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
        "required": true,
        "system": false,
        "type": "text"
      },
      {
        "autogeneratePattern": "",
        "hidden": false,
        "id": "text18589324",
        "max": 0,
        "min": 0,
        "name": "notes",
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
    "id": "pbc_3379366518",
    "indexes": [
      "CREATE INDEX `idx_7mVbxC1AgZ` ON `ref_intervention_baselines` (`intervention_key`)"
    ],
    "listRule": null,
    "name": "ref_intervention_baselines",
    "system": false,
    "type": "base",
    "updateRule": null,
    "viewRule": null
  });

  app.save(collection);

  const baselinesCollection = app.findCollectionByNameOrId("ref_intervention_baselines");
  const baselineData = [
    { "intervention_key": "corporate_welfare_campaigns", "baseline_probability": 0.45, "region": "Global", "source_citation": "Animal Charity Evaluators (ACE)", "notes": "Corporate pressure campaigns (e.g., cage-free) have a historically strong success rate." },
    { "intervention_key": "policy_and_legal_advocacy", "baseline_probability": 0.10, "region": "Global", "source_citation": "Open Philanthropy", "notes": "Legislative changes are high variance, low probability, high payout." },
    { "intervention_key": "alternative_protein_and_food_tech", "baseline_probability": 0.15, "region": "Global", "source_citation": "Good Food Institute / VC Averages", "notes": "Benchmarked against standard Venture Capital success rates." },
    { "intervention_key": "undercover_investigations_and_exposes", "baseline_probability": 0.25, "region": "Global", "source_citation": "ACE Impact Models", "notes": "Unpredictable conversion from media attention to concrete action." },
    { "intervention_key": "capacity_building_and_movement_growth", "baseline_probability": 0.20, "region": "Global", "source_citation": "Founders Pledge", "notes": "Meta-charity multiplier; dependent on downstream success." },
    { "intervention_key": "scientific_and_welfare_research", "baseline_probability": 0.30, "region": "Global", "source_citation": "Rethink Priorities", "notes": "Probability that research directly leads to an implemented welfare improvement." },
    { "intervention_key": "individual_rescue_and_sanctuary", "baseline_probability": 1.00, "region": "Global", "source_citation": "EA Consensus", "notes": "Direct intervention. 0 systemic leverage; scale is exact." },
    { "intervention_key": "veterinary_care_and_treatment", "baseline_probability": 1.00, "region": "Global", "source_citation": "EA Consensus", "notes": "Direct intervention. 0 systemic leverage; scale is exact." },
    { "intervention_key": "high_volume_spay_neuter", "baseline_probability": 1.00, "region": "Global", "source_citation": "EA Consensus", "notes": "Direct intervention. Preventative but non-probabilistic at extraction level." }
  ];

  for (const item of baselineData) {
    let record;
    try {
      record = app.findFirstRecordByData(baselinesCollection.id, "intervention_key", item.intervention_key);
    } catch (e) {
      record = new Record(baselinesCollection);
    }
    const form = new RecordUpsertForm(app, record);
    form.load(item);
    form.submit();
  }
}, (app) => {
  const collection = app.findCollectionByNameOrId("pbc_3379366518");

  return app.delete(collection);
})
