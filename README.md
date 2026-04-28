# Illumina Expert System (Rule-Based Decision Support System)
A Django-based rule engine for structured quotation decision-making

## Overview
This project is a rule-based decision support system developed using Django to assist in quotation evaluation for advertising services.  
The system improves consistency in pricing decisions by applying structured rules based on job parameters.

---

## Features
- Pricing tier recommendation (Basic / Standard / Premium)  
- Margin range suggestion  
- Risk-based review levels  
- Explanation generation for each recommendation  
- Role-based workflow (Admin, Salesperson)  
- Public enquiry interface for customer input  

---

## How It Works
The system uses a scoring-based rule engine where inputs such as:
- job size  
- urgency  
- materials  
- installation requirements  

contribute to a total score.

Based on this score, the system generates:
- pricing tier  
- margin range  
- review requirement level  

The system follows a **human-in-the-loop approach**, where recommendations assist decision-making while final approval remains with the admin.

---

## Tech Stack
- Python  
- Django  
- SQLite  

---

## Project Structure
Core rule logic and services are located in:  
`quotes/services/`

---

## Documentation
Full project report is available in this repository: 
'Project Report.pdf'

---

## Note
This project was developed as part of an academic assignment.  
The repository focuses on demonstrating backend logic and system design.
