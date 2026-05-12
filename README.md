# 📊 Mobile Phones Data Analysis  

This repository contains an exploratory data analysis (EDA) of mobile phone specifications, including pricing, RAM, battery capacity, weight, and screen size. The analysis is performed using **Python, Pandas, Seaborn, and Matplotlib**, providing insights into the correlation between different attributes and their impact on mobile phone trends.  

---
Dataset Link: https://www.kaggle.com/datasets/abdulmalik1518/mobiles-dataset-2025
## 📌 Objective  
The primary goal of this analysis is to:  
✅ Understand price variations across different countries.  
✅ Identify trends in battery capacity and RAM sizes.  
✅ Examine the relationship between screen size and mobile weight.  
✅ Compute the correlation between numerical attributes.  

---

## 🛠 Dataset Description  
The dataset consists of various features related to mobile phones, such as:  
- 📌 **Company Name** – Manufacturer (Apple, Samsung, Xiaomi, etc.)  
- 📌 **RAM** – Available RAM in GB (2GB, 4GB, 8GB, etc.)  
- 📌 **Battery Capacity** – Battery power in mAh  
- 📌 **Screen Size** – Display size in inches  
- 📌 **Mobile Weight** – Weight of the device in grams  
- 📌 **Launched Price** – Initial price in different currencies  

---

## 📊 Key Analyses and Visualizations  

### 🔹 1. Price Distribution Across Countries  
A **boxplot** visualizes the price distribution across multiple countries to compare pricing strategies.  

✔ **Key Finding:** Some brands have a significant variation in pricing across different markets.  

---

### 🔹 2. RAM vs Battery Capacity  
A **scatter plot** showcases how battery capacity changes with different RAM configurations.  

✔ **Observation:** Higher RAM models generally feature larger battery capacities, but exceptions exist.  

---

### 🔹 3. Screen Size vs Mobile Weight  
A **scatter plot** reveals trends in screen size and mobile weight, indicating whether larger screens result in heavier devices.  

✔ **Insight:** While bigger screens tend to be heavier, some brands optimize weight despite larger displays.  

---

### 🔹 4. Correlation Heatmap  
A **correlation heatmap** displays the relationships between numerical attributes.  

✔ **Findings:**  
📌 Strong correlation observed between **battery capacity and RAM**.  
📌 **Screen size and weight** show a moderate correlation.  

---

## 📂 Files in the Repository  
- 📄 **Mobile_Data_Analysis.ipynb** → Jupyter Notebook containing the analysis.  
- 📊 **data.csv** → The dataset used for analysis.  
- 📈 **Visualizations/** → Folder containing generated graphs.  

---

## 🚀 How to Use This Repository  

1️⃣ Clone the repository:  
```bash
git clone https://github.com/your-username/mobile-data-analysis.git
