# PawCare+ Microservices Application

PawCare+ is a production-ready microservices application for managing pet owners, pets, and appointments. It features a React frontend and three Python FastAPI backend services, all containerized and deployable to Kubernetes.

## Architecture

- **Frontend**: React application with Vite, served via Nginx
- **Pet Service**: Manages owners and pets (FastAPI + PostgreSQL)
- **Appointment Service**: Handles appointment scheduling and status lifecycle (FastAPI + PostgreSQL)
- **Notification Service**: Logs notifications for appointment status changes (FastAPI)
- **Database**: PostgreSQL
- **Deployment**: Docker + Kubernetes + Helm

## Project Structure

```
pawcare-plus/
├── docker-compose.yaml          # Local development setup
├── frontend/                    # React application
├── services/
│   ├── pet-service/            # Pet management service
│   ├── appointment-service/    # Appointment management service
│   └── notification-service/   # Notification logging service
└── helm/                       # Kubernetes Helm charts
    ├── pet-service/
    ├── appointment-service/
    ├── notification-service/
    ├── frontend/    ├── postgres/    └── ingress/
```

## Prerequisites

- Docker and Docker Compose
- Node.js 18+ and npm (for local frontend development)
- kubectl and Helm (for Kubernetes deployment)
- Python 3.11+ (optional, for local service development)

## Local Development Setup

### 1. Clone and Navigate

```bash
cd pawcare-plus
```

### 2. Start Services with Docker Compose

```bash
docker-compose up --build
```

This will start:
- PostgreSQL database
- Pet Service (http://localhost:8001)
- Appointment Service (http://localhost:8002)
- Notification Service (http://localhost:8003)
- Frontend (http://localhost:3000)

### 3. Access the Application

- **Frontend**: http://localhost:3000
- **Pet Service API Docs**: http://localhost:8001/docs
- **Appointment Service API Docs**: http://localhost:8002/docs
- **Notification Service API Docs**: http://localhost:8003/docs

### 4. API Endpoints

#### Pet Service
- `GET /owners/` - List owners
- `POST /owners/` - Create owner
- `GET /pets/` - List pets
- `POST /pets/` - Create pet
- `GET /health` - Health check

#### Appointment Service
- `GET /appointments/` - List appointments
- `POST /appointments/` - Create appointment
- `PUT /appointments/{id}/status` - Update appointment status
- `GET /health` - Health check

#### Notification Service
- `POST /notifications/` - Log notification
- `GET /health` - Health check

## Kubernetes Deployment

### Prerequisites

- Kubernetes cluster (local: minikube, kind, or k3s)
- Helm 3+
- NGINX Ingress Controller installed

### 1. Install NGINX Ingress Controller

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v0.49.0/deploy/static/provider/cloud/deploy.yaml
```

### 2. Build and Push Docker Images

```bash
# Build services
docker build -t your-registry/pet-service:latest ./services/pet-service
docker build -t your-registry/appointment-service:latest ./services/appointment-service
docker build -t your-registry/notification-service:latest ./services/notification-service
docker build -t your-registry/frontend:latest ./frontend

# Push to registry
docker push your-registry/pet-service:latest
docker push your-registry/appointment-service:latest
docker push your-registry/notification-service:latest
docker push your-registry/frontend:latest
```

### 3. Deploy PostgreSQL

```bash
kubectl apply -f https://raw.githubusercontent.com/bitnami/charts/main/bitnami/postgresql/templates/
# Or use a managed PostgreSQL service
```

### 2. Deploy PostgreSQL

```bash
helm install postgres ./helm/postgres
```

### 3. Deploy Services

```bash
helm install pet-service ./helm/pet-service
helm install appointment-service ./helm/appointment-service
helm install notification-service ./helm/notification-service
helm install frontend ./helm/frontend
helm install ingress ./helm/ingress
```

### 5. Update /etc/hosts

Add to your `/etc/hosts`:
```
127.0.0.1 pawcare.local
```

### 6. Access the Application

- **Frontend**: http://pawcare.local
- **Pet Service**: http://pawcare.local/api/pets
- **Appointment Service**: http://pawcare.local/api/appointments
- **Notification Service**: http://pawcare.local/api/notifications

## Development

### Frontend Development

```bash
cd frontend
npm install
npm run dev
```

### Service Development

Each service can be run locally:

```bash
cd services/pet-service
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Set environment variables:
```bash
export DATABASE_URL="postgresql://user:password@localhost:5432/pawcare"
```

## Configuration

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `NOTIFICATION_SERVICE_URL`: URL for notification service
- `REACT_APP_API_BASE`: Frontend API base URL

### Helm Values

Customize deployment by editing `values.yaml` in each Helm chart:
- Image versions
- Resource limits
- Environment variables
- Service configurations

## Health Checks

All services include:
- `/health` endpoint
- Kubernetes readiness and liveness probes
- Docker health checks

## Monitoring and Logging

- Services use Python logging
- Structured logs for appointment status changes
- Health endpoints for monitoring

## API Documentation

OpenAPI/Swagger docs available at:
- Pet Service: `/docs`
- Appointment Service: `/docs`
- Notification Service: `/docs`

## Testing

```bash
# Run docker-compose tests
docker-compose up --abort-on-container-exit

# Individual service tests (when implemented)
cd services/pet-service
pytest
```

## Contributing

1. Follow the existing code structure
2. Add tests for new features
3. Update documentation
4. Use meaningful commit messages

## License

This project is licensed under the MIT License.