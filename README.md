# Stocks Serverless Pipeline

A fully automated **serverless data pipeline** that tracks a curated watchlist of technology stocks and identifies the daily top mover. The system is built end-to-end on AWS using serverless services, Infrastructure as Code with Terraform, and a React frontend.

The pipeline automatically ingests stock data, calculates daily percentage changes, stores results, and displays the history on a publicly hosted dashboard.

---

# Overview

The system tracks the following watchlist:

```
AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA
```

Each day the pipeline:

1. Fetches open and close prices for each stock
2. Calculates the daily percentage change
3. Identifies the stock with the **largest absolute movement**
4. Stores the result in DynamoDB
5. Displays the historical results through a public dashboard

This project demonstrates practical experience with:

* Serverless architecture
* Infrastructure as Code
* Cloud-native event-driven design
* Simple frontend data visualization


### Key Design Decisions

**Separation of concerns**

The ingestion pipeline (scheduled Lambda) is separated from the API retrieval logic used by the frontend.

**Serverless-first design**

All infrastructure uses managed AWS services to minimize operational overhead and remain within the AWS Free Tier.

**Fault tolerance**

The Lambda functions include error handling so individual failures do not interrupt the pipeline.

---

# Technical Stack

## Backend

* Python 3.11
* AWS Lambda
* Massive API for stock data
* DynamoDB for storage

Dependencies are defined in:

```
requirements.txt
```

Example dependencies:

```
boto3
massive
```

## Frontend

* React with Vite
* Fetch API for data retrieval
* Hosted via AWS S3 Static Website Hosting

Features include:

* Card display of recent stock movers
* Color-coded performance indicators

  * Green = gain
  * Red = loss

## Infrastructure

Provisioned using **Terraform**:

* AWS Lambda
* DynamoDB
* EventBridge
* API Gateway
* S3 static hosting

---

# Features

* Automated daily ingestion of stock data
* Identification of the stock with the largest percentage movement
* Persistent historical storage in DynamoDB
* REST API for retrieving the last 7 days of results
* Publicly hosted dashboard
* Fully reproducible infrastructure via Terraform

Stored data format:

```
Date
Ticker
Percent Change
Closing Price
```

---

# Project Structure

```
Pennymac-Stocks-Serverless-Pipeline

terraform/
  api_gateway.tf
  backend.tf
  dynamodb.tf
  eventbridge.tf
  frontend.tf
  lambda_ingestion.tf
  lambda_api.tf
  iam.tf
  main.tf
  provider.tf
  outputs.tf
  variables.tf

lambda/
  ingestion/
  retrieval/

frontend/
  src/

requirements.txt

README.md
```

---

# Setup & Deployment

## 1 Clone the repository

```
git clone https://github.com/crissa-owens/Pennymac-Stocks-Serverless-Pipeline.git
cd Pennymac-Stocks-Serverless-Pipeline
```

---

## 2 Install Python dependencies

```
pip install -r requirements.txt
```

---

## 3 Configure environment variables

The Lambda function requires:

```
MASSIVE_API_KEY
TABLE_NAME
```

Example:

```
export MASSIVE_API_KEY=<your_massive_api_key>
export TABLE_NAME=<dynamodb_table_name>
```

Secrets (MASSIVE_API_KEY) should **never be committed to the repository**.

---

## 4 Deploy infrastructure

```
cd terraform
terraform init
terraform apply
```

Terraform provisions:

* Lambda functions
* DynamoDB tables
* EventBridge schedule
* API Gateway endpoints
* S3 frontend hosting

---

## 5 Deploy frontend

From the frontend directory:

```
npm install
npm run build
```

Upload the build to S3:

```
aws s3 sync dist/ s3://crissa-stock-dashboard
```

---

# API Usage

### Endpoint

```
GET /movers
```

### Example Response

```
[
  {
    "date": "2026-03-03",
    "ticker": "NVDA",
    "percent_change": 4.21,
    "closing_price": 890.13
  }
]
```

The frontend retrieves this endpoint and renders the most recent 7 days of top movers.

---

# Usage

* EventBridge triggers the ingestion Lambda once per day
* Lambda calculates the largest stock movement
* Results are written to DynamoDB
* The frontend fetches the latest data from the API and renders it dynamically

---

# Trade-offs & Design Decisions

### DynamoDB

Chosen for its seamless integration with Lambda and ability to scale without infrastructure management.

### Scheduled Lambda

EventBridge provides a reliable scheduling mechanism without running persistent compute resources.

### S3 Static Hosting

A simple and cost-effective way to deploy a single-page application within the AWS Free Tier.

---

# Potential Improvements

If extended beyond the interview scope:

* Add **CloudFront CDN** for global frontend delivery
* Implement **API caching** via API Gateway
* Add **structured logging and monitoring** with CloudWatch dashboards
* Expand watchlist or support user-configurable stocks

---

## AI Assistance Disclosure

Some limited assistance from generative AI tools was used during development for tasks such as:

- Drafting documentation and README
- Debugging infrastructure configuration issues
- Optimizing Ingestion and API handlers

All architectural decisions, implementation, and deployment of the system were completed and validated manually.

---

# Demo

GitHub Repository
[https://github.com/crissa-owens/Pennymac-Stocks-Serverless-Pipeline](https://github.com/crissa-owens/Pennymac-Stocks-Serverless-Pipeline)

Live Dashboard
[http://crissa-stock-dashboard.s3-website-us-east-1.amazonaws.com/](http://crissa-stock-dashboard.s3-website-us-east-1.amazonaws.com/)

---

## Credits

- Stock market icon used for the site favicon, sourced from FreePNGImg.

---

# Final Notes

This project was developed as a technical challenge to demonstrate practical experience with:

* AWS serverless architecture
* Infrastructure as Code
* Cloud-native event-driven pipelines
* Lightweight frontend visualization

All infrastructure is reproducible via Terraform and runs comfortably within the AWS Free Tier.
