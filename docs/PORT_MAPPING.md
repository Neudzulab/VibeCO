# Port Mapping Registry

The port map is the first document to read when touching the platform topology.
It is the canonical reference for every gateway route and downstream microservice
listener. If an environment drifts from these values, treat it as a bug and
correct it before moving forward with the deployment or investigation.

The data is stored twice for different audiences:

- `configs/port_mapping.yaml` — machine-readable snapshot for automation,
  sanity checks, and dashboards.
- This markdown file — human-friendly briefing that highlights intent, notes,
  and change control reminders.

Always update the YAML file **and** this document in the same commit. CI checks
read the YAML, while reviewers and operators lean on the prose below.

| Service | Description | Local Dev Port | Container Port | Protocol | Notes |
| --- | --- | --- | --- | --- | --- |
| `api-gateway` | Edge ingress that authenticates requests and routes to backend services. | `8080` | `8080` | HTTP | Publishes OpenAPI docs at `/docs`; first stop when debugging routing. |
| `project-service` | CRUD API for project metadata and timeline entries. | `8081` | `8081` | HTTP | Depends on PostgreSQL via internal network. |
| `reporting-service` | Aggregates analytics and exports PDF/markdown summaries. | `8082` | `8082` | HTTP | Triggers async jobs through the worker queue. |
| `render-worker` | Background worker responsible for heavy markdown rendering tasks. | `5672` | `5672` | AMQP | Connects to RabbitMQ; not exposed outside the cluster. |
| `identity-service` | OAuth2 provider for first-party agents. | `8083` | `8083` | HTTP | Callback URLs must be registered with the gateway. |
| `metrics-collector` | Prometheus-compatible metrics endpoint. | `9090` | `9090` | HTTP | Scraped by the platform observability stack. |

## Verification flow

1. Open `configs/port_mapping.yaml` to confirm the intended bindings.
2. Compare with the active manifests (Docker Compose, Kubernetes, Terraform).
3. Validate gateway configuration for every listed port.
4. Run smoke tests against each service using the documented local ports.
5. Record mismatches as incidents and correct them immediately.

## Change control checklist

- [ ] Update gateway routing configuration after modifying any service port.
- [ ] Notify platform operations so firewall/security groups reflect the change.
- [ ] Search for the old port values across `configs/`, `deploy/`, and
      infrastructure repositories to ensure they are replaced.
- [ ] Announce the change in the release notes and architecture stand-up.

Archive superseded values in the version control history instead of deleting
them from git. Anyone confused about a port should check this registry first.
