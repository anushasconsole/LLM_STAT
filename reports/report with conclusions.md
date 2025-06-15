# Statistical Analysis Report

**Generated at**: 2025-06-13 12:49:59

**Dataset Structure**: Univariate, Bivariate

**Columns Analyzed**: ['height', 'weight']


---

## Univariate Analysis

### Column: height

**Method:** descriptive_stats

- mean: 173.25

- median: 172.5

- std: 4.0625

- q1: 170

- q3: 181

- min: 168

- max: 181

- conclusions: {'interpretation': 'The mean score is approximately 173.25, with a standard deviation of 4.06. The median score is around 172.5. The data range is from 168 to 181. This suggests that the scores are centered around 173 with some variability, and a majority lies between 168 and 181.', 'significance': 'Significant', 'confidence': '95% confidence interval for the mean is approximately (165.23, 181.27)'}


---

### Column: weight

**Method:** descriptive_stats

- mean: 34.5

- median: 34

- std: 17.692051833761816

- q1: 18

- q3: 43.5

- min: 18

- max: 60

- conclusions: {'interpretation': "The data set has a mean (average) score of 34.5 with quite a bit of variation as indicated by a standard deviation of approximately 17.7. The middle or 'typical' score is 34, and the scores range from 18 to 60. Approximately half of the data falls below 34.5 and above 18.", 'significance': 'Practically significant', 'confidence': '95% confidence interval not applicable in this context'}


---

## Bivariate Analysis

### Pair: height_vs_weight

**Method:** t_test

- t_statistic: 1.4753869265095374

- p_value: 0.15900302865453222

- df: 5

- conclusions: {'interpretation': 'The t-test shows that there is no significant difference (p > 0.05) in weight between two groups at a 95% confidence level, when comparing the mean weight of individuals with an average height of 172cm and 168cm. However, this does not rule out the possibility of practical differences.', 'significance': 'Not significant', 'confidence': '95% confidence interval'}

**Method:** pearson_correlation

- correlation: 0.9284716357328276

- p_value: 0.01559832639982778

- conclusions: {'interpretation': 'The correlation between height and weight is strong (0.9285). This suggests that as height increases, weight tends to increase significantly (p-value = 0.016), with a confidence level of 95%. This relationship could indicate that taller individuals tend to weigh more than shorter ones in this dataset.', 'significance': 'Significant', 'confidence': 'Confidence level: 95%, Interval not applicable for correlation'}

**Method:** spearman_correlation

- correlation: 0.653497188234224

- p_value: 0.0596422414059851

- conclusions: {'interpretation': "There is a moderate positive correlation (0.65) between height and weight in the provided data. This suggests that as height increases, weight tends to increase as well. However, it's important to note that this relationship is not perfect. The p-value of 0.0596 indicates that the observed correlation may have occurred by chance alone about 6% of the time if there was truly no relationship between height and weight.", 'significance': 'Significant', 'confidence': '95% confidence level'}

**Method:** linear_regression

- slope: 0.8392857142857143

- intercept: -16.125

- r_squared: 0.9408265380843244

- std_error: 3.232371737877713

- p_value: 0.010476191489336647

- conclusions: {'interpretation': 'There is a strong positive linear relationship between height and weight (slope = 0.839). For every one unit increase in height, there is an average increase of approximately 0.84 units in weight. The model accounts for 94.08% of the variability in weight. The average intercept (-16.125) represents the predicted weight when height is zero, which is not practically meaningful since human height cannot be zero.', 'significance': 'Significant', 'confidence': '95% confidence level'}


---
