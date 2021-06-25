##############################################################################
"""
Import libs
"""
##############################################################################

import pandas as pd
from statistics import mode
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from datetime import datetime as dt

##############################################################################
"""
Import dataset from http://insideairbnb.com/get-the-data.html
"""
##############################################################################
# create a list of available city and states
city = ['tx/austin','nc/asheville', 'ma/boston', 'fl/boward-county', \
        'ma/cambridge','il/chicago','nv/clark-county-nv', 'oh/columbus',\
        'co/denver','hi/hawaii','nj/jersey-city','ca/los-angeles',\
        'tn/nashville','la/new-orleans','ny/new-york-city',\
        'ca/oakland','ca/pacific-grove','or/portland','ri/rhode-island',\
        'or/salem-or','ca/san-diego','ca/san-francisco',\
        'ca/san-mateo-county','ca/santa-clara-county',\
        'ca/santa-cruz-county','wa/seattle','mn/twin-cities-msa',\
        'dc/washington-dc']

# grab all possible days within July for compile date from url
day = list(range(32))

# iterate through each state and day to get all possible July entries
appended_data = []
for c in city:
    try:
        for d in day:
            try:
                url = 'http://data.insideairbnb.com/united-states/{}/2019-07-{}/data/listings.csv.gz'.format(c, d)
                print(url)
                df = pd.read_csv(url)
                appended_data.append(df)
            except:
                continue
    except:
        continue
    

# concatenate the dataframes together
appended_data = pd.concat(appended_data)
# save locally
appended_data.to_excel('C:\\Users\\adamp\\OneDrive\\Desktop\\a_EDA\\FinalProject\\appended.xlsx')

#extract only the columns needed
dfmain = appended_data[['city','state','id','host_id','host_since',\
  'host_response_time','host_response_rate','host_listings_count',\
  'host_total_listings_count','host_identity_verified','market',\
  'property_type','room_type','accommodates','bathrooms','bedrooms','beds',\
  'bed_type','amenities','price','cleaning_fee','minimum_nights',\
  'maximum_nights','availability_365','number_of_reviews',\
  'number_of_reviews_ltm','review_scores_rating','review_scores_accuracy',\
  'review_scores_cleanliness','review_scores_checkin',\
  'review_scores_communication','review_scores_location','review_scores_value'\
  ,'instant_bookable','reviews_per_month']]

 # save locally
dfmain.to_excel('C:\\Users\\adamp\\OneDrive\\Desktop\\a_EDA\\FinalProject\\dfmain.xlsx')

dfmain = pd.read_excel('C:\\Users\\adamp\\OneDrive\\Desktop\\a_EDA\\FinalProject\\dfmain.xlsx')
dfbackup = dfmain
dfmain = dfbackup


##############################################################################
"""
Clean dataset
"""
##############################################################################
# convert $ object columns to floats
dfmain['price'] = dfmain['price'].replace('[\$,]', '', regex=True).astype(float)
dfmain['cleaning_fee'] = dfmain['cleaning_fee'].replace('[\$,]', '', regex=True).astype(float)

# remove unnecessary characters and states and make the state uppercase
dfmain['state'] = dfmain['state'].astype(str).str.upper()
dfmain['state'] = dfmain['state'].str.replace('BAJA CALIFORNIA', 'CA')
dfmain['state'] = dfmain['state'].str.replace('CALIFORNIA', 'CA')

dfmain = dfmain.drop(dfmain[(dfmain.state == 'DEPARTAMENTO DE MALDONADO')].index)  # URAGUAY? 
dfmain = dfmain.drop(dfmain[(dfmain.state == ' ')].index) 
dfmain = dfmain.drop(dfmain[ (dfmain.state == 'B.C.')].index)
dfmain = dfmain.drop(dfmain[ (dfmain.state == 'NAN')].index)

# convert the host date to a true date
dfmain['host_sinceConvert'] = pd.to_datetime(dfmain['host_since'])
dfmain['today'] = dt.today()

# convert the difference to days
dfmain['trueHostSince'] = abs((dfmain['today']  - dfmain['host_sinceConvert'])).dt.days

# for some reason Excel imports floats as objects... updated to float
dfmain['host_response_rate'] = pd.to_numeric(dfmain['host_response_rate'].str.replace('%', ''))

##############################################################################
"""
BEGIN ANALYSIS OF VARIABLES - HISTOGRAMS
"""
##############################################################################

def histFunc (var, name, b):
    Hist = var.dropna()
    plt.hist(Hist, bins=b, alpha=.9, label=name)
    plt.legend()
    print(Hist.mode())
    print(Hist.kurtosis())
    print(Hist.skew())
    print(Hist.describe())

histHostLength = histFunc(dfmain['trueHostSince'],'Host Since in days',30)
histComm = histFunc(dfmain['review_scores_communication'],'Communication Scores (1-10 scale)',10)
histResp = histFunc(dfmain['host_response_rate'],'Host response rate',40)
histReview = histFunc(dfmain['number_of_reviews'],'Number of reviews rcvd',30)
histCleanFee = histFunc(dfmain['cleaning_fee'],'Cleaning Fees',30)
histCReview = histFunc(dfmain['review_scores_cleanliness'],'Number of cleaning reviews',10)
hist365 = histFunc(dfmain['availability_365'],'Number of days open in a year',50)
histRatings = histFunc(dfmain['review_scores_rating'],'Overall average review ratings',30)
histPrice = histFunc(dfmain['price'],'Price Per Night',50)

# remove high prices and 0 prices
dfmain.price[dfmain.price >= 2000] = np.nan
# dfmain.price[dfmain.price < 10] = 0
dfmain = dfmain.drop(dfmain[(dfmain.price == np.nan)].index)

##############################################################################
"""
PMF's
"""
##############################################################################
# utilize PMF functions from the text 
import thinkstats2
import thinkplot

def myPMF (var1, lab1, var2, lab2, xlab, ylab, ax1, ax2, ax3, ax4):
    thinkplot.PrePlot(2)
    pmf1 = thinkstats2.Pmf(var1, label=lab1)
    pmf2 = thinkstats2.Pmf(var2, label=lab2)
    thinkplot.Pmfs([pmf1, pmf2])
    thinkplot.Show(xlabel=xlab,
                 ylabel=ylab,
                 axis=[ax1,ax2,ax3,ax4])\
    # Calculate the true effect size (Cohen's D) for both variables
    diff = var1.mean() - var2.mean()
    var_1 = var1.var()
    var_2 = var2.var()
    n1, n2 = len(var1), len(var2)
    
    pooled_var = (n1 * var_1 + n2 * var_2) / (n1 + n2)
    d = diff/sqrt(pooled_var)   
    
    print('median',str(lab1),str(np.median(pmf1)))
    print('mean',str(lab1),str(np.mean(pmf1)))
    print('median',str(lab2),str(np.median(pmf2)))
    print('mean',str(lab2),str(np.mean(pmf2)))
    print("Cohen's D", str(d))


#view the frequency of the data
dfmain['bed_type'].value_counts(sort=False)
"""
Pull-out Sofa       283
Futon               422
Real Bed         100138
Couch                90
Airbed              235
"""
   
# comparison is between real beds and non real beds
realBed = dfmain[dfmain.bed_type == 'Real Bed']
otherBeds = dfmain[dfmain.bed_type != 'Real Bed']

# first scenario PMF comparison
myPMF(var1=realBed['review_scores_rating'], lab1='real bed',
      var2=otherBeds['review_scores_rating'], lab2='other beds',
      xlab='overall reviews', ylab='probability',
      ax1=20,ax2=101,ax3=0,ax4=.3)

# first scenario PMF comparison
myPMF(var1=realBed['price'], lab1='real bed',
      var2=otherBeds['price'], lab2='other beds',
      xlab='price', ylab='probability',
      ax1=0,ax2=2000,ax3=0,ax4=.05)

# comparing price is very granular. 
# create a bin price to visualize different price ranges since prices may be too granular
# bins 1-25 = $1 - $505
# bins 26-50 = $525 - $1010
# bins >51 = $1030 - $1999
bins = np.linspace(1, max(dfmain['price']), 100)
dfmain['binPrice'] = np.digitize(dfmain['price'], bins)

# Do Real Beds cost more than non-real beds?
myPMF(var1=realBed['binPrice'], lab1='real bed',
      var2=otherBeds['binPrice'], lab2='other beds',
      xlab='bin price', ylab='probability',
      ax1=0,ax2=100,ax3=0,ax4=.22)

# retrieve a list of all the states
#dfmain.state.unique()

# Do locations with higher cleaning fees have better cleaning reviews? 
clean_under_10 = dfmain[dfmain.review_scores_cleanliness <10]
clean_at_10 = dfmain[dfmain.review_scores_cleanliness == 10]

myPMF(var1=clean_under_10['cleaning_fee'], lab1='Cleaning Rating < 10',
      var2=clean_at_10['cleaning_fee'], lab2='Cleaning Rating at 10',
      xlab='Cleaning Fees', ylab='probability',
      ax1=0,ax2=400,ax3=0,ax4=.09)

# Do lower priced rooms come with a higher cleaning cost? 
low_priced = dfmain[dfmain.price <100]
high_priced = dfmain[dfmain.price >500]

myPMF(var1=low_priced['cleaning_fee'], lab1='Low Overall Price',
      var2=high_priced['cleaning_fee'], lab2='High Overall Price',
      xlab='Cleaning Fees', ylab='probability',
      ax1=0,ax2=400,ax3=0,ax4=.15)


# Do long time hosts tend to get better reviews?
youngHost = dfmain[dfmain.trueHostSince <150]
oldHost = dfmain[dfmain.trueHostSince >730]

myPMF(var1=youngHost['review_scores_rating'], lab1='Young Host',
      var2=oldHost['review_scores_rating'], lab2='Old Host',
      xlab='Overall Scores/Ratings', ylab='probability',
      ax1=19,ax2=101,ax3=0,ax4=.80)

# Does the number of days the venue is open impact the price points?
open_small = dfmain[dfmain.availability_365 < 61]
open_long = dfmain[dfmain.availability_365 == 365]

myPMF(var1=open_small['binPrice'], lab1='Open a short time',
      var2=open_long['binPrice'], lab2='Open a long time',
      xlab='Binned Price', ylab='probability',
      ax1=0,ax2=101,ax3=0,ax4=.16)

##############################################################################
"""
CDF
"""
##############################################################################

def myCDF (var1, var2, lab1, lab2, title, x):
    sorted_data = np.sort(var1)
    sorted_data2 = np.sort(var2)
    yvals=np.arange(len(sorted_data))/float(len(sorted_data)-1)
    yvals2=np.arange(len(sorted_data2))/float(len(sorted_data2)-1)
    plt.plot(sorted_data,yvals, label = lab1)
    plt.plot(sorted_data2,yvals2,label = lab2)
    plt.title(label=title)
    plt.xlabel(x)
    plt.ylabel('CDF')
    plt.legend()
    plt.show()

myCDF(var1=youngHost['review_scores_rating'], lab1='Young Host',
      var2=oldHost['review_scores_rating'], lab2='Old Host'
      ,title = 'Young Host vs New Host Reviews', x='review rating')
myCDF(var1=open_small['price'], lab1='Open a short time',
      var2=open_long['price'], lab2='Open a long time'
      ,title = 'Airbnb Experience price comparison', x='price')

myCDF(var1=low_priced['cleaning_fee'], lab1='Low Overall Price',
      var2=high_priced['cleaning_fee'], lab2='High Overall Price'
      ,title = 'Low Price vs High Price', x='cleaning fee')
myCDF(var1=clean_under_10['cleaning_fee'], lab1='Cleaning Rating < 10',
      var2=clean_at_10['cleaning_fee'], lab2='Cleaning Rating at 10'
      ,title = 'Cleaning Ratings', x='cleaning fee')

myCDF(var1=realBed['price'], lab1='real bed',
      var2=otherBeds['price'], lab2='other beds'
      ,title = 'Real Bed vs. Other Bed', x='price')
myCDF(var1=realBed['review_scores_rating'], lab1='real bed',
      var2=otherBeds['review_scores_rating'], lab2='other beds'
      ,title = 'Real Bed vs. Other Bed', x='Review Rating')

##############################################################################
"""
Modeling
"""
##############################################################################

# I tried several different models with this dataset.
# Variables from the young host and old host dataframes were the most effective
# when modeling the data. 
mean, var = thinkstats2.TrimmedMeanVar(youngHost['availability_365'].dropna(), p=0.02)
std = np.sqrt(var)

xs = [-4, 4]
fxs, fys = thinkstats2.FitLine(xs, mean, std)
thinkplot.Plot(fxs, fys, linewidth=4, color='0.8')

thinkplot.PrePlot(2) 
xs, ys = thinkstats2.NormalProbability(youngHost['availability_365'].dropna())
thinkplot.Plot(xs, ys, label='Young Hosts')

xs, ys = thinkstats2.NormalProbability(oldHost['availability_365'].dropna())
thinkplot.Plot(xs, ys, label='Old Hosts')
thinkplot.Config(title='Normal probability plot availability',
                 xlabel='Standard deviations from mean',
                 ylim= (0,366),
                 ylabel='Days')

mean, var = thinkstats2.TrimmedMeanVar(youngHost['availability_365'].dropna(), p=0.02)
std = np.sqrt(var)

xs = [-4, 4]
fxs, fys = thinkstats2.FitLine(xs, mean, std)
thinkplot.Plot(fxs, fys, linewidth=4, color='0.8')

thinkplot.PrePlot(2) 
xs, ys = thinkstats2.NormalProbability(youngHost['cleaning_fee'].dropna())
thinkplot.Plot(xs, ys, label='Young Hosts')

xs, ys = thinkstats2.NormalProbability(oldHost['cleaning_fee'].dropna())
thinkplot.Plot(xs, ys, label='Old Hosts')
thinkplot.Config(title='Normal probability plot cleaning fees',
                 xlabel='Standard deviations from mean',
                 ylim= (0,366),
                 ylabel='Days')


mean, var = thinkstats2.TrimmedMeanVar(youngHost['availability_365'].dropna(), p=0.02)
std = np.sqrt(var)

xs = [-4, 4]
fxs, fys = thinkstats2.FitLine(xs, mean, std)
thinkplot.Plot(fxs, fys, linewidth=4, color='0.8')

thinkplot.PrePlot(2) 
xs, ys = thinkstats2.NormalProbability(youngHost['availability_365'].dropna())
thinkplot.Plot(xs, ys, label='Young Hosts')

xs, ys = thinkstats2.NormalProbability(oldHost['availability_365'].dropna())
thinkplot.Plot(xs, ys, label='Old Hosts')
thinkplot.Config(title='Normal probability plot cleaning fees',
                 xlabel='Standard deviations from mean',
                 ylim= (0,366),
                 ylabel='Days')

##############################################################################
"""
Scatter Plots and Correlation
"""
##############################################################################

# delete unnecessary columns
import seaborn as sns
def deleteCols (df):
    del df['maximum_nights']
    del df['Unnamed: 0']
    del df['city']
    del df['state']
    #del df['id']
    del df['host_id']
    del df['host_total_listings_count']
    del df['number_of_reviews_ltm']
    del df['minimum_nights']
    del df['reviews_per_month']
    del df['instant_bookable'] # could be a conveniance feature, but no 100%
    del df['amenities'] # could be good data, but would require work to parse
    del df['host_identity_verified'] # I'm not sure what this column means
    del df['market'] # these are not consistent 
    del df['host_response_time'] # have host response rate
    del df['property_type'] # too many categories to analyze
deleteCols(dfmain)

# add indicators for the scatter plot
dfmain['RealBed'] = dfmain.bed_type == 'Real Bed'
dfmain['clean_at_10'] = dfmain.review_scores_cleanliness == 10
dfmain['youngHost'] = dfmain.trueHostSince <150
dfmain['open_small'] = dfmain.availability_365 < 61
dfmain['open_long'] = dfmain.availability_365 == 365

# encode the categorical variables to rows represented by 0's and 1's

# this step finds all categorical variables 
obj_df = dfmain.select_dtypes(include=['object']).copy()
# see if there are any null fields
obj_df[obj_df.isnull().any(axis=1)]
del obj_df['instant_bookable'] # could be a conveniance feature, but no 100%
del obj_df['amenities'] # could be good data, but would require work to parse
del obj_df['host_identity_verified'] # I'm not sure what this column means
del obj_df['market'] # these are not consistent 
del obj_df['host_response_time'] # have host response rate
del obj_df['property_type'] # too many categories to analyze

# obj_df[obj_df.isnull().any(axis=1)]

# converts the objects to boolean values and joins back to main df
obj_df2 = pd.get_dummies(obj_df, columns=["room_type","bed_type"], 
                        prefix=["room","bed"])

dfcorr = pd.DataFrame.join(dfmain, obj_df2, lsuffix='_ind')
   

# calculate column correlations and make a seaborn heatmap
    
def correlationFunc (df):
    corr = df.corr().round(2)
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)] = True
    f, ax = plt.subplots(figsize=(14, 11))
    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(220, 10, as_cmap=True)
    
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1,vmin=-1, center=0,
            square=True, linewidths=.5, cbar_kws={"shrink": .5}, annot=True)

correlationFunc(dfcorr)
list(dfcorr)
dfcleaningfees = dfcorr[['accommodates','bathrooms', 'room_Entire home/apt',
                         'bedrooms','beds','price',
                         'availability_365','cleaning_fee']]

correlationFunc (dfcleaningfees)


sns.set(style="ticks")
sns.pairplot(dfcleaningfees)


ax = sns.scatterplot(x="bedrooms", y="cleaning_fee",hue="clean_at_10",
                     style="clean_at_10", data=dfcorr, x_jitter =.5)
list(dfcorr)
dfhosts = dfcorr[['host_listings_count','number_of_reviews','review_scores_rating',
                            'review_scores_accuracy','review_scores_cleanliness',
                            'review_scores_checkin','review_scores_communication',
                            'review_scores_location','review_scores_value',
                            'trueHostSince']]

correlationFunc (dfhosts)
sns.set(style="ticks")
sns.pairplot(dfhosts)


dfprice = dfcorr[['cleaning_fee','accommodates','bathrooms',
                  'bedrooms','beds','availability_365','room_Entire home/apt',
                  'room_Private room','room_Shared room','bed_Real Bed','price']]

correlationFunc (dfprice)
sns.set(style="ticks")
sns.pairplot(dfprice)


dfresponse = dfcorr[['number_of_reviews','review_scores_rating',
                            'review_scores_accuracy','review_scores_cleanliness',
                            'review_scores_checkin','review_scores_communication',
                            'review_scores_location','review_scores_value',
                            'host_response_rate']]

correlationFunc (dfresponse)
sns.set(style="ticks")
sns.pairplot(dfresponse)



##############################################################################
"""
Hypothesis Testing
"""
##############################################################################

from thinkstats2 import HypothesisTest as ht
import hypothesis as hp

# Difference in means
data = clean_at_10.cleaning_fee.values, clean_under_10.cleaning_fee.values
hyp = hp.DiffMeansPermute(data)
pvalue = hyp.PValue()
pvalue


# I tried several scenarios and the p-value always came back 0.0

# Corr Testing
cleaned = dfmain.dropna(subset=['cleaning_fee', 'price'])
data = cleaned.cleaning_fee.values, cleaned.price.values
ht = hp.CorrelationPermute(data)
pvalue = ht.PValue()
pvalue

# I tried several scenarios and the p-value always came back 0.0

##############################################################################
"""
Linear Model
"""
##############################################################################

import seaborn as sns
import numpy as np
from scipy import stats

x, y = dfmain['host_response_rate'],dfmain['review_scores_rating']
sns.jointplot(x, y, kind="reg")
def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2
sns.jointplot(x, y, kind="reg", stat_func=r2)



x, y = dfmain['accommodates'],dfmain['cleaning_fee']
x, y = dfmain['beds'],dfmain['cleaning_fee']
sns.jointplot(x, y, kind="reg")
def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2
sns.jointplot(x, y, kind="reg", stat_func=r2)


x, y = clean_under_10['cleaning_fee'],clean_under_10['review_scores_cleanliness']
sns.jointplot(x, y, kind="reg")
def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2
sns.jointplot(x, y, kind="reg", stat_func=r2)


# Samples
dfyoung= youngHost.sample(500)
dfold= oldHost.sample(500)

# Regression plot using seaborn.
fig = plt.figure(figsize=(10,7))
sns.regplot(x=dfyoung.trueHostSince,y=dfyoung.review_scores_rating,color='blue', marker='+')
sns.regplot(x=dfold.trueHostSince,y=dfold.review_scores_rating,color='black', marker='+')

# Legend, title and labels.
plt.legend(labels=['dfyoung','dfold'])
plt.title('Relationship between Host Days and Ratings', size=24)
plt.xlabel('Host Days', size=18)
plt.ylabel('Ratings', size=18);


x, y = dfmain['availability_365'],dfmain['price']
sns.jointplot(x, y, kind="reg")
def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2
sns.jointplot(x, y, kind="reg", stat_func=r2)

x, y = dfmain['availability_365'],dfmain['cleaning_fee']
sns.jointplot(x, y, kind="reg")
def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2
sns.jointplot(x, y, kind="reg", stat_func=r2)

