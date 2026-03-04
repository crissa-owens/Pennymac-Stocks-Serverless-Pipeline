# Stocks Serverless Pipeline

A fully automated serverless pipeline that tracks a curated watchlist of tech stocks and identifies the daily top mover. Built end-to-end on AWS using serverless technologies, Terraform, and a clean SPA frontend.

---

## Table of Contents

* [Overview](#overview)
* [Architecture](#architecture)
* [Technical Stack](#technical-stack)
* [Features](#features)
* [Setup & Deployment](#setup--deployment)
* [Usage](#usage)
* [Trade-offs & Notes](#trade-offs--notes)
* [Demo](#demo)

---

## Overview

The TRE Team requires a daily dashboard showing which stock moved the most (up or down) among a select watchlist:

```text
AAPL, MSFT, GOOGL, AMZN, TSLA, NVDA
```

This project demonstrates:

* **Serverless Architecture**: AWS Lambda, DynamoDB, EventBridge, API Gateway
* **Infrastructure as Code (IaC)**: Terraform
* **Frontend Visualization**: SPA hosted on AWS S3/Amplify

The system is fully automated to fetch market data, calculate daily percentage changes, persist results, and display the top movers.

---

## Architecture

```
EventBridge (Daily Cron)
          │
          ▼
     Lambda Function
          │
          ▼
    Fetch stock prices (Massive API)
          │
          ▼
   Calculate % change → Identify top mover
          │
          ▼
      DynamoDB Table
          │
          ▼
API Gateway REST API (GET /movers)
          │
          ▼
    Frontend SPA (S3/Amplify)
```

Key design decisions:

* Separation of **Ingestion** (daily stock processing) and **Retrieval** (API endpoint for frontend)
* Error handling in Lambda ensures pipeline continues if a stock fails or API rate limits occur
* Fully modular Terraform code to provision and manage all AWS resources

---

## Technical Stack

**Backend**:

* Python 3.x, AWS Lambda
* Massive API for stock data
* DynamoDB for storage

**Frontend**:

* React SPA (or vanilla JS/Next/Vue)
* Fetches `/movers` endpoint to display last 7 days of top movers
* Color-coded gain/loss visualization

**Infrastructure**:

* Terraform (AWS Free Tier resources)
* EventBridge Cron for Lambda scheduling
* API Gateway for REST API

---

## Features

* Automated daily calculation of the stock with the largest absolute percent change
* Persistent storage in DynamoDB: Date, Ticker, Percent Change, Closing Price
* REST API exposing the last 7 days of top movers
* Simple SPA frontend with color-coded results (green for gains, red for losses)
* Fully IaC-compliant, reproducible stack

---

## Setup & Deployment

1. **Clone Repository**

```bash
git clone https://github.com/crissa-owens/Pennymac-Stocks-Serverless-Pipeline.git
cd pennymac-stocks-serverless-pipeline
```

2. **Set Environment Variables** (for Lambda)

```bash
export MASSIVE_API_KEY=<your_massive_api_key>
export TABLE_NAME=<dynamodb_table_name>
```

3. **Deploy Infrastructure** (Terraform)

```bash
cd terraform
terraform init
terraform apply
```

4. **Upload Frontend**

* Build SPA: `npm run build`
* Deploy to S3 or AWS Amplify

5. **Verify**

* Lambda is scheduled via EventBridge
* API Gateway endpoint `/movers` returns last 7 days of top movers

---

## Usage

* The Lambda function automatically runs daily
* The SPA fetches `/movers` to display a table or card view of top movers
* Green/Red coloring indicates positive/negative percentage change

---

## Trade-offs & Notes

* Limited to **AWS Free Tier** resources; minimal scaling tested
* Massive API chosen for simplicity and free access; handles small watchlist efficiently
* Frontend kept simple to focus on architecture and serverless design
* Error handling ensures partial failures do not break daily ingestion

---

## Demo

* GitHub Repo: [https://github.com/crissa-owens/Pennymac-Stocks-Serverless-Pipeline.git](https://github.com/crissa-owens/Pennymac-Stocks-Serverless-Pipeline.git)
* Live Frontend: [YourS3OrAmplifyURL]