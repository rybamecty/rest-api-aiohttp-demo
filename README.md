# Culture Analytics - Test Assignment

REST API with aiohttp for Junior SaaS Developer position.

## Project Structure

```
culture-analytics/
├── app.py               # Main application entry point
├── server/              # Server components
│   ├── config.py       # Application configuration
│   ├── handlers.py     # HTTP request handlers
│   └── models.py       # Pydantic data models
├── client/             # Client implementations
│   ├── simple_client.py       # Manual aiohttp client
│   └── generated/             # Auto-generated client
├── tests/              # Test suite
│   ├── test_server.py         # Server tests
│   └── test_simple_client.py  # Client tests
├── openapi.yaml        # OpenAPI specification
├── requirements.txt    # Dependencies
└── pytest.ini          # Pytest configuration
```

## Installation

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

Application can be configured via environment variables:

```bash
# Server configuration
export HOST=0.0.0.0        # Server host (default: 0.0.0.0)
export PORT=8080           # Server port (default: 8080)
```

Or create `.env` file:
```
HOST=0.0.0.0
PORT=8080
```

## Running the Server

```bash
python app.py
```

Server will start at `http://localhost:8080`

## API Endpoints

- `GET /health` - Service health check
- `POST /data` - Create new data item
- `GET /data` - Get all data items
- `GET /data/{id}` - Get item by ID
- `DELETE /data/{id}` - Delete item by ID

## Usage Examples

### Health Check
```bash
curl http://localhost:8080/health
```

Response:
```json
{"status": "ok", "version": "1.0.0"}
```

### Create Item
```bash
curl -X POST http://localhost:8080/data \
  -H "Content-Type: application/json" \
  -d '{"name": "Sales", "value": 1000.50}'
```

Response:
```json
{"id": 1, "name": "Sales", "value": 1000.5}
```

### Get All Items
```bash
curl http://localhost:8080/data
```

### Get Item by ID
```bash
curl http://localhost:8080/data/1
```

### Delete Item
```bash
curl -X DELETE http://localhost:8080/data/1
```

## Using the Client

### Manual Client

```python
from client.simple_client import CultureAnalyticsClient

# Create client
client = CultureAnalyticsClient(base_url="http://localhost:8080")

# Health check
response = await client.health_check()
print(response)  # {'status': 'ok', 'version': '1.0.0'}

# Create item
item = await client.create_data(name="Sales", value=1000.50)
print(item)  # {'id': 1, 'name': 'Sales', 'value': 1000.5}

# List items
items = await client.list_data()
print(items)
```

### Auto-generated Client

```bash
# Install generator
pip install openapi-python-client

# Generate client
openapi-python-client generate --path openapi.yaml --output-path client/generated

# Install generated client
pip install -e client/generated/
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ -v --cov=server --cov-report=term-missing

## Assignment Requirements

✅ **aiohttp server implemented**
- 5 endpoints for data operations
- Pydantic validation
- Error handling
- Logging

✅ **aiohttp client implemented**
- Manual client (`client/simple_client.py`)
- Auto-generated client (`client/generated/`)

✅ **OpenAPI contract generation**
- Complete API specification in `openapi.yaml`
- Describes all endpoints, parameters, and responses

✅ **Client generated from contracts**
- Using `openapi-python-client`
- Full typing and validation

✅ **Tests written**
- 6 server tests
- 4 client tests
- Coverage for all endpoints and error cases

## Technology Stack

- **aiohttp 3.9.5** - Async web framework for server and client
- **pydantic 2.5.0** - Data validation and serialization
- **pytest 7.4.3** - Testing framework
- **pytest-aiohttp 1.0.5** - Fixtures for testing aiohttp apps
- **pytest-cov 4.1.0** - Code coverage measurement
- **openapi-python-client** - Python client generator from OpenAPI spec

## Architectural Decisions

### Data Storage
Uses in-memory storage (dict) for simplicity in test assignment. Production would use database (PostgreSQL, MongoDB, etc.).

### Configuration
Environment variables for flexible deployment across different environments.

### Logging
Structured logging with appropriate levels (INFO, WARNING, ERROR) for production readiness.

### Validation
Pydantic automatically validates incoming data and returns clear errors for invalid inputs.

### Asynchronous Design
Using async/await allows efficient handling of multiple concurrent requests.

### Testing
Comprehensive test coverage ensures API correctness and simplifies refactoring.

## Code Quality

```bash
# Check code style
flake8 server/ client/simple_client.py tests/

# Auto-format code
black server/ client/simple_client.py tests/
```

## Possible Improvements

- Add authentication (JWT)
- Connect database (PostgreSQL + SQLAlchemy)
- Add pagination for `GET /data`
- Add filtering and sorting
- Add rate limiting
- Add structured logging (structlog)
- Dockerize application
- Add CI/CD (GitHub Actions)

## Author

Viktoria Alekseenko
Email: vikkischastie@gmail.com
Telegram: @donnaViktoriia
