import matplotlib.pyplot as plt
import seaborn as sns

def aggregate_engagement_metrics(df):
    # Aggregate the engagement metrics per user (MSISDN)
    engagement_data = df.groupby('MSISDN/Number').agg({
        'Bearer Id': 'count',                    # Total sessions frequency
        'Dur. (ms)': 'sum',                      # Total session duration
        'Total DL (Bytes)': 'sum',               # Total download bytes
        'Total UL (Bytes)': 'sum'                # Total upload bytes
    }).reset_index()

    # Total traffic (download + upload)
    engagement_data['Total Traffic (Bytes)'] = engagement_data['Total DL (Bytes)'] + engagement_data['Total UL (Bytes)']

    # Rename columns for clarity
    engagement_data.columns = [
        'User MSISDN', 'Total Sessions', 'Total Duration (ms)', 'Total Download (Bytes)', 
        'Total Upload (Bytes)', 'Total Traffic (Bytes)'
    ]
    
    return engagement_data

from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

def normalize_and_cluster(df, n_clusters=3):
    # Select relevant engagement metrics
    engagement_metrics = df[['Total Sessions', 'Total Duration (ms)', 'Total Traffic (Bytes)']]

    # Normalize the data
    scaler = MinMaxScaler()
    engagement_metrics_scaled = scaler.fit_transform(engagement_metrics)

    # Apply k-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42)
    df['Engagement Cluster'] = kmeans.fit_predict(engagement_metrics_scaled)

    return df, kmeans

def compute_cluster_statistics(df):
    # Group by cluster and compute min, max, average, and total metrics
    cluster_stats = df.groupby('Engagement Cluster').agg({
        'Total Sessions': ['min', 'max', 'mean', 'sum'],
        'Total Duration (ms)': ['min', 'max', 'mean', 'sum'],
        'Total Traffic (Bytes)': ['min', 'max', 'mean', 'sum']
    }).reset_index()

    return cluster_stats
def top_engaged_users_per_app(df, app_column):
    # Aggregate total traffic per user for the given app
    app_traffic = df.groupby('MSISDN/Number').agg({app_column: 'sum'}).reset_index()
    
    # Sort and get top 10 most engaged users for this app
    top_users = app_traffic.sort_values(by=app_column, ascending=False).head(10)
    return top_users



def plot_top_app_usage(df, top_apps):
    for app in top_apps:
        app_data = df.groupby('MSISDN/Number')[app].sum().nlargest(10)
        plt.figure(figsize=(10,6))
        sns.barplot(x=app_data.index, y=app_data.values)
        plt.title(f'Top Usage for {app}')
        plt.xlabel('User MSISDN')
        plt.ylabel('Total Download (Bytes)')
        plt.show()
def elbow_method(df):
    # Normalize engagement metrics
    engagement_metrics = df[['Total Sessions', 'Total Duration (ms)', 'Total Traffic (Bytes)']]
    scaler = MinMaxScaler()
    engagement_metrics_scaled = scaler.fit_transform(engagement_metrics)

    # Apply k-means clustering with different values of k and calculate inertia
    inertia = []
    k_values = range(1, 11)
    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42)
        kmeans.fit(engagement_metrics_scaled)
        inertia.append(kmeans.inertia_)

    # Plot inertia vs. k
    plt.figure(figsize=(10,6))
    plt.plot(k_values, inertia, 'bo-', markersize=8)
    plt.xlabel('Number of clusters (k)')
    plt.ylabel('Inertia')
    plt.title('Elbow Method to Determine Optimal k')
    plt.show()


