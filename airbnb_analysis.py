import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Loading data
def load_data(path):
    try:
        df = pd.read_csv(path)
        print("Data loaded successfully")
        return df
    except Exception as e:
        print("Error loading data")
        return None


# Cleaning Data
def clean_data(df):

    # Filling unknown categorical values
    unknown_cols = ["Name","house rules","host_identity_verified","host name","Construction year"]
    for col in unknown_cols:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")

    # Converting  numeric columns and fill with median
    numeric_cols = ["lat","long","minimum nights","number of reviews",
                    "calculated host listings count","reviews per month","review rate number"]
    
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
            df[col] = df[col].fillna(df[col].median())

    # Clean price columns("$",",")
    price_cols = ["price","service fee"]
    for col in price_cols:
        if col in df.columns:
            df[col] = df[col].astype(str)
            df[col] = df[col].str.replace("$","",regex=False)
            df[col] = df[col].str.replace(",","",regex=False)
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Fill categorical Data with mode Value
    mode_cols = ["neighbourhood","country","country code","instant_bookable","cancellation_policy"]
    for col in mode_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mode()[0])

    # Date handling
    if "last review" in df.columns:
        df["last review"] = pd.to_datetime(df["last review"], errors="coerce")
        df["last review"] = df["last review"].ffill()

    # Dropping columns
    df = df.drop(columns=["license","id"], errors="ignore")

    print("\n✅ Missing values after cleaning:\n", df.isnull().sum())
    return df


#   Analysis
def analyse_data(df):
    print("Dataset Shape:", df.shape)
    print("Summary Statistics:\n", df.describe(include="all"))
    df.info()


# Visualisation
def visualize_data(df):

    # 1. Price Distribution
    if "price" in df.columns:
        df["price"].dropna().hist(bins=50)
        plt.title("Price Distribution")
        plt.xlabel("Price")
        plt.ylabel("Frequency")
        plt.show()

    # 2. Top Neighbourhoods
    if "neighbourhood" in df.columns:
        df["neighbourhood"].value_counts().head(10).plot(kind="bar")
        plt.title("Top 10 Neighbourhoods")
        plt.xlabel("Neighbourhood")
        plt.ylabel("Count")
        plt.xticks(rotation=45)
        plt.show()

    # 3. Reviews vs Price
    if "number of reviews" in df.columns and "price" in df.columns:
        plt.scatter(df["number of reviews"], df["price"])
        plt.title("Reviews vs Price")
        plt.xlabel("Number of Reviews")
        plt.ylabel("Price")
        plt.show()


# Save Data
def save_data(df, output_path="cleaned_airbnb_data.csv"):
    df.to_csv(output_path, index=False,encoding = "utf-8-sig")
    print("Data saved")


# Main
def main():
    path = "airbnb_data.csv" 
    df = load_data(path)

    if df is not None:
        df = clean_data(df)
        analyse_data(df)
        visualize_data(df)
        save_data(df)


if __name__ == "__main__":
    main()
