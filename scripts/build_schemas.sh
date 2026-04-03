#!/bin/bash

for schema in {analytics,meta,impact_beneficiaries,impact_interventions,impact_metrics,impact_transparency,financials,search}; do
    datamodel-codegen \
        --input schemas/v1/$schema.schema.json \
        --input-file-type jsonschema \
        --output-model-type pydantic_v2.BaseModel \
        --output utils_api/app/schemas/$schema.py \
        --use-subclass-enum
done
