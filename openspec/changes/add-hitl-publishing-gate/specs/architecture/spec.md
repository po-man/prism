## ADDED Requirements

### Requirement: Human-In-The-Loop (HITL) Publishing Gate
The architecture SHALL enforce a "fail-closed" staging environment, ensuring no AI-generated data is deployed to the public production build without explicit human approval.

#### Scenario: Defaulting to Draft State
- **WHEN** a new organisation record is created in the Data Vault (PocketBase) OR when existing extraction data (financials/impact) is overwritten by the Orchestrator (n8n)
- **THEN** the record's `publish_status` MUST be explicitly set to `draft`.
- **AND** it MUST remain in this state until a human analyst manually updates the record to `approved`.

#### Scenario: Hugo-Native Staging and Safe Deployment
- **WHEN** the system generates Markdown routing stubs for the static site
- **THEN** the generator MUST read the `publish_status` of the JSON artifact.
- **AND** if the status is `draft`, the frontmatter MUST include `draft: true`.
- **AND** the production CI/CD build command (`hugo`) MUST natively ignore these drafts, while allowing analysts to preview them locally using the `hugo server -D` command.