import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

def aggregate_experience_metrics(df):
    # Separate numeric and non-numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    non_numeric_cols = df.select_dtypes(exclude=['number']).columns

    # Fill missing values in numeric columns with their mean
    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

    # Fill missing values in non-numeric columns (like 'Handset Type') with mode
    df[non_numeric_cols] = df[non_numeric_cols].fillna(df[non_numeric_cols].mode().iloc[0])

    # Aggregate network parameters per customer
    experience_data = df.groupby('MSISDN/Number').agg({
        'TCP DL Retrans. Vol (Bytes)': 'mean',    # Average TCP Downlink Retransmission Volume
        'TCP UL Retrans. Vol (Bytes)': 'mean',    # Average TCP Uplink Retransmission Volume
        'Avg RTT DL (ms)': 'mean',                # Average Downlink RTT
        'Avg RTT UL (ms)': 'mean',                # Average Uplink RTT
        'Avg Bearer TP DL (kbps)': 'mean',        # Average Downlink Throughput
        'Avg Bearer TP UL (kbps)': 'mean',        # Average Uplink Throughput
        'Handset Type': 'first'                   # Handset type (one per customer)
    }).reset_index()

    # Rename columns for clarity
    experience_data.columns = [
        'User MSISDN', 'Avg TCP DL Retrans. Vol', 'Avg TCP UL Retrans. Vol', 'Avg RTT DL', 'Avg RTT UL',
        'Avg Bearer TP DL', 'Avg Bearer TP UL', 'Handset Type'
    ]
    
    return experience_data

def top_bottom_frequent_values(df, column):
    top_values = df[column].nlargest(10)
    bottom_values = df[column].nsmallest(10)
    most_frequent = df[column].value_counts().head(10)

    return top_values, bottom_values, most_frequent

def plot_distribution_per_handset(df, column, ylabel):
    plt.figure(figsize=(12, 8))
    sns.boxplot(x='Handset Type', y=column, data=df)
    plt.xticks(rotation=45, ha='right')  # Rotate x labels for better readability
    plt.ylabel(ylabel)
    plt.title(f'Distribution of {ylabel} per Handset Type')
    plt.show()

def cluster_users_by_experience(df, n_clusters=3):
    # Select relevant columns for clustering
    features = df[['Avg TCP DL Retrans. Vol', 'Avg TCP UL Retrans. Vol', 'Avg RTT DL', 'Avg RTT UL', 'Avg Bearer TP DL', 'Avg Bearer TP UL']]

    # Standardize the features
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    # Apply k-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['Experience Cluster'] = kmeans.fit_predict(scaled_features)

    return df, kmeans