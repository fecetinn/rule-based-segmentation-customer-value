# 🧠 Rule-Based Segmentation for Customer Profitability

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)

## 📌 Project Description

This project implements a rule-based segmentation strategy to estimate the potential profitability of new customers based on historical sales data. The goal is to create **level-based personas**, segment them according to average value, and estimate how much revenue future customers might bring.

Inspired by a real business case from Gezinomi, the project uses a dataset containing hotel booking data, such as city, concept type, season, and booking lead time.

---

## 📚 Dataset Overview

The dataset contains the following fields:

| Feature              | Description                                      |
|----------------------|--------------------------------------------------|
| `SaleId`             | Unique sale ID                                   |
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
   - `Last_Minuters`: 0–7  
   - `Potential_Planners`: 8–30  
   - `Planners`: 31–90  
   - `Early_Birds`: 91-180
   - `Promotioners`: >180
3. **Aggregations**:
   - Mean price and count for grouped attributes
4. **Level-Based Persona Creation**:
   - Concatenated columns: `City`, `ConceptName` and `Season` as `sales_level_based`
5. **Segmentation**:
   - Based on quartiles of `Price`
6. **Prediction Example Queries**:
   - Estimate expected revenue from a given persona

---


## 📊 Segment Summary Table

After assigning customer personas to segments (A–D) based on average `Price`, we summarized each segment's financial characteristics:

| Segment | Avg. Value | Min. Value | Max. Value | Total Value |
|---------|------------|------------|------------|--------------|
| A       | 110.15     | 77.96      | 4880.47    | 1.628840e+06 |
| B       | 64.97      | 54.26      | 77.96      | 9.607300e+05 |
| C       | 44.59      | 35.34      | 54.26      | 6.596030e+05 |
| D       | 25.65      | 0          | 35.34      | 3.794480e+05 |

> These results allow decision-makers to understand the revenue potential and variability within each segment, helping to optimize marketing and targeting strategies.

---

## 🔍 Estimating Profitability for New Customers

The project includes a utility function called `estimate_segment_value()` that allows you to simulate the expected profitability of any new customer based on their persona string (e.g., `"ANTALYA_HERŞEY DAHIL_HIGH"`).

### 🧪 Sample Usage

```python
segment, estimate_df = estimate_segment_value(agg_df, "antalya_herşey dahil_low") # Enter `persona` as your desire.
```

## 📈 Sample Output

```python
ANTALYA_HERŞEY DAHIL_LOW: 
   Segment   Avg_Value  Min_Value   Max_Value   Total_Value
3       A  110.153543  77.962578  4880.47138  1.628840e+06
```

---

## 🛠 Tech Stack

- Python
- Pandas
- Jupyter Notebook
- Rule-Based Business Logic

---

## 📄 License

MIT License. See `LICENSE` file for details.

Feel free to contribute to this project by submitting issues or pull requests. Your contributions are welcome!

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
