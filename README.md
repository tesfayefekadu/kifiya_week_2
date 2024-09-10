                                  Telecommunications Data Analysis

                                          Overview
This project aims to evaluate the growth potential of a telecommunications company by analyzing customer engagement and network experience. The goal is to identify areas for improving customer satisfaction based on their usage of services and the quality of network performance.

                            The analysis covers:

Customer engagement scores based on data usage across applications.
Network experience scores based on key performance indicators like TCP retransmission, RTT, and throughput.
Customer satisfaction, calculated as the average of engagement and experience scores.
Clustering of users based on their satisfaction scores to identify patterns.

                               Data Overview
The dataset includes several metrics related to user behavior, network performance, and satisfaction. Key columns include:

MSISDN/Number: Unique identifier for each customer.
Engagement Metrics: Data usage from various apps (YouTube, Netflix, Social Media, etc.).
Experience Metrics: Network performance metrics like RTT, TCP retransmission, throughput.
Satisfaction Score: Average of engagement and experience scores for each user
                                Requirements
To run this project, you need Python 3.1+ and the following Python packages. Install them using requirements.txt

                                             Limitations
Data Scope: The dataset only includes application usage and network performance. Other factors like pricing or customer service interactions are not considered.
Overfitting Risk: The R-squared score for the regression model may suggest overfitting, which could limit its generalization to unseen data.
Missing Data: Some rows with missing values were handled by either dropping or filling with mean/mode, which may not fully capture the complexities of customer behavior.