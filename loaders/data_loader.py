import streamlit as st
import snowflake.connector
import pandas as pd
import json
import os
from dotenv import load_dotenv
from config.settings import INITIAL_CATEGORIES

# Load environment variables
load_dotenv()


def get_snowflake_config():
    """Get Snowflake configuration with validation"""
    config = {
        "user": os.getenv("SNOWFLAKE_USER"),
        "password": os.getenv("SNOWFLAKE_PASSWORD"),
        "account": os.getenv("SNOWFLAKE_ACCOUNT"),
        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE"),
        "database": os.getenv("SNOWFLAKE_DATABASE"),
        "schema": os.getenv("SNOWFLAKE_SCHEMA"),
    }

    # Validate required fields
    missing_fields = [key for key, value in config.items() if not value]
    if missing_fields:
        st.error(f"Missing environment variables: {', '.join(missing_fields)}")
        return None

    return config


def create_snowflake_connection():
    """Create a new Snowflake connection"""
    config = get_snowflake_config()
    if not config:
        return None

    try:
        conn = snowflake.connector.connect(
            user=config["user"],
            password=config["password"],
            account=config["account"],
            warehouse=config["warehouse"],
            database=config["database"],
            schema=config["schema"],
            login_timeout=60,
            network_timeout=60,
        )
        return conn
    except Exception as e:
        st.error(f"Failed to connect to Snowflake: {e}")
        return None


def safe_json_parse(value):
    """Safely parse JSON string, return original value if parsing fails"""
    if not isinstance(value, str):
        return value

    if not value or value.strip() == "":
        return None

    # Try to parse as JSON
    try:
        # Handle common JSON formats
        value = value.strip()
        if value.startswith("{") and value.endswith("}"):
            return json.loads(value)
        elif value.startswith("[") and value.endswith("]"):
            return json.loads(value)
        else:
            # Try to parse anyway in case it's a JSON string without obvious delimiters
            return json.loads(value)
    except (json.JSONDecodeError, ValueError):
        # If JSON parsing fails, return the original string
        return value


def process_item_data(raw_item):
    """Process raw item data from Snowflake, handling JSON parsing"""
    processed_item = {}

    for key, value in raw_item.items():
        key_lower = key.lower()

        # Handle special fields that should be parsed as JSON
        if key_lower in [
            "applications",
            "categories",
            "images",
            "important_figures",
            "key_points",
            "references",
            "related_topics",
            "timeline",
        ]:
            processed_item[key_lower] = safe_json_parse(value) or []

        # Handle other fields
        elif key_lower == "title":
            processed_item["title"] = value or "Untitled Item"
        elif key_lower == "summary":
            processed_item["summary"] = value or ""
        elif key_lower == "current_status":
            processed_item["current_status"] = value or ""
        elif key_lower == "future_prospects":
            processed_item["future_prospects"] = value or ""
        elif key_lower == "source_url":
            processed_item["source_url"] = value or ""
        elif key_lower in ["generated_at", "last_modified"]:
            processed_item[key_lower] = value
        else:
            # For any other fields, try to parse as JSON, otherwise keep as is
            processed_item[key_lower] = safe_json_parse(value)

    return processed_item


@st.cache_data
def load_all_data_streamlit():
    """
    Loads data from Snowflake tables and organizes them
    into a dictionary structure for the Streamlit application.
    Returns the full item data (cached).
    """
    # Create fresh connection for this operation
    conn = create_snowflake_connection()
    if not conn:
        return None

    app_data = {}
    app_data.update(INITIAL_CATEGORIES)

    try:
        cursor = conn.cursor()

        # Get available tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        available_tables = [
            table[1] for table in tables
        ]  # Table name is usually in index 1

        # Iterate through each category
        for category_id in INITIAL_CATEGORIES.keys():
            try:
                # Try different table naming conventions, including ARTISTS
                possible_table_names = [
                    f"{category_id}_items",
                    f"{category_id.upper()}_ITEMS",
                    f"items_{category_id}",
                    f"ITEMS_{category_id.upper()}",
                    category_id,
                    category_id.upper(),
                    "ARTISTS",  # Add ARTISTS table specifically
                ]

                table_found = False
                for table_name in possible_table_names:
                    if table_name in available_tables:
                        # Load data from the table
                        query = f"SELECT * FROM {table_name}"
                        cursor.execute(query)
                        results = cursor.fetchall()

                        # Get column names
                        column_names = [desc[0] for desc in cursor.description]

                        # Convert results to list of dictionaries with proper JSON parsing
                        for row in results:
                            raw_item = dict(zip(column_names, row))

                            # Process the item data with proper JSON parsing
                            processed_item = process_item_data(raw_item)

                            app_data[category_id]["items"].append(processed_item)

                        table_found = True
                        break

            except Exception as e:
                continue

    except Exception as e:
        st.error(f"Database query error: {e}")
        return None

    finally:
        # Always close the connection
        if conn:
            conn.close()

    return app_data


@st.cache_data
def load_category_data_streamlit(category_id):
    """
    Loads data for a specific category from Snowflake.
    Useful for loading data on-demand instead of all at once.
    """
    conn = create_snowflake_connection()
    if not conn:
        return []

    try:
        cursor = conn.cursor()

        # Try different table naming conventions, including ARTISTS
        possible_table_names = [
            f"{category_id}_items",
            f"{category_id.upper()}_ITEMS",
            f"items_{category_id}",
            f"ITEMS_{category_id.upper()}",
            category_id,
            category_id.upper(),
            "ARTISTS",  # Add ARTISTS table specifically
        ]

        # Get available tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        available_tables = [table[1] for table in tables]

        # Find the correct table
        table_name = None
        for possible_name in possible_table_names:
            if possible_name in available_tables:
                table_name = possible_name
                break

        if not table_name:
            return []

        # Load data from the table
        query = f"SELECT * FROM {table_name}"
        cursor.execute(query)
        results = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]

        items = []
        for row in results:
            raw_item = dict(zip(column_names, row))

            # Process the item data with proper JSON parsing
            processed_item = process_item_data(raw_item)
            items.append(processed_item)

        return items

    except Exception as e:
        return []

    finally:
        if conn:
            conn.close()


# Test function without caching
def test_connection():
    """Test connection without caching (for debugging)"""
    conn = create_snowflake_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT CURRENT_VERSION()")
            version = cursor.fetchone()[0]
            cursor.close()
            st.success(f"✅ Connection successful! Snowflake version: {version}")
            return True
        except Exception as e:
            st.error(f"Query test failed: {e}")
            return False
        finally:
            conn.close()
    return False


# Alternative: Using pandas for simpler data loading
@st.cache_data
def load_data_with_pandas(category_id):
    """
    Alternative approach using pandas for simpler data loading
    """
    config = get_snowflake_config()
    if not config:
        return pd.DataFrame()

    try:
        # Create connection string for pandas
        conn_string = f"snowflake://{config['user']}:{config['password']}@{config['account']}/{config['database']}/{config['schema']}?warehouse={config['warehouse']}"

        # Try different table names, including ARTISTS
        possible_table_names = [
            f"{category_id}_items",
            f"{category_id.upper()}_ITEMS",
            category_id,
            category_id.upper(),
            "ARTISTS",
        ]

        for table_name in possible_table_names:
            try:
                query = f"SELECT * FROM {table_name}"
                df = pd.read_sql(query, conn_string)

                # Process the dataframe to handle JSON columns
                json_columns = [
                    "applications",
                    "categories",
                    "images",
                    "important_figures",
                    "key_points",
                    "references",
                    "related_topics",
                    "timeline",
                ]

                for col in json_columns:
                    if col.upper() in df.columns:
                        df[col.upper()] = df[col.upper()].apply(safe_json_parse)
                    elif col in df.columns:
                        df[col] = df[col].apply(safe_json_parse)

                return df
            except Exception:
                continue

        return pd.DataFrame()

    except Exception as e:
        return pd.DataFrame()


# Debug helper
def show_debug_info():
    """Show connection debug information"""
    st.subheader("🔍 Snowflake Debug Information")

    # Show environment variables (without passwords)
    with st.expander("Environment Variables"):
        config = get_snowflake_config()
        if config:
            for key, value in config.items():
                if key == "password":
                    st.write(f"✅ {key}: {'*' * len(value)}")
                else:
                    st.write(f"✅ {key}: {value}")
        else:
            st.error("Configuration not loaded properly")

    # Test connection
    with st.expander("Connection Test"):
        if st.button("Test Connection"):
            test_connection()

    # Show available tables
    with st.expander("Available Tables"):
        if st.button("Show Tables"):
            conn = create_snowflake_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SHOW TABLES")
                    tables = cursor.fetchall()

                    if tables:
                        st.write("Available tables:")
                        for table in tables:
                            st.write(f"- {table[1]}")  # Table name
                    else:
                        st.warning("No tables found")

                except Exception as e:
                    st.error(f"Error showing tables: {e}")
                finally:
                    conn.close()

    # Show sample data from ARTISTS table
    with st.expander("Sample Data from ARTISTS Table"):
        if st.button("Show Sample Data"):
            conn = create_snowflake_connection()
            if conn:
                try:
                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM ARTISTS LIMIT 1")
                    result = cursor.fetchone()
                    column_names = [desc[0] for desc in cursor.description]

                    if result:
                        raw_item = dict(zip(column_names, result))
                        st.write("Raw data:")
                        st.json(raw_item)

                        st.write("Processed data:")
                        processed_item = process_item_data(raw_item)
                        st.json(processed_item)
                    else:
                        st.warning("No data found in ARTISTS table")

                except Exception as e:
                    st.error(f"Error showing sample data: {e}")
                finally:
                    conn.close()
