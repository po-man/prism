# openspec/changes/add-hitl-publishing-gate/tasks.md

## 1. PocketBase Migration (`pocketbase/migrations`)
- [ ] 1.1 Create a new JavaScript migration file (e.g., `1773000000_add_publish_status.js`) to modify the `organisations` collection.
- [ ] 1.2 Add a new field named `publish_status` of type `select`.
- [ ] 1.3 Configure the `select` options to be `["draft", "approved", "rejected"]` with the `maxSelect` set to 1.
- [ ] 1.4 Set the default value of the field to `draft`.

## 2. Orchestrator Updates (`n8n/workflows/SUjUpjve9Vj6aJSbbuIWL.json`)
- [ ] 2.1 Locate the final "Storage API - Update Charity - Analytics" node.
- [ ] 2.2 Update the JSON payload in the Body Parameters to explicitly include `"publish_status": "draft"` so that re-runs safely pull the charity off the live site.
- [ ] 2.3 Locate the node responsible for writing the Markdown stub to `web/content/` (created in a previous refactoring). Update the template string to inject `draft: {{ $json.publish_status !== 'approved' }}` into the frontmatter.

## 3. Script Updates (`scripts/generate_stubs.py`)
- [ ] 3.1 Open `scripts/generate_stubs.py`.
- [ ] 3.2 Update the `create_markdown_stub` function to accept the parsed JSON and evaluate the status:
  `is_draft = "true" if org_data.get("publish_status") != "approved" else "false"`
- [ ] 3.3 Inject `draft: {is_draft}` into the generated f-string frontmatter payload.

## 4. Operational Workflow (No code changes, process only)
- [ ] 4.1 To review new extractions, run `hugo server -D` locally.
- [ ] 4.2 Validate the metrics. If corrections are needed, edit the record via the PocketBase Admin UI (`http://localhost:8090/_/`).
- [ ] 4.3 Change `publish_status` to `approved` and save.
- [ ] 4.4 Run `python scripts/sync_pb_to_fs.py` to pull the approved data to the local repo before running `git commit`.