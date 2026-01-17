# Implementation Tasks

## Initialization
- [x] Initialize Git repository.
- [x] Create top-level directories: `workflows`, `schemas`, `data`, `web`, `openspec`.
- [x] Create `.gitignore` ignoring `node_modules`, `public/`, and n8n binary data.

## Schema Layer
- [x] Create `schemas/README.md` documenting usage protocols.

## Data Layer
- [x] Create `data/organisations/` directory.
- [x] Add a `.gitkeep` file to preserve the directory structure.

## Web Layer (Frontend)
- [x] Initialize new Hugo site in `web/`.
- [x] Configure Hugo `hugo.yaml` to mount `../data` as a data source.
- [x] Install Tailwind CSS module in `web/`.

## Orchestration Layer (n8n)
- [x] Create `docker-compose.yml` in root to spin up n8n.
- [x] Map local `workflows/` and `data/` volumes to the n8n container.