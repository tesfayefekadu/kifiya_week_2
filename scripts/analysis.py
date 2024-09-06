import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler



def top_n_handsets(df):
    h_count=df['Handset Type'].value_counts().head(10)
    return h_count

def top_n_manufacturers(df):
    h_man = df['Handset Manufacturer'].value_counts().head(3)
    return h_man

def top_5_handsets_per_manufacturer(df, top_manufacturers):
     return  df[df['Handset Manufacturer'].isin(top_manufacturers)].groupby('Handset Manufacturer')['Handset Type'].value_counts().groupby(level=0).head(5)

def aggregate_user_data(df): 
    """ 
    Aggregate user data to compute total number of sessions, session duration, 
    total download/upload data, and data volume per application. 
    """ 
    user_aggregation = df.groupby('MSISDN/Number').agg( 
        total_sessions=('Bearer Id', 'count'), 
        total_duration_ms=('Dur. (ms)', 'sum'), 
        total_download_bytes=('Total DL (Bytes)', 'sum'), 
        total_upload_bytes=('Total UL (Bytes)', 'sum'), 
        social_media_dl_bytes=('Social Media DL (Bytes)', 'sum'), 
        google_dl_bytes=('Google DL (Bytes)', 'sum'), 
        email_dl_bytes=('Email DL (Bytes)', 'sum'), 
        youtube_dl_bytes=('Youtube DL (Bytes)', 'sum'), 
        netflix_dl_bytes=('Netflix DL (Bytes)', 'sum'), 
        gaming_dl_bytes=('Gaming DL (Bytes)', 'sum'), 
        other_dl_bytes=('Other DL (Bytes)', 'sum') 
    ).reset_index() 
 
    # Rename columns for clarity 
    user_aggregation.columns = [ 
        'User MSISDN', 
        'Total Sessions', 
        'Total Duration (ms)', 
        'Total Download (Bytes)', 
        'Total Upload (Bytes)', 
        'Social Media Download (Bytes)', 
        'Google Download (Bytes)', 
        'Email Download (Bytes)', 
        'YouTube Download (Bytes)', 
        'Netflix Download (Bytes)', 
        'Gaming Download (Bytes)', 
        'Other Download (Bytes)' 
    ] 
    return user_aggregation   

def handle_missing_values(df):
    # Drop rows with missing values
    df.dropna(inplace=True)
    return df


def basic_metrics(df):
    metrics = df.describe().loc[['mean', '50%', 'std']].transpose()
    metrics.columns = ['Mean', 'Median', 'Std Dev']
    return metrics

def segment_users_by_duration(df):
    df['Decile'] = pd.qcut(df['Total Duration (ms)'], 10, labels=False)
    decile_stats = df.groupby('Decile').agg({
        'Total Download (Bytes)': 'sum',
        'Total Upload (Bytes)': 'sum'
    }).reset_index()
    return decile_stats
def univariate_dispersion_analysis(df):
    dispersion_params = pd.DataFrame({
        'Variance': df.var(),
        'Range': df.max() - df.min()
    })
    return dispersion_params

def compute_dispersion_params(df):
    # Select only numeric columns for analysis
    numeric_cols = df.select_dtypes(include='number')
    
    # Compute the dispersion parameters: variance, standard deviation, range, and IQR
    dispersion_params = pd.DataFrame({
        'Variance': numeric_cols.var(),
        'Std Dev': numeric_cols.std(),
        'Range': numeric_cols.max() - numeric_cols.min(),
        'IQR': numeric_cols.quantile(0.75) - numeric_cols.quantile(0.25)
    })
    
    return dispersion_params



def plot_univariate_analysis(df, column):
    # Plot histogram
    plt.figure(figsize=(10,6))
    sns.histplot(df[column], bins=30, kde=True)
    plt.title(f'Distribution of {column}')
    plt.show()

    # Plot boxplot
    plt.figure(figsize=(10,6))
    sns.boxplot(x=df[column])
    plt.title(f'Boxplot of {column}')
    plt.show()

def bivariate_analysis(df, x_column, y_column):
    plt.figure(figsize=(10,6))
    sns.scatterplot(x=df[x_column], y=df[y_column])
    plt.title(f'Bivariate Analysis: {x_column} vs {y_column}')
    plt.show()

def correlation_analysis(df):
    correlation_matrix = df.corr()
    plt.figure(figsize=(10,8))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Matrix')
    plt.show()
    return correlation_matrix

def perform_pca(df, n_components=2):
    # Standardize the data before applying PCA
    scaler = StandardScaler()
    scaled_data = scaler.fit_transform(df)

    # Apply PCA
    pca = PCA(n_components=n_components)
    principal_components = pca.fit_transform(scaled_data)
    
    explained_variance = pca.explained_variance_ratio_
    
    print(f'Explained variance by components: {explained_variance}')
    
    return principal_components, explained_variance