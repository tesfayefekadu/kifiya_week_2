import numpy as np
import numpy as np

def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((point1 - point2) ** 2))

def assign_scores(df, engagement_centroid, experience_centroid, feature_columns):
    # Extracting the correct feature columns
    features = df[feature_columns]

    # Calculating engagement score
    df['Engagement Score'] = features.apply(lambda row: euclidean_distance(row, engagement_centroid), axis=1)

    # Calculating experience score
    df['Experience Score'] = features.apply(lambda row: euclidean_distance(row, experience_centroid), axis=1)
    
    return df
