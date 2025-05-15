# 🧠 Rule-Based Segmentation for Customer Profitability

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)
[![Kaggle](https://img.shields.io/badge/Kaggle-Profile-blue.svg)](https://www.kaggle.com/code/fatiherencetin/telco-customer-churn)

## 📌 Project Description

This project implements a rule-based segmentation strategy to estimate the potential profitability of new customers based on historical sales data. The goal is to create **level-based personas**, segment them according to average value, and estimate how much revenue future customers might bring.

Inspired by a real business case from Gezinomi, the project uses a dataset containing hotel booking data, such as city, concept type, season, and booking lead time.

---

## 📊 Dataset Overview

The dataset contains the following fields:

| Feature              | Description                                      |
|----------------------|--------------------------------------------------|
| `SaleId`             | Unique sale ID                                          |
| `SaleDate`           | Date of sale                                     |
| `CheckInDate`        | Customers' checkin date to hotel                 |
| `Price`              | Paid price for the booking                       |
| `ConceptName`        | Hotel concept (e.g. "Herşey Dahil")              |
| `SaleCityName`       | City where the hotel is located                  |
| `CInDay`             | Day of the week the customer checks in           |
| `SaleCheckInDayDiff` | Days between booking and check-in                |
| `Seasons`            | Season type: Low / High                          |


---

## 🧩 Business Logic & Tasks

The key business questions addressed:

- What are the average profits across city/concept/season combinations?
- How to segment customers based on **purchase behavior (early/late)**?
- How to define personas using multiple categorical attributes?
- What is the expected value (mean price) of a persona?
- In which segment does a given customer fall?

---

## ⚙️ Rule-Based Classification Steps

1. **Data Exploration and Cleaning**
2. **Time Window Categorization**:  
   `SaleCheckInDayDiff → EB_Score` with labels:  
   - `Last Minuters`: 0–7  
   - `Potential Planners`: 8–30  
   - `Planners`: 31–90  
   - `Early Birds`: 91-180
   - `Promotioners`: >180
3. **Aggregations**:
   - Mean price and count for grouped attributes
4. **Level-Based Persona Creation**:
   - Concatenated columns: `City_Concept_Season`
5. **Segmentation**:
   - Based on quartiles of `Price`
6. **Prediction Example Queries**:
   - Estimate expected revenue from a given persona

---

## 📈 Sample Output

| Persona                          | Segment | Avg. Price |
|----------------------------------|---------|------------|
| ANTALYA_HERŞEY DAHIL_HIGH        | A       | 103.94     |
| GIRNE_YARIM PANSIYON_LOW         | C       | 75.80      |
| DİĞER_HERŞEY DAHIL_LOW           | B       | 87.31      |

---

## 🛠 Tech Stack

- Python
- Pandas
- Jupyter Notebook
- Rule-Based Business Logic

---

## 📄 License

MIT License. See `LICENSE` file for details.

---

## 📫 Contact

Feel free to reach out:

<p align="left">
  <a href="www.linkedin.com/in/fatih-eren-cetin" target="_blank"  rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/LinkedIn-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" height="30" />
  </a>
  
  <a href="https://medium.com/@fecetinn" target="_blank"  rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Medium-12100E?style=for-the-badge&logo=medium&logoColor=white" alt="Medium" height="30" />
  </a>
  
  <a href="https://www.kaggle.com/fatiherencetin" target="_blank"  rel="noopener noreferrer">
    <img src="https://img.shields.io/badge/Kaggle-20BEFF?style=for-the-badge&logo=kaggle&logoColor=white" alt="Kaggle" height="30" />
  </a>
</p>

---

## 🔮 Future Extensions

- Add Streamlit dashboard for persona lookup
- Compare with clustering-based segmentation (e.g. KMeans)
