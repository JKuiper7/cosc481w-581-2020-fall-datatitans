from pathlib import Path
import matplotlib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from django.http import HttpResponse

SMALL_SIZE = 8
MEDIUM_SIZE = 15
BIGGER_SIZE = 20

plt.rc("font", size=SMALL_SIZE)  # default text sizes
plt.rc("axes", titlesize=SMALL_SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=SMALL_SIZE)  # legend fontsize
plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title

DataDir = Path(__file__).parent.parent / "data/input"
ImageDir = Path(__file__).parent.parent / "images"
print("Data directory:", DataDir)
# df = pd.read_csv('owid-covid-data.csv') # import csv file to dataframe
df = pd.read_csv(DataDir / "owid-covid-data.csv")  # import csv file to dataframe
df.head()

# In[87]:
# df.describe()                          # list out data frame
plt.figure(figsize=(50, 20))  # set size of the graph
sns.set(font_scale=3)  # set scale of graph fonts
sns.lineplot(data=df["total_deaths"])  # set line plot from data
# plt.ylim(0,250)                        # function to adjust the y limit
# plt.xlim(0,250)                        # function to adjust the x limit
plt.xticks(rotation=-45)  # add an angle to x labels
# In[4]: Total deaths from full data
dims = (100, 25)  # dimension variable for plot area
fig, ax = plt.subplots(figsize=dims)  # set plot area size

g = sns.lineplot(x=df["date"], y=df["total_deaths"])  # line plot for full data
for ind, label in enumerate(g.get_xticklabels()):  # loop so not every xtick is show,
    if ind % 10 == 0:  # making chart more readable
        label.set_visible(True)
    else:
        label.set_visible(False)

plt.autoscale()  # adjust frame for labels
plt.xticks(rotation=-45)  # add an angle to x labels
# plt.savefig('pltTransparent1.png', transparent=True)
plt.savefig(ImageDir / "plot1.jpeg")
# response = HttpResponse(content_type="image/jpeg")
# plt.savefig(response, format="jpeg")
# return response
plt.show()