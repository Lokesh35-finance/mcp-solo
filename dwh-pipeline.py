"""
ETL Script Example
Reads from PostgreSQL, Oracle, MySQL, and XML
Applies business rules
Combines into a unified dataset
Exports to Excel
>200 lines
"""

import psycopg2
import cx_Oracle
import mysql.connector
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
import os

# ==============================
# CONFIGURATION
# ==============================
CONFIG = {
    "postgres": {
        "host": "localhost",
        "database": "finance",
        "user": "postgres_user",
        "password": "postgres_pass"
    },
    "oracle": {
        "dsn": "localhost/XE",
        "user": "oracle_user",
        "password": "oracle_pass"
    },
    "mysql": {
        "host": "localhost",
        "database": "sales",
        "user": "mysql_user",
        "password": "mysql_pass"
    },
    "xml_file": "customers.xml",
    "output_excel": "combined_etl_output.xlsx"
}

# ==============================
# DATA EXTRACTION FUNCTIONS
# ==============================

def extract_postgres():
    """Extract data from PostgreSQL"""
    conn = None
    try:
        conn = psycopg2.connect(
            host=CONFIG["postgres"]["host"],
            database=CONFIG["postgres"]["database"],
            user=CONFIG["postgres"]["user"],
            password=CONFIG["postgres"]["password"]
        )
        cursor = conn.cursor()
        cursor.execute("SELECT id, customer_name, amount, transaction_date FROM transactions;")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=["id", "customer_name", "amount", "transaction_date"])
        return df
    except Exception as e:
        print("Postgres Error:", e)
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()


def extract_oracle():
    """Extract data from Oracle"""
    conn = None
    try:
        conn = cx_Oracle.connect(
            CONFIG["oracle"]["user"],
            CONFIG["oracle"]["password"],
            CONFIG["oracle"]["dsn"]
        )
        cursor = conn.cursor()
        cursor.execute("SELECT order_id, product_name, quantity, order_date FROM orders")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=["order_id", "product_name", "quantity", "order_date"])
        return df
    except Exception as e:
        print("Oracle Error:", e)
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()


def extract_mysql():
    """Extract data from MySQL"""
    conn = None
    try:
        conn = mysql.connector.connect(
            host=CONFIG["mysql"]["host"],
            database=CONFIG["mysql"]["database"],
            user=CONFIG["mysql"]["user"],
            password=CONFIG["mysql"]["password"]
        )
        cursor = conn.cursor()
        cursor.execute("SELECT invoice_id, region, total_value, invoice_date FROM invoices")
        rows = cursor.fetchall()
        df = pd.DataFrame(rows, columns=["invoice_id", "region", "total_value", "invoice_date"])
        return df
    except Exception as e:
        print("MySQL Error:", e)
        return pd.DataFrame()
    finally:
        if conn:
            conn.close()


def extract_xml():
    """Extract data from XML file"""
    try:
        tree = ET.parse(CONFIG["xml_file"])
        root = tree.getroot()
        records = []
        for customer in root.findall("customer"):
            cid = customer.find("id").text
            name = customer.find("name").text
            country = customer.find("country").text
            signup = customer.find("signup_date").text
            records.append((cid, name, country, signup))
        df = pd.DataFrame(records, columns=["id", "name", "country", "signup_date"])
        return df
    except Exception as e:
        print("XML Error:", e)
        return pd.DataFrame()

# ==============================
# TRANSFORMATION / BUSINESS RULES
# ==============================

def transform_postgres(df):
    """Apply transformations on Postgres data"""
    if df.empty:
        return df
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["amount_usd"] = df["amount"].astype(float) * 1.0  # Assume already USD
    return df


def transform_oracle(df):
    """Apply transformations on Oracle data"""
    if df.empty:
        return df
    df["order_date"] = pd.to_datetime(df["order_date"])
    df["total_items"] = df["quantity"].astype(int)
    return df


def transform_mysql(df):
    """Apply transformations on MySQL data"""
    if df.empty:
        return df
    df["invoice_date"] = pd.to_datetime(df["invoice_date"])
    df["tax"] = df["total_value"].astype(float) * 0.18  # assume 18% tax
    df["net_value"] = df["total_value"].astype(float) + df["tax"]
    return df


def transform_xml(df):
    """Apply transformations on XML data"""
    if df.empty:
        return df
    df["signup_date"] = pd.to_datetime(df["signup_date"])
    df["is_active"] = df["signup_date"].apply(lambda x: x.year >= 2020)
    return df

# ==============================
# COMBINE ALL DATA
# ==============================

def combine_data(pg_df, ora_df, my_df, xml_df):
    """Combine all datasets into a unified structure"""
    combined = {}
    combined["postgres"] = pg_df
    combined["oracle"] = ora_df
    combined["mysql"] = my_df
    combined["xml"] = xml_df

    # Example business logic: summary metrics
    summary = {
        "total_transactions": len(pg_df),
        "total_orders": len(ora_df),
        "total_invoices": len(my_df),
        "total_customers": len(xml_df),
        "total_revenue": my_df["net_value"].sum() if not my_df.empty else 0
    }

    return combined, summary

# ==============================
# LOAD TO EXCEL
# ==============================

def load_to_excel(combined, summary):
    """Write data and summary to Excel file"""
    with pd.ExcelWriter(CONFIG["output_excel"]) as writer:
        for key, df in combined.items():
            df.to_excel(writer, sheet_name=key, index=False)
        # Summary sheet
        summary_df = pd.DataFrame([summary])
        summary_df.to_excel(writer, sheet_name="Summary", index=False)
    print(f"Excel file created: {CONFIG['output_excel']}")

# ==============================
# MAIN ETL RUNNER
# ==============================

def main():
    print("ETL Job Started:", datetime.now())

    pg_df = extract_postgres()
    ora_df = extract_oracle()
    my_df = extract_mysql()
    xml_df = extract_xml()

    print("Extraction Complete.")

    pg_df = transform_postgres(pg_df)
    ora_df = transform_oracle(ora_df)
    my_df = transform_mysql(my_df)
    xml_df = transform_xml(xml_df)

    print("Transformation Complete.")

    combined, summary = combine_data(pg_df, ora_df, my_df, xml_df)

    load_to_excel(combined, summary)

    print("ETL Job Finished:", datetime.now())


if __name__ == "__main__":
    main()
