#DF structure SUBCATEGORIA, ITEM, ITEM_DESC
import json
from pyspark.sql.functions import concat, lit, row_number
from pyspark.sql.window import Window
import os
from datetime import datetime

def anonimizeColumn(df, original_column_name, anonymized_column_name, prefix):

    window = Window.orderBy(original_column_name)
    distinct_vals = df.select(original_column_name).distinct().withColumn(
        anonymized_column_name, concat(lit(prefix), row_number().over(window))
    )

    # Join to add anonymized column
    df = df.join(distinct_vals, on=original_column_name, how="left")

    # Create mapping dictionary (anonymized -> original)
    mapping_dict = {row[anonymized_column_name]: row[original_column_name] for row in distinct_vals.collect()}

    return df, mapping_dict


def anonimize_catalog(df):
    # Anonymize SUBCATEGORIA column
    df, subcategory_map = anonimizeColumn(df, "GROUP_COLUMN_NAME", "Group", "g")
    # Anonymize ITEM column
    df, item_map = anonimizeColumn(df, "PRODUCT_ID_COLUMN_NAME", "ProductId", "p")
    return df, item_map, subcategory_map


def save_dict_to_json(data_dict, file_path, meta_info=None):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    output = {
        "meta": {
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        "mapping": data_dict
    }

    if meta_info:
        output["meta"].update(meta_info)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)


def load_dict_from_json(file_path):

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    mapping = data.get("mapping", {})
    meta = data.get("meta", {})
    return mapping, meta


anon_df ,item_map, subcat_map=anonimize_catalog(df_original_catalog)
print(anon_df.columns)
save_dict_to_json(item_map,"Files/MODELS/item_map.json")
save_dict_to_json(subcat_map,"Files/MODELS/subcat.json")

print(load_dict_from_json("Files/MODELS/item_map.json"))



from pyspark.sql.functions import col, min, max, randn, when, lit, datediff

def add_days_since_first_date(df, date_col="anonimized_date"):
    # 1. Obtener la fecha mínima
    min_date = df.select(min(col(date_col))).collect()[0][0]
    print("MIN DATE IS: ",min_date)
    df_with_days = df.withColumn(
        "date_num",
        datediff(col(date_col), lit(min_date))
    )
    
    return df_with_days

def normalize_sales(df):
    # 1. Get min and max of Sales_$ column
    stats = df.agg(
        min(col("Sales_$")).alias("min_val"),
        max(col("Sales_$")).alias("max_val")
    ).collect()[0]

    min_val = stats["min_val"]
    max_val = stats["max_val"]

    # 2. Handle case when all values are equal (avoid division by zero)
    if max_val == min_val:
        df = df.withColumn("Sales", lit(0.5))  # assign neutral mid-value
    else:
        # 3. Normalize Sales_$ to [0, 1]
        df = df.withColumn(
            "Sales",
            (col("Sales_$") - lit(min_val)) / (lit(max_val) - lit(min_val))
        )

        # 4. Add Gaussian noise (std ~ 3%)
        df = df.withColumn("Sales", col("Sales") + randn() * 0.03)

        # 5. Clip values to keep them in [0, 1]
        df = df.withColumn(
            "Sales",
            when(col("Sales") < 0, 0)
            .when(col("Sales") > 1, 1)
            .otherwise(col("Sales"))
        )

    return df

def anonimize_df(anonimized_catalog):
    product_ids = [row['PRODUCT_ID_COLUMN_NAME'] for row in anonimized_catalog.select("PRODUCT_ID_COLUMN_NAME").distinct().collect()]
    
    # Convertir la lista a un string para usar en SQL IN, cuidando formato de comillas
    product_ids_str = ", ".join(f"'{pid}'" for pid in product_ids)
    # Construir query SQL
    query = f"""
        SELECT date, PRODUCT_ID_COLUMN_NAME, ZONE_ID_COLUMN_NAME, `Sales_$`
        FROM fact_sales
        WHERE PRODUCT_ID_COLUMN_NAME IN ({product_ids_str})
        AND Base = 'FISICO'
    """
    
    # Ejecutar query y retornar DataFrame filtrado
    df = spark.sql(query)
    df, zone_map = anonimizeColumn(df, "ZONE_ID_COLUMN_NAME", "ZoneId", "z")
    save_dict_to_json(zone_map,"Files/MODELS/store.json")
    df=add_days_since_first_date(df, date_col="Date")
        # 5. Unir con el catálogo anonimizado (por PRODUCT_ID_COLUMN_NAME = PRODUCT_ID_COLUMN_NAME)
    df = df.join(
        anonimized_catalog.select("PRODUCT_ID_COLUMN_NAME", "ProductId", "Group"),
        df.PRODUCT_ID_COLUMN_NAME == anonimized_catalog.PRODUCT_ID_COLUMN_NAME,
        how="left"
    )
    
    df=normalize_sales(df)

    df=df.select("date","date_num", "Group", "ProductId", "ZoneId", "Sales_$")
    print(df.columns)
    return df