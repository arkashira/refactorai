# dataflow.md  

## System Dataflow Architecture for **refactorai**

```
+-------------------+        +-------------------+        +-------------------+
|  External Data    |        |   Ingestion Layer |        |   Processing /   |
|  Sources          |        |   (API Gateway)   |        |   Transform Tier |
|-------------------|        |-------------------|        |-------------------|
| • Git repos (GitHub,|  -->  | • AuthN / AuthZ   |  -->   | • Code parser     |
|   GitLab, Bitbucket) |      |   (OAuth2, OIDC) |        |   (tree‑sitter)   |
| • IDE plugins (VS  |        | • Rate limiter    |        | • LLM inference   |
|   Code, IntelliJ, |        | • Validation      |        |   service (GPT‑4) |
|   PyCharm)        |        |   (schema)        |        | • Refactor rules  |
| • CI/CD webhooks  |        | • Queue (Kafka)   |        |   engine          |
|   (GitHub Actions,|        |                   |        | • Diff generator  |
|   GitLab CI)      |        +-------------------+        +-------------------+
+-------------------+                                          |
                                                               |
                                                               v
+-------------------+        +-------------------+        +-------------------+
|   Storage Tier    |        |  Query / Serving  |        |   Egress to User  |
|-------------------|        |  Layer            |        |-------------------|
| • Object Store    |  <--   | • GraphQL API     |  -->   | • IDE plugin UI   |
|   (S3/MinIO)      |        |   (auth‑protected)|        |   (VS Code, Jet- |
| • Metadata DB    |        | • REST endpoints  |        |   brain, etc.)   |
|   (PostgreSQL)    |        |   (auth‑protected)|        | • Web dashboard   |
| • Vector Store    |        | • Cache (Redis)   |        |   (review results|
|   (PGVector)      |        +-------------------+        |    & suggestions)|
+-------------------+                                          |
                                                               |
                                                               v
+-------------------+
|   Monitoring &   |
|   Observability  |
|-------------------|
| • Metrics (Prom   |
|   ectus)          |
| • Logs (ELK)      |
| • Tracing (Jaeger)|
+-------------------+
```

### 1. External Data Sources
- **Git repositories** (GitHub, GitLab, Bitbucket) – full clone or shallow fetch of target branches.
- **IDE plugins** (VS Code, IntelliJ, PyCharm, Eclipse) – send opened file snapshots and cursor context.
- **CI/CD webhooks** – trigger analysis on PR creation / push events.
- **Package registries** (npm, PyPI, Maven) – optional dependency‑graph enrichment.

### 2. Ingestion Layer
| Component | Responsibility | Tech / Notes |
|-----------|----------------|--------------|
| **API Gateway** | Unified entry point; terminates TLS, validates JWT/OIDC tokens. | Kong / AWS API GW |
| **AuthN/AuthZ** | Enforce per‑user/project permissions; scopes: `read:repo`, `write:suggestions`. | OAuth2, OIDC, RBAC |
| **Rate Limiter & Quota** | Prevent abuse; per‑user request caps. | Redis‑based token bucket |
| **Schema Validation** | Ensure payload conforms to JSON schema (repo URL, commit SHA, IDE context). | AJV / Fastify |
| **Message Queue** | Decouple ingestion from processing; guarantee at‑least‑once delivery. | Apache Kafka (topic: `refactor_requests`) |
| **Dead‑Letter Queue** | Capture malformed or failed messages for later inspection. | Kafka DLQ |

### 3. Processing / Transform Layer
| Component | Responsibility | Tech / Notes |
|-----------|----------------|--------------|
| **Code Parser** | AST generation, language detection, tokenization. | Tree‑sitter + language plugins |
| **Embedding Service** | Produce vector embeddings for code snippets (for similarity / context). | OpenAI embeddings / sentence‑transformers, stored in PGVector |
| **LLM Inference Service** | Generate refactoring recommendations, explainability text. | Hosted GPT‑4‑Turbo (or open‑source Llama 2 70B) behind a GPU‑accelerated inference server (vLLM). |
| **Rule Engine** | Apply deterministic style/complexity rules (e.g., cyclomatic complexity thresholds). | OpenPolicyAgent (OPA) |
| **Diff Generator** | Compute minimal edit diffs between original and suggested code. | libgit2 + custom diff algorithm |
| **Orchestrator** | Coordinates steps, retries, and updates status in metadata DB. | Temporal.io workflow engine |
| **Security Scanner** | Optional static analysis (SAST) to ensure suggestions do not introduce vulnerabilities. | Bandit / Semgrep integration |

### 4. Storage Tier
- **Object Store (S3/MinIO)** – raw repository snapshots, generated diff patches, IDE plugin assets.
- **Metadata DB (PostgreSQL)** – request metadata, user/project mapping, job status, audit logs.
- **Vector Store (PGVector extension)** – embeddings for fast similarity search (e.g., “find similar refactor patterns”).
- **Cache (Redis)** – short‑lived results for repeated queries within a session.

All storage endpoints are behind VPC private subnets; access is mediated by IAM roles and signed URLs for object retrieval.

### 5. Query / Serving Layer
| Component | Responsibility | Tech / Notes |
|-----------|----------------|--------------|
| **GraphQL API** | Expose fine‑grained queries: `suggestions(projectId)`, `history(requestId)`. Auth‑protected. | Apollo Server |
| **REST Endpoints** | Legacy/simple calls for IDE plugins: `POST /analyze`, `GET /result/:id`. | FastAPI |
| **Cache Layer** | Serve recent suggestions instantly; TTL 15 min. | Redis |
| **WebSocket / SSE** | Push real‑time progress updates to IDE UI. | Socket.io |
| **Rate Limiting** | Enforce per‑user API quotas at this layer as second line of defense. | Kong plugins |

### 6. Egress to User
- **IDE Plugin UI** – Inline annotations, quick‑fix actions, side‑panel with detailed explanations. Communicates via the GraphQL/REST endpoints and WebSocket for live updates.
- **Web Dashboard** – Project‑level view of all analyses, trend charts (technical debt over time), exportable reports (PDF/Markdown). Auth via SSO (SAML/OIDC).
- **CLI Tool** – Optional `refactorai` command for batch processing in CI pipelines; outputs SARIF reports.

### 7. Auth Boundaries
1. **User ↔ API Gateway** – JWT/OIDC token validated; scopes checked.
2. **API Gateway ↔ Ingestion Queue** – Service‑to‑service auth via mTLS; producer identity attached to Kafka headers.
3. **Processing Workers ↔ Storage** – IAM role‑based access; signed URLs for object store reads/writes.
4. **Serving Layer ↔ Front‑end (IDE/Web)** – Same JWT passed; refreshed via refresh token flow.
5. **Internal Service Mesh** – Mutual TLS between micro‑services (Istio/Linkerd) to prevent lateral movement.

---

*End of dataflow.md*