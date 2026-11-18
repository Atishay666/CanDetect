# 🛡️ CanDetect AI – Financial Fraud Detection System

An AI-powered financial fraud detection system that uses Machine Learning to identify potentially fraudulent transactions and Generative AI to provide an intelligent fraud analysis summary.

## 🚀 Project Overview

CanDetect AI is a web-based financial fraud detection application developed using Python and Flask.

The system allows users to upload transaction data in CSV format. A trained Machine Learning model analyzes the transactions and classifies them as:

- ✅ Genuine
- 🚨 Fraud

The system also calculates fraud probability, assigns risk levels, displays analytical results, and generates an AI-powered summary using Google Gemini.

## ✨ Features

- 🔐 User Login System
- 📂 CSV Transaction Upload
- 🤖 Machine Learning-based Fraud Detection
- 📊 Fraud vs Genuine Transaction Analysis
- 📈 Fraud Rate Calculation
- ⚠️ Risk Classification
- 🔍 Transaction Search
- 🤖 Google Gemini AI Fraud Analysis
- 📋 Detailed Transaction Results
- 📥 Downloadable Fraud Detection Report
- 📊 Interactive Fraud Distribution Chart
- 🌐 Flask-based Web Interface

## 🧠 Machine Learning

The system uses a trained Machine Learning classification model to detect fraudulent financial transactions.

### Input

The model processes transaction features such as:

- Time
- V1–V28
- Amount

The `Class` column is used as the target label during model training.

### Output

For each transaction, the system generates:

- Prediction
- Fraud Probability
- Risk Level

Example:

| Prediction | Fraud Probability | Risk |
|------------|-------------------|------|
| Genuine | 0.02% | Low |
| Fraud | 99.98% | High |

## 🤖 Generative AI Integration

Google Gemini is integrated into the application to generate an intelligent summary of the fraud analysis.

The AI summary considers:

- Total transactions
- Fraudulent transactions
- Genuine transactions
- Fraud rate
- Overall fraud risk

The Gemini API key is loaded securely using an environment variable.

```powershell
$env:GEMINI_API_KEY="YOUR_API_KEY"