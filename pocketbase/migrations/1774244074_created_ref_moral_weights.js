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
        "id": "text2890138554",
        "max": 0,
        "min": 0,
        "name": "species_key",
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
        "id": "text3669748592",
        "max": 0,
        "min": 0,
        "name": "species_name",
        "pattern": "",
        "presentable": false,
        "primaryKey": false,
        "required": true,
        "system": false,
        "type": "text"
      },
      {
        "hidden": false,
        "id": "number130897217",
        "max": null,
        "min": null,
        "name": "weight",
        "onlyInt": false,
        "presentable": false,
        "required": true,
        "system": false,
        "type": "number"
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
    "id": "pbc_2356542250",
    "indexes": [
      "CREATE UNIQUE INDEX `idx_jLz5cUotuT` ON `ref_moral_weights` (`species_key`)"
    ],
    "listRule": null,
    "name": "ref_moral_weights",
    "system": false,
    "type": "base",
    "updateRule": null,
    "viewRule": null
  });

  app.save(collection);

  const data = [
    {
      "species_key": "pig", "species_name": "Pig", "weight": 0.5150, "source_citation": "Rethink Priorities, 2023",
      "notes": "Median estimate; reflects high cognitive/affective complexity and limb similarity."
    },
    {
      "species_key": "cattle", "species_name": "Cattle", "weight": 0.5150, "source_citation": "EA Forum / RP Ref",
      "notes": "Standardly referenced to pigs; subject to significant heat stress burdens in tropics."
    },
    {
      "species_key": "dog", "species_name": "Dog", "weight": 1.0, "source_citation": "Rethink Priorities (Mammal Ref)",
      "notes": "High credence in sentience and moral interest; typically used as the mammalian baseline."
    },
    {
      "species_key": "cat", "species_name": "Cat", "weight": 1.0, "source_citation": "Rethink Priorities (Mammal Ref)",
      "notes": "High cognitive and emotional responsiveness; baseline mammal moral weight."
    },
    {
      "species_key": "rabbit", "species_name": "Rabbit", "weight": 0.5150, "source_citation": "Rethink Priorities (Mammal Ref)",
      "notes": "Mammalian physiology and complex nociception; weight aligned with other terrestrial mammals."
    },
    {
      "species_key": "chicken", "species_name": "Chicken", "weight": 0.3320, "source_citation": "Rethink Priorities, 2023",
      "notes": "Median estimate adjusted for probability of sentience and cognitive proxies."
    },
    {
      "species_key": "songbird", "species_name": "Songbird / Wild Bird", "weight": 0.3320, "source_citation": "Rethink Priorities (Chicken Ref)",
      "notes": "Capacity similar to domestic poultry; may experience more moments/sec due to high FFF."
    },
    {
      "species_key": "octopus", "species_name": "Octopus", "weight": 0.2130, "source_citation": "Rethink Priorities, 2023",
      "notes": "Outlier for invertebrates; recognized as sentient in UK and EU legislation."
    },
    {
      "species_key": "carp", "species_name": "Carp", "weight": 0.0890, "source_citation": "Rethink Priorities, 2023",
      "notes": "Reflects current research gaps in fish cognitive proxies."
    },
    {
      "species_key": "honey_bee", "species_name": "Honey Bee", "weight": 0.0710, "source_citation": "Rethink Priorities, 2023",
      "notes": "Reflects evidence of centralized pain processing and temporal resolution."
    },
    {
      "species_key": "salmon", "species_name": "Salmon", "weight": 0.0560, "source_citation": "Rethink Priorities, 2023",
      "notes": "Median estimate; primary subject of cost-effective stunning interventions."
    },
    {
      "species_key": "crayfish", "species_name": "Crayfish", "weight": 0.0380, "source_citation": "Rethink Priorities, 2023",
      "notes": "Part of the sentience review for decapod crustaceans."
    },
    {
      "species_key": "shrimp", "species_name": "Shrimp", "weight": 0.0310, "source_citation": "Rethink Priorities, 2023",
      "notes": "Median estimate; critical focus area due to massive slaughter scale."
    },
    {
      "species_key": "crab", "species_name": "Crab", "weight": 0.0230, "source_citation": "Rethink Priorities, 2023",
      "notes": "Reflects current conservative scoring of empirical traits for decapods."
    },
    {
      "species_key": "cricket", "species_name": "Farmed Cricket", "weight": 0.0130, "source_citation": "Rethink Priorities (BSF Ref)",
      "notes": "Benchmarked to other industrial insects like BSF."
    },
    {
      "species_key": "bsf", "species_name": "Black Soldier Fly", "weight": 0.0130, "source_citation": "Rethink Priorities, 2023",
      "notes": "Key species in the growing insect farming industry."
    },
    {
      "species_key": "silkworm", "species_name": "Silkworm", "weight": 0.0020, "source_citation": "Rethink Priorities, 2023",
      "notes": "Reflects the lowest intensity of cognitive proxies in reviewed literature."
    },
    {
      "species_key": "generic_companion", "species_name": "Generic Companion Animal", "weight": 1.0, "source_citation": "EA Consensus (Median)",
      "notes": "Baseline for companion animals when specific species is unknown."
    },
    {
      "species_key": "generic_farmed", "species_name": "Generic Farmed Animal", "weight": 0.3, "source_citation": "EA Consensus (Median)",
      "notes": "Conservative median for farmed animals when specific species is unknown."
    },
    {
      "species_key": "generic_wild", "species_name": "Generic Wild Animal", "weight": 0.2, "source_citation": "EA Consensus (Median)",
      "notes": "Conservative median for wild animals when specific species is unknown."
    },
    {
      "species_key": "generic_unspecified", "species_name": "Generic Unspecified Animal", "weight": 0.1, "source_citation": "EA Consensus (Conservative Baseline)",
      "notes": "General low baseline for animals when species and domain are unknown."
    }
  ];

  for (const item of data) {
    let record;
    try {
      // Try to find an existing record by the unique species_key
      record = app.findFirstRecordByData(collection.id, "species_key", item.species_key);
    } catch (e) {
      // If not found, create a new record
      record = new Record(collection);
    }

    // Populate the record with the new data
    const form = new RecordUpsertForm(app, record);
    form.load(item);
    form.submit(); // This will either create or update the record
  }
}, (app) => {
  const collection = app.findCollectionByNameOrId("ref_moral_weights");
  return app.delete(collection);
});