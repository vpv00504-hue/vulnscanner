# VulnScanner: Graph Neural Network-Based Software Vulnerability Detection

## Overview

VulnScanner is an AI-powered software vulnerability detection system that uses Graph Neural Networks (GNNs) to identify vulnerable source code. The project combines machine learning, graph-based code representation, and an interactive web interface to help analyze source code for potential security vulnerabilities.

The system consists of:

* Python backend for model inference
* Graph Neural Network vulnerability detection model
* React-based frontend interface
* Pre-trained vulnerability detection models
* Dataset processing and graph generation pipeline

---

## Features

* Detects vulnerable source code using Graph Neural Networks
* Interactive web interface for code submission
* AI-powered vulnerability analysis
* Pre-trained model support
* Dataset preprocessing pipeline
* Modern React frontend
* Python backend API
* Extensible architecture for future vulnerability datasets

---

## Project Structure

```text
vulnscanner/
│
├── backend/              # Backend API
├── models/               # Trained GNN models
├── scripts/              # Training and preprocessing scripts
├── utils/                # Utility functions
├── vuln-ui/              # React frontend
├── data/                 # Dataset files
├── final_model.pth       # Trained model
└── README.md
```

---

## Technology Stack

### Backend

* Python
* PyTorch
* PyTorch Geometric
* Flask/FastAPI (depending on implementation)

### Frontend

* React
* JavaScript
* Tailwind CSS

### Machine Learning

* Graph Neural Networks (GNN)
* Code Property Graphs
* Deep Learning

---

## Installation

### Clone Repository

```bash
git clone https://github.com/vpv00504-hue/vulnscanner.git
cd vulnscanner
```

### Create Virtual Environment

```bash
python -m venv venv
```

Activate environment:

**Windows**

```bash
venv\Scripts\activate
```

### Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Install Frontend Dependencies

```bash
cd vuln-ui
npm install
```

---

## Running the Project

### Start Backend

```bash
cd backend
python app.py
```

### Start Frontend

Open another terminal:

```bash
cd vuln-ui
npm start
```

Frontend:

```text
http://localhost:3000
```

---

## Model Information

The project includes pre-trained vulnerability detection models:

* final_model.pth
* models/saved/best_model.pth

These models are used for inference and vulnerability classification.

---

## Dataset

The project utilizes vulnerability datasets represented as graph structures for Graph Neural Network training and evaluation.

Dataset files are located in:

```text
data/
```

---

## Future Improvements

* Multi-language vulnerability detection
* Explainable AI for vulnerability reasoning
* Real-time code analysis
* Cloud deployment
* CI/CD integration
* Additional vulnerability datasets
* Model performance optimization

---

## Author

Achu

B.Tech Computer Science Engineering

Graph Neural Network Research & Software Security Enthusiast

---

## License

This project is intended for educational and research purposes.
