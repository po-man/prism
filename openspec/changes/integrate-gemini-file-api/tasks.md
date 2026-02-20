## 1. Database Schema Updates (PocketBase)
- [ ] 1.1 Create a new migration file in `pocketbase/migrations/` to update the `source_artifacts` collection.
- [ ] 1.2 Add a new text field: `gemini_file_uri` (pattern: URI).
- [ ] 1.3 Add a new date field: `gemini_file_uploaded_at`.
- [ ] 1.4 Apply the migration and verify the fields appear in the PocketBase Admin UI.

## 2. Create Sub-Workflow: `Ensure Gemini URI`
- [ ] 2.1 Create a new n8n workflow. Add an `Execute Workflow Trigger` node that accepts `artifact_id` and `file_name` as inputs.
- [ ] 2.2 Add an `HTTP Request` node to `GET` the `source_artifacts` record from PocketBase using the `artifact_id`.
- [ ] 2.3 Add an `If` node to check expiration. Logic: `{{ $json.gemini_file_uploaded_at }}` is not empty AND the difference between now and the timestamp is less than 46 hours.
- [ ] 2.4 **True Branch (Cache Hit):** Route directly to a `Set` node that outputs `gemini_file_uri`.
- [ ] 2.5 **False Branch (Cache Miss / Expired):**
      - Add an `HTTP Request` node to download the binary file from PocketBase (`/api/files/source_artifacts/{{$json.id}}/{{$json.raw}}`).
      - Add an `HTTP Request` node to upload the binary to `https://generativelanguage.googleapis.com/upload/v1beta/files`. Ensure `X-Goog-Upload-Protocol: multipart` is set.
      - Add an `HTTP Request` node to `PATCH` the `source_artifacts` record with the newly returned `file.uri` and the current datetime for `gemini_file_uploaded_at`.
      - Route to a `Set` node that outputs the new `gemini_file_uri`.

## 3. Update Main Workflow (`SUjUpjve9Vj6aJSbbuIWL.json`)
- [ ] 3.1 Locate the existing nodes that download the physical binaries right before extraction (e.g., "Storage API - Get Charity - Download Annual Report").
- [ ] 3.2 Replace these binary download nodes with `Execute Workflow` nodes calling the new `Ensure Gemini URI` sub-workflow. Map the `artifact_id` from the expanded `organisations` record.
- [ ] 3.3 Update the "Extract Financials" `HTTP Request` node payload. Replace the base64 `inline_data` object with:
      ```json
      {
        "file_data": {
          "mime_type": "application/pdf",
          "file_uri": "={{ $json.gemini_file_uri }}"
        }
      }
      ```
- [ ] 3.4 Repeat the payload update for the "Extract Governance Metrics" and "Extract Impact Metrics" LLM nodes.
- [ ] 3.5 Remove the legacy `Code` nodes that were manually formatting base64 attachments (e.g., `Code in JavaScript1`, `Code in JavaScript2` that mapped `inline_data`), as they are now obsolete.

## 4. Testing & Validation
- [ ] 4.1 Trigger the main workflow for an NGO with a >50MB Annual Report.
- [ ] 4.2 Verify the `source_artifacts` collection successfully stores the `gemini_file_uri` and timestamp.
- [ ] 4.3 Trigger the main workflow a second time immediately after. Verify the sub-workflow takes the `True` branch (cache hit) and skips the Gemini upload.
- [ ] 4.4 Manually edit the `gemini_file_uploaded_at` in PocketBase to be 3 days ago. Re-run the main workflow, and verify the sub-workflow successfully re-uploads the file and updates the record.