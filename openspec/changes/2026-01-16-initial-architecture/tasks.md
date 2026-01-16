# Implementation Tasks

## Initialization
- [ ] Initialize Git repository.
- [ ] Create top-level directories: `workflows`, `schemas`, `data`, `web`, `openspec`.
- [ ] Create `.gitignore` ignoring `node_modules`, `public/`, and n8n binary data.

## Schema Layer
- [ ] Create `schemas/README.md` documenting usage protocols.

## Data Layer
- [ ] Create `data/organisations/` directory.
- [ ] Add a `.gitkeep` file to preserve the directory structure.

## Web Layer (Frontend)
- [ ] Initialize new Hugo site in `web/`.
- [ ] Configure Hugo `config.toml` to mount `../data` as a data source.
- [ ] Install Tailwind CSS module in `web/`.

## Orchestration Layer (n8n)
- [ ] Create `docker-compose.yml` in root to spin up n8n.
- [ ] Map local `workflows/` and `data/` volumes to the n8n container.