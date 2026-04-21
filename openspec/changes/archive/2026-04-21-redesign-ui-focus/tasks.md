## 1. Master Directory Updates (`web/layouts/`)
- [x] 1.1 Open `web/layouts/index.html`.
- [x] 1.2 In the table `<thead >`, delete the `<th>` for `Highest Leverage (Tractability)`.
- [x] 1.3 In the `<tbody>` range loop, delete the entire `<td>` block mapping to `Highest Leverage (Tractability)` (including the `$tractabilityCheck` Scratch logic preceding it).
- [x] 1.4 In the `<script>` block for table sorting, remove the `else if (sortType === 'tractability') { ... }` sorting condition block.
- [x] 1.5 Open `web/layouts/partials/index-how-to-read.html` and delete the `div` containing `data-highlight-column="Highest Leverage (Tractability)"`.

## 2. Impact Profile (ITN Scorecard) Refactoring (`web/layouts/partials/`)
- [x] 2.1 Open `web/layouts/partials/itn-scorecard.html`.
- [x] 2.2 Change the section heading from `<h2 ...>ITN Scorecard</h2>` to `<h2 ...>Impact Profile</h2>`.
- [x] 2.3 Locate the "Tractability" card section (Middle column).
- [x] 2.4 Change the card header `<h3>Highest Intervention Leverage</h3>` to `<h3>Intervention Portfolio</h3>`.
- [x] 2.5 Delete the `<p class="text-xl font-semibold text-gray-900">{{ $tractabilityTier }}</p>` element to remove the prominent Tier emphasis.
- [x] 2.6 Refactor the `range $tractabilityElaboration` loop. Remove the `<h4 ...>{{ .tier_name }}</h4>` rendering. Instead, output the extracted `$name` strings directly as inline, styled pill badges (e.g., `bg-blue-50 text-blue-700 px-2 py-1 rounded-md text-sm font-medium`) clustered together via flex-wrap, placing the `provenance-badge.html` directly next to the intervention name inside the pill.
    - Inside the loop, check if the intervention name is already in the slice. If not, append it and render the extracted `$name` as an inline, styled pill badge (e.g., `<span class="bg-blue-50 text-blue-700 px-3 py-1 rounded-full text-sm font-medium">...</span>`), clustered together via a `flex flex-wrap gap-2` container. Include the `provenance-badge.html` adjacent to the text inside the pill.
- [x] 2.7 **Layout Restructuring:** Change the parent grid container for the cards. Currently it is likely `grid-cols-1 md:grid-cols-3`. Change it so the first two cards (Importance & Neglectedness) sit in a `grid-cols-1 md:grid-cols-2` container, and move the Tractability card outside this grid to sit below them as a full-width block.
- [x] 2.8 **Rename Demographics:** - Change the "Importance" card header from `<h3>Scale (Importance)</h3>` to `<h3>Scale of Reach</h3>` (or "Total Beneficiaries").
    - Change the "Neglectedness" card header from `<h3>Target Species (Neglectedness)</h3>` to `<h3>Beneficiary Demographics</h3>`.

## 3. IES Scorecard Contextualisation (`web/layouts/partials/`)
- [x] 3.1 Open `web/layouts/partials/ies-scorecard.html`.
- [x] 3.2 Add a new explanatory `<p>` tag beneath the main header, stating: "This model exposes the 'ingredients' of impact calculation. The resulting scores are provided as a reference point to standardise impact across different species and interventions, rather than declaring an absolute 'golden' score."
- [x] 3.3 Locate the "Evaluated Impact" metric block within the 3-column grid. Change the font class of the `{{ $ies_metric.evaluated_ies }}` output from `text-4xl font-extrabold` to `text-3xl font-bold` to visually balance it with the "Claimed Impact" column.
- [x] 3.4 Locate the main "Evaluated Impact" header or score readout. Insert a small UI badge reading "Annual" (e.g., `<span class="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-gray-100 text-gray-800">Annual</span>`) next to it.