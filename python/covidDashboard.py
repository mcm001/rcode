from io import StringIO
import matplotlib.pyplot as plt
import numpy as np
import requests
import pandas as pd

url = "http://news.northeastern.edu/interactive/2021/08/updated-covid-dashboard/datasets/covidupdate_testData.csv"

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

r = requests.get(url, allow_redirects=True, headers=headers)
# print(r.content)
# print(r.text)

csv = pd.read_csv(StringIO(r.text), sep=",")
print(csv)

date = csv['Date']
positive = csv['Positive Tests']
date = np.array(date)
positive = np.array(positive)

def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

windowSize = 3

plt.figure()

plt.subplot(221)
plt.scatter(date, positive, label="Positive tests per-day")
plt.ylim(0, max(positive))
plt.plot(date[windowSize - 1:], moving_average(positive, windowSize), 'y', label=f"{windowSize}-day average")
plt.legend()
plt.title("Cases over time")

plt.subplot(222)
per100k = positive / np.array(csv['Tests Completed']) * 100000
plt.scatter(date, per100k, label='Positive per 100k')
plt.ylim(0, max(per100k))
plt.plot(date[windowSize - 1:], moving_average(per100k, windowSize), 'y', label=f"{windowSize}-day average")
plt.legend()
plt.title("Cases per 100k")

plt.subplot(224)
plt.plot(date[1:], csv['Beds In Use'][1:], label='Beds In Use')
plt.plot(date[1:], csv['Beds Not In Use'][1:], label='Beds Not In Use')
plt.legend()
plt.title("Bed Usage")

plt.show()