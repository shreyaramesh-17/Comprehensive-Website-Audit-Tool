# 🕵️‍♂️ Comprehensive Website Audit Tool

[![Python](https://img.shields.io/badge/Python-3.x-blue)](https://www.python.org/) 
[![Flask](https://img.shields.io/badge/Flask-2.x-green)](https://flask.palletsprojects.com/) 
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Issues](https://img.shields.io/github/issues/shreyaramesh-17/Comprehensive-Website-Audit-Tool)](https://github.com/shreyaramesh-17/Comprehensive-Website-Audit-Tool/issues)

A **Flask-based web application** that audits websites for **security**, **performance**, **SEO**, and **accessibility** issues. It generates a professional PDF report with actionable findings and suggestions for improvement. Perfect for developers, auditors, and website owners.

---

## 🚀 Features

- 🔒 **Security Audits**: HTTPS checks, HTTP headers (`CSP`, `HSTS`), XSS detection  
- ⚡ **Performance Metrics**: Page load speed, bottleneck detection  
- 📈 **SEO Audits**: Metadata, sitemap, robots.txt, heading hierarchy  
- ♿ **Accessibility Checks**: Form labels, alt text, semantic HTML validation  
- 📄 **PDF Reports**: Summarized results with severity levels and remediation suggestions  

---


## 🛠️ Getting Started

### Prerequisites

- Python 3.x  
- pip  
- (Optional) Virtual environment (`venv` / `virtualenv`)  

### Installation

```bash
# Clone the repository
git clone https://github.com/shreyaramesh-17/Comprehensive-Website-Audit-Tool.git
cd Comprehensive-Website-Audit-Tool

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate

export FLASK_APP=app.py       # Linux/Mac
set FLASK_APP=app.py          # Windows
export FLASK_ENV=development
flask run


# Install dependencies
pip install -r requirements.txt
