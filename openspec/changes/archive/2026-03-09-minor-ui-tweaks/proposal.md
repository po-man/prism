## Why
As PRISM matures, several minor UI refinements are needed to improve the user experience, data context, and regional accuracy. Specifically, users need immediate visibility of the reporting financial year, sorting behaviours should surface the highest-performing/most-recent items first, and timestamps must accurately reflect the project's primary operating timezone (Hong Kong). 

## What Changes
- **Favicon:** Add standard favicon linking to the base HTML layout to improve browser tab recognition.
- **Financial Year Context:** Surface the `financial_year` from the financials schema in the individual organisation header and the Impact Pathway 'Inputs' card.
- **Data Source Icon Spacing:** Reduce the horizontal margin (`ml-1.5` to `ml-0.5`) between the SVG icons and their text labels in the single organisation view for a tighter, more polished look.
- **Timezone Localisation:** Update all Hugo time formatting functions for the `updated` field to explicitly cast the UTC database timestamps into the `Asia/Hong_Kong` timezone.
- **Table Sorting:** Invert the default initial sorting state of the master directory table. Changing the initial HTML data attributes from `asc` to `desc` will ensure the first user click sorts the data in descending order.

## Impact
- **Affected specs:** `ui`
- **Affected code:** - `web/layouts/_default/baseof.html`
  - `web/layouts/_default/single.html`
  - `web/layouts/index.html`
  - `web/layouts/partials/impact-pathway.html`