import pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt


# referenced https://www.geeksforgeeks.org/google-search-analysis-with-python/

trending_topics = TrendReq(hl='en-US', tz = 480) # language & timezone settings

keywords = ["Natural Language Processing", "Machine Learning"]
keywords = ["TXT","Red Velvet", "Namtanfilm"]

try:
    trending_topics.build_payload(keywords, cat=0, timeframe='today 6-m')
except Exception as e:
    print(f"An error occurred: {e}")

trending_topics.build_payload(keywords, cat = 0, timeframe='today 6-m')

data = trending_topics.interest_over_time()
print(data)
