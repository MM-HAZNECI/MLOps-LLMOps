# Customer Service Request Classification System

Developed as part of the MLOps-LLMOps Bootcamp.

## Objective
This system automatically classifies, prioritizes, and extracts tags from customer service requests using Google Gemini AI and stores the results in a PostgreSQL database.

## Prerequisites
- Docker & Docker Compose
- Python 3.12 (uv recommended)
- Google Gemini API Key

## Setup Instructions

### 1. Environment Variables
Create a \`.env\` file in the root directory with the following content:
\`\`\`env
GOOGLE_API_KEY=your_actual_api_key_here
DB_URL=postgresql://myuser:mypassword@localhost:5432/customer_service
\`\`\`

### 2. Database Setup
Launch the PostgreSQL database using Docker Compose:
\`\`\`bash
docker compose up -d
\`\`\`

### 3. Installation
Install the required dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 4. Running the Application
Run the main processing script:
\`\`\`bash
python main.py
\`\`\`

## System Architecture
- **Data Source**: \`data/sample_requests.csv\`
- **Database**: PostgreSQL (2 tables: \`customer_requests\`, \`request_classifications\`)
- **LLM**: Google Gemini (via LangChain Agent)
- **Framework**: SQLModel & Pydantic

## Querying Results
To view the classified results:
\`\`\`bash
docker exec -it odev4_postgres psql -U myuser -d customer_service -c "SELECT * FROM request_classifications;"
\`\`\`
