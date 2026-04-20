## 1. Master Directory Updates (`web/layouts/`)
- [ ] 1.1 Open `web/layouts/index.html`.
- [ ] 1.2 In the table `<thead >`, delete the `<th>` for `Highest Leverage (Tractability)`.
- [ ] 1.3 In the `<tbody>` range loop, delete the entire `<td>` block mapping to `Highest Leverage (Tractability)` (including the `$tractabilityCheck` Scratch logic preceding it).
- [ ] 1.4 In the `<script>` block for table sorting, remove the `else if (sortType === 'tractability') { ... }` sorting condition block.
- [ ] 1.5 Open `web/layouts/partials/index-how-to-read.html` and delete the `div` containing `data-highlight-column="Highest Leverage (Tractability)"`.

## 2. Impact Profile (ITN Scorecard) Refactoring (`web/layouts/partials/`)
- [ ] 2.1 Open `web/layouts/partials/itn-scorecard.html`.
- [ ] 2.2 Change the section heading from `<h2 ...>ITN Scorecard</h2>` to `<h2 ...>Impact Profile</h2>`.
- [ ] 2.3 Locate the "Tractability" card section (Middle column).
- [ ] 2.4 Change the card header `<h3>Highest Intervention Leverage</h3>` to `<h3>Verified Interventions</h3>`.
- [ ] 2.5 Delete the `<p class="text-xl font-semibold text-gray-900">{{ $tractabilityTier }}</p>` element to remove the prominent Tier emphasis.
- [ ] 2.6 Refactor the `range $tractabilityElaboration` loop. Remove the `<h4 ...>{{ .tier_name }}</h4>` rendering. Instead, output the extracted `$name` strings directly as inline, styled pill badges (e.g., `bg-blue-50 text-blue-700 px-2 py-1 rounded-md text-sm font-medium`) clustered together via flex-wrap, placing the `provenance-badge.html` directly next to the intervention name inside the pill.

## 3. IES Scorecard Contextualisation (`web/layouts/partials/`)
- [ ] 3.1 Open `web/layouts/partials/ies-scorecard.html`.
- [ ] 3.2 Add a new explanatory `<p>` tag beneath the main header, stating: "This model exposes the 'ingredients' of impact calculation. The resulting scores are provided as a reference point to standardise impact across different species and interventions, rather than declaring an absolute 'golden' score."
- [ ] 3.3 Locate the "Evaluated Impact" metric block within the 3-column grid. Change the font class of the `{{ $ies_metric.evaluated_ies }}` output from `text-4xl font-extrabold` to `text-3xl font-bold` to visually balance it with the "Claimed Impact" column.