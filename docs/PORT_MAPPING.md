# Port Mapping Registry

This registry is the authoritative list of ports exposed by the VibeCO microservices
and supporting infrastructure. Update it whenever a service adds, removes, or changes
a network listener. Downstream manifests (Docker Compose, Kubernetes, Terraform,
reverse proxies) must reference the values here.

| Service | Description | Local Dev Port | Container Port | Protocol | Notes |
| --- | --- | --- | --- | --- | --- |
| `api-gateway` | Edge ingress that authenticates requests and routes to backend services. | `8080` | `8080` | HTTP | Publishes OpenAPI docs at `/docs`. |
| `project-service` | CRUD API for project metadata and timeline entries. | `8081` | `8081` | HTTP | Depends on PostgreSQL via internal network. |
| `reporting-service` | Aggregates analytics and exports PDF/markdown summaries. | `8082` | `8082` | HTTP | Triggers async jobs through the worker queue. |
| `render-worker` | Background worker responsible for heavy markdown rendering tasks. | `5672` | `5672` | AMQP | Connects to RabbitMQ; not exposed outside the cluster. |
| `identity-service` | OAuth2 provider for first-party agents. | `8083` | `8083` | HTTP | Callback URLs must be registered with the gateway. |
| `metrics-collector` | Prometheus-compatible metrics endpoint. | `9090` | `9090` | HTTP | Scraped by the platform observability stack. |

## Change Control Checklist

- [ ] Update gateway routing configuration after modifying any service port.
- [ ] Notify platform operations so firewall/security groups reflect the change.
- [ ] Search for the old port values in `configs/`, `deploy/`, and infrastructure
      repositories to ensure they are replaced.
- [ ] Announce the change in the release notes and architecture stand-up.

Keep this file reviewed first during incident response. If the running environment
does not match the registry, treat it as a misconfiguration bug.
