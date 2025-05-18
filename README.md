# Sales Forecast Model

## About the Dataset

The dataset contains retail sales information for various products over a series of time periods.

To maintain data confidentiality, the dataset has been anonymized through the following steps:

1. Hashing the product and zone identifiers.  
2. Injecting noise into the data to obscure exact values.  
3. Scaling product sales values for normalization.

### Dataset Structure

The dataset is composed a table, with the main table described below:

#### **Sales Table**

- **PeriodNumber**: Represents the chronological order of the time period in which the product was sold.  
- **ProductId**: An anonymized identifier for the product.  
- **ZoneId**: An anonymized identifier for the geographical sales zone.  
- **Sales**: The sales amount (local currency) for the corresponding product and period.


---

## Acknowledgment

Parts of this documentation were developed with the assistance of [ChatGPT](https://openai.com/chatgpt) by OpenAI and [GitHub Copilot](https://github.com/features/copilot), AI tools used to enhance clarity, structure, and writing efficiency.