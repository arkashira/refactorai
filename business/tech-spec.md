```markdown
# Technical Specification for RefactorAI

## Stack
- **Language/Framework**: Python (FastAPI) for backend, TypeScript (React) for frontend.
- **Runtime**: Docker containers orchestrated by Kubernetes.
- **Database**: PostgreSQL for relational data, MongoDB for unstructured data.
- **AI/ML**: PyTorch for model training, ONNX for model deployment.
- **IDE Integration**: Plugins for VSCode, IntelliJ, and PyCharm using their respective extension APIs.
- **Version Control Integration**: GitHub API, GitLab API, and Bitbucket API for version control system integration.

## Hosting
- **Free-Tier-First Platforms**:
  - **Backend**: Google Cloud Run (free tier: 2 million requests per month).
  - **Frontend**: Vercel (free tier: unlimited deployments, 100GB bandwidth per month).
  - **Database**: Supabase (free tier: 500MB database storage, 2GB bandwidth per month).
  - **AI/ML**: Google Cloud AI Platform (free tier: $300 credit for new users).

## Data Model
### Tables/Collections
1. **Users**
   - `user_id` (UUID, primary key)
   - `username` (String)
   - `email` (String)
   - `password_hash` (String)
   - `created_at` (Timestamp)
   - `updated_at` (Timestamp)

2. **Codebases**
   - `codebase_id` (UUID, primary key)
   - `user_id` (UUID, foreign key)
   - `repository_url` (String)
   - `branch` (String)
   - `last_analyzed` (Timestamp)
   - `status` (String)

3. **RefactoringRecommendations**
   - `recommendation_id` (UUID, primary key)
   - `codebase_id` (UUID, foreign key)
   - `file_path` (String)
   - `line_number` (Integer)
   - `description` (String)
   - `severity` (String)
   - `created_at` (Timestamp)

4. **UserFeedback**
   - `feedback_id` (UUID, primary key)
   - `recommendation_id` (UUID, foreign key)
   - `user_id` (UUID, foreign key)
   - `rating` (Integer)
   - `comments` (String)
   - `created_at` (Timestamp)

## API Surface
1. **POST /api/codebases**
   - Purpose: Register a new codebase for analysis.

2. **GET /api/codebases/{codebase_id}/recommendations**
   - Purpose: Retrieve refactoring recommendations for a specific codebase.

3. **POST /api/recommendations/{recommendation_id}/feedback**
   - Purpose: Submit user feedback on a specific recommendation.

4. **GET /api/users/{user_id}/codebases**
   - Purpose: Retrieve all codebases associated with a user.

5. **POST /api/auth/login**
   - Purpose: Authenticate a user and return an authentication token.

6. **POST /api/auth/register**
   - Purpose: Register a new user.

7. **GET /api/recommendations**
   - Purpose: Retrieve all refactoring recommendations across all codebases.

8. **PUT /api/recommendations/{recommendation_id}**
   - Purpose: Update the status of a recommendation.

9. **DELETE /api/codebases/{codebase_id}**
   - Purpose: Remove a codebase from the system.

10. **GET /api/recommendations/stats**
    - Purpose: Retrieve statistics on refactoring recommendations.

## Security Model
- **Authentication**: JWT (JSON Web Tokens) for API authentication.
- **Secrets Management**: Google Cloud Secret Manager for storing sensitive information.
- **IAM (Identity and Access Management)**: Role-based access control (RBAC) for different user roles (e.g., admin, developer).
- **Data Encryption**: TLS 1.3 for data in transit, AES-256 for data at rest.

## Observability
- **Logs**: Structured logging using ELK Stack (Elasticsearch, Logstash, Kibana).
- **Metrics**: Prometheus for metrics collection, Grafana for visualization.
- **Traces**: Jaeger for distributed tracing.

## Build/CI
- **CI/CD Pipeline**: GitHub Actions for continuous integration and deployment.
- **Build Tools**: Docker for containerization, Helm for Kubernetes deployments.
- **Testing**: Unit tests with pytest, integration tests with Postman, end-to-end tests with Cypress.
- **Deployment**: Automated deployments to Google Cloud Run and Vercel using GitHub Actions.
```