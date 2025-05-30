# Sales Forecast Model

## Project Description

Sales forecasting remains a significant challenge in the retail industry. While traditional autoregressive models like **ARIMA** have produced solid results, **LSTM (Long Short-Term Memory)** networks have shown superior performance in recent years due to their ability to model complex, nonlinear, and temporal patterns.

In this project, we aim to predict product sales using features such as product group and sales zone.

The project is being developed in the **Microsoft Fabric** environment using private datasets. To provide clear, reproducible examples, a subset of the data has been anonymized.

## Objective

The primary goal is to implement an LSTM-based sales forecasting model. Given a group of products, the model will predict future sales using historical sales data along with product and zone identifiers.

Due to the project's scope, full implementation will take several weeks. This document outlines ongoing progress, preliminary results, and partial implementations.

---

## Literature Overview

Historically, sales forecasting has been approached using autoregressive models such as **ARIMA**. These models are effective for stationary, linear time series but struggle with more complex and nonlinear patterns.

**LSTM networks** have emerged as a powerful alternative, particularly effective at learning long-term dependencies in time series data. Among LSTM variants, **ConvLSTM (Convolutional LSTM)** has shown promising results in capturing both spatial and temporal patterns, making it ideal for datasets involving multiple zones or regions.


## Literature Results

**Traditional Models (ARIMA)**  
- Preprocessing: Differencing to address non-stationarity  
- Result:  
  - RMSE: **185.6**  
  - MAPE: **13.5%**  
- Limitation: Inability to capture nonlinear behavior in data

**LSTM Models**  
- Superior in identifying long-term dependencies  
- Result:  
  - RMSE: **124.5**  
  - MAPE: **8.9%**

---

## About the Dataset

The dataset includes retail sales information across different time periods for multiple products. Due to confidentiality concerns, we applied several anonymization steps:

> 📁 Anonymization logic is implemented in `anonimize.py`.

### Anonymization Steps:
1. Hashing of `ProductId`, `ZoneId`, and `Group` identifiers.  
2. Injection of controlled noise to obscure exact sales values.  
3. Normalization of sales amounts using scaling techniques.

### Dataset Scope

We are working with a subset of the original dataset consisting of:
- **3 product groups**
- **88 distinct products**

### Sales Table Structure

| Column         | Description                                                   |
|----------------|---------------------------------------------------------------|
| `PeriodNumber` | Time period identifier (sequential)                           |
| `ProductId`    | Anonymized product identifier                                 |
| `ZoneId`       | Anonymized geographic sales zone identifier                   |
| `Sales`        | Sales amount in local currency                                |
| `Group`        | Group classification for the product                          |

---

## ETL Process

The ETL pipeline processes raw data into multiple dataset versions tailored for different modeling scenarios. Each dataset version is optimized for complexity, granularity, and performance.

### Dataset Versions

1. **Simple Sales Series**  
   - Contains data for one product in one zone.  
   - Used as a baseline for initial LSTM modeling.  
   - Example: Group 3, Product ID 28, Zone 23  
   - File: `Simple_Sales_Serie.csv`

2. **Composed Dataset**  
   - Includes two products (Product IDs 2 and 4) across all zones (Zone IDs 1 to 170).  
   - One-hot encoding applied to both `ProductId` and `ZoneId`.
   - File: `data_only_2_products.csv`

3. **Complete Dataset**  
   - Full dataset including 88 products across over 100 zones.  
   - Represents the most complex version for advanced modeling.

---

## Progress, Problems Log, and Comments

As we work toward implementing a ConvLSTM model, we've encountered several challenges. This section outlines our progress, results, and the reasoning behind each decision.

### Approach 1 – Dataset Size Constraints

#### ⚠️ Dataset Size

Using the complete dataset was not feasible within the planned project timeline. Even when limiting it to just 10 products, we generated over **2.8 million rows** with **200 columns** before applying the sequence windowing function.

Running the slicing function to generate input sequences for LSTM took around **20 minutes**, making it impractical to iterate or test multiple models.  
To address this, we reduced the dataset to only two products:  
➡️ `data_only_2_products.csv`

#### 🚧 First LSTM Attempt

We trained a basic LSTM model with the following architecture:
1. LSTM layer with 50 units  
2. Output layer: `Dense(1)`

**Result**:  
The model performed poorly — the **MAPE metric returned INF**, indicating significant issues in data preparation or model configuration.

![alt text](/Images/Preductions_LSTM_Vanilla_1.png)

---

### Data Quality Issues

During the creation of the two-product dataset, we initially selected `product_id_1` and `product_id_2`. However, we discovered that `product_id_2` had missing sales data during several periods.

![alt text](/Images/product_1_missing_dates.png)

We then switched to using `product_id_2` and `product_id_4`, which both have **complete sales time series**.

![alt text](/Images/complete_p2_p4.png)

---

### Still Underperforming: RMSE vs. ARIMA

Even after correcting for product selection, the LSTM model still underperformed:
- LSTM RMSE: **749**
- ARIMA RMSE: **185**

This suggested deeper issues in the data structure or model setup.

---

### 🕵️‍♂️ Zone-Level Data Inspection

Upon visualizing data by product and zone, we found a key problem:

![alt text](/Images/missingValuesZonesP2.png)

Many zones had incomplete data — they showed sales only during a portion of the timeline. This causes:
- Uneven sequence lengths
- Inconsistent model inputs

---

### Next Steps

To move forward, we must address this inconsistency. Options include:
1. **Restrict the dataset** to a time window where all products and zones have complete records.
2. **Fill in missing data** using interpolation or other imputation methods that preserve data integrity.


### Approach 2 – Build a simple LSTM one product - one zone

`lstm_v1.ipynb` contains details of the execution.

I don't lose the focus on reaching a ConvLSTM that learns about products, groups and zones. But I know that the best way to reach that point is understanding and improving step by step. For this reason I'm doing the simplest case: One product, one zone. Using the ➡️ `Simple_Sales_Serie.csv`

After checking if the data is complete we found 34 missing dates, but we decided to keep going.
![alt text](/Images/missingValues_zone32_product28.png)


**Result**:  
The model performed with Test MAPE: 89.18% - so far from a good model (even using ARIMA models as benchmark).

### About the model

The model is still improving the loss, which means that continued training could improve the performance.
The prediction results show that the model is learning the trend but the magnitude of the sales predictions is still too small.

### Next Steps

1. Keep improving this model and build a simple ARIMA model to compare
2. Improve the LSTM until reaching at least the ARIMA model performance
3. Improve the LSTM to a ConvLSTM using the 2 products dataset
4. Once we reach results comparable to literature, we can:
   - Classify our product groups using correlations
   - Test it with real sales data

   


---

## References

[1] F. M. Fukai, D. C. Cavalieri, and F. Z. de Castro, “Long short-term memory neural networks applied in demand forecast in the retail market,” Dec. 2024. DOI: [10.55592/cilamce.v6i06.10158](https://doi.org/10.55592/cilamce.v6i06.10158)

[2] H. Sharma et al., “Enhancement of Sales Forecasting and Prediction with Machine Learning Methods,” *International Research Journal of Computer Science*, vol. 11, no. 11, pp. 641–644, Dec. 2024. DOI: [10.26562/irjcs.2024.v1111.02](https://doi.org/10.26562/irjcs.2024.v1111.02)

[3] P. Singh, D. Sharma, D. Patel, and N. Bose, “Enhancing Sales Forecasting Accuracy Using Machine Learning Algorithms and Time Series Analysis in Predictive Sales Analytics,” *Journal of AI ML Research*, vol. 9, no. 4, 2020.

---

## Acknowledgment

Parts of this documentation were developed with the assistance of [ChatGPT](https://openai.com/chatgpt) by OpenAI and [GitHub Copilot](https://github.com/features/copilot), AI tools used to enhance clarity, structure, and efficiency in documentation.
