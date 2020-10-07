---
title: "Geocoding"
mathjax: true
nav_order: 1
parent: Geo-Spatial
has_children: no
---

# Geocoding

**Geocoding** is taking an address (e.g. 1600 Pennsylvania Ave NW, Washington DC 20500) or a name of a place (e.g. The White House) and turning it into a geographic position on the earth's surface. Commonly, the cooridinate system is longitude and latitude but there are other [potential coordinate systems](https://pro.arcgis.com/en/pro-app/help/data/geocoding/introduction-to-finding-places-on-a-map.htm) that can be used.

There are many different types of locations one can geocode including:
  1. Cities
  2. Landmarks
  3. Geographic Locations
    * Mountains
    * Rivers
  3. Addresses
    * Street Intersections
    * House Numbers with street names
    * Postal Codes

There are multiple ways to geocode. For instance, you could find the corrdinates of the Empire State building by flying to New York, riding an elevator to the top of the building, and then using your GPS to get the latitiude and longitude of where you were standing. A much more efficient way of geocoding is through **interpolation**. Interpolation uses other known geocoded locations to estimate the coordinates of the data that you wish to geocode. A computer uses an algorithm and the closest known geocodes to conduct this interpolation. However, the farther the "closest" known geocodes are to the data you are trying to geocode the less *accurate* the geocoding process is. [smartystreets](https://smartystreets.com/articles/what-are-geocodes), a geocode platform, has a good explanation of this.

Additionally, **Reverse Geocoding**  takes a latitude-longitude pair (or other global coordinates) and converts it into an address or a place. Depending on the data that is available reverse geocoding can be very useful. Similar to regular geocoding, reverse geocoding uses other known reverse geocoded locations to estimate the address of the inputted coordinates. 

## The Geocoding Process 

Whenever you geocode data there is a 3 step process that is undergone: 

* **Step 1: Input Data**
      Descriptive or textual data is inputted to yield a desired corresponding spatial data 
* **Step 2: Classification of Input Data**
      Input data is sorted into two groups *relative input data* and *absolute data*
* **Step 3A: Relative Input Data**
      Relative input data is the non-preferred type of data (most geocoding reject relative input data). Relative data are textual descriptions of locations that cannot be converted into precise spatial data on their own. Instead they are dependent on a other reference locations. For example, "across the street from the White House" has to use "the White House" as a reference point and then deduce what "across the street" means.
* **Step 3B: Absolute Data**
      This is the sweet sweet data that geocoding platforms love. A spatial coordinate (lon, lat) can be defined for this data independently of other reference points. Examples:
      USPS ZIP codes; complete and partial postal addresses; PO boxes; cities; counties; intersections; and named places

## Why is geocoding helpful? 

Odds are if you are on this page then you already have a reason to use geocoding, but here is a brief motivation for how geocoding can help with a project. Geocoding is helpful when you want to do spatial work. For example, maybe you have data on voter addresses and want to visualize party allegiance. Perhaps, you are wondering who is affected by a certain watershed. If you are limited to postal addresses without being able to visualize the actual location of those addresses the inference is limited. Commuter habits, crime trends, pandemic evolution, and (fill in your example here) analyses are all improved with geocoding. Thanks, geocoding! 


## Geocoding Services 

It is important to recognize that there are many different geocoding platforms. There are others but here is a short list of platforms to consider:

1. [Geocodio](https://www.geocod.io/)
2. [Google's geocode API service](https://developers.google.com/maps/documentation/geocoding/intro)
3. [IPUMS Geomarker](https://geomarker.ipums.org/)
4. [ArcGIS](https://geocode.arcgis.com/arcgis/)

When you are deciding which geocode platform to use some important things to keep in mind are **pricing structures** and other specific features of the platfrom like **bulk geocoding** and **coverage**. For example, Geocodio is much more suited to geocode big data sets than Google's platform. However, Geocodio is only able to geocode within the United States and Cananda whereas Google has international capabilities. Google is better at guessing what location you are trying to geocode ("the White House") than Geocodio, but Geocodio offers census appends. The pricing sturcture is also nuanced across platforms. [Here](https://www.geocod.io/compare/) is a comparison chart provided by Geocodio that gives a flavor of what to consider when deciding which service to use (although you should bear in mind that vendor evaluations may be biased...) Lots to consider! In the end, which platform works best will depend on your preferences and the nature of your project. 




## Keep in Mind

- Be attentive to **accuracy** and **accuracy type**. Just because something is spit out doesn't mean you should use/trust it
- When you use a service like Geocodio, you need to consider pricing (2,500 free lookups per day)
- One size doesn't necesarily fit all--tailor the geocode platform you choose to your project

# Implementations

## Python

[**Geopy**](https://geopy.readthedocs.io/en/stable/) is a Python package thay provides a front end for a large number of geocoding APIs, including [OpenStreetMap](https://www.openstreetmap.org), Bing, Google, ArcGIS, and more. Below is an example of using **geopy**. Users may also want to explore the [**geocoder**](https://geocoder.readthedocs.io/) Python package. We'll use the OpenStreetMap API to do the geocoding. It's important to note that this API has some fair usage conditions including a maximum of 1 request per second, that you provide an informative 'user agent' parameter, and that you clearly display attribution (thank you OpenStreetMap!). For bulk geocoding, you may need to pay a fee to a provider.

```python
# If you don't have it, install geopy using 'pip install geopy'
from geopy.geocoders import Nominatim

# Create a geolocator using Open Street Map (aka Nominatim)
# Use your own user agent identifier here
geolocator = Nominatim(user_agent='LOST_geocoding_page')

# Pass an address to retrieve full location information:
location = geolocator.geocode('Bank of England')

print(location.address)
# >> Bank of England, 8AH, Threadneedle Street, Bishopsgate, City of London,
# England, EC2R 8AH, United Kingdom

print(location.latitude, location.longitude)
# >> 51.51413225 -0.08892476721255456

# We can also reverse geocode from a lat and lon:
scnd_location = geolocator.reverse("51.529969, -0.127688")

print(scnd_location.address)
# >> British Library, 96, Euston Road, Bloomsbury, London Borough of Camden,
# England, NW1 2DB, United Kingdom
```



## rgeocodio (R + Geocodio)

This example will talk specifically about Geocodio and how to use the Goecodio platform in **R studio**. 

### Geocodio
[Geocodio's website](https://www.geocod.io/) is very straight forward, but I will briefly walk through the process:

1. Start by making an account. This account will allow you to do your geocoding with Geocodio as well as get a Geocodio API which we can use in R studio.

2. To geocode on the website you can either upload a spreadsheet or copy and paste addresses into the input window. I highly recommend a spreadsheet which takes a [specific format](https://www.geocod.io/guides/preparing-your-spreadsheet/)

3. Geocodio will ask you to make edits if the data you have provided isn't accurate enough

4. Once your data is in satisfactory form Geodio allows you to make *appends* which allows you to include information pertaining to the addresses you wish to geocode (e.g. what State Legislative District the address is in or Census ACS Demographic information for the addresses you are geocoding)

5. Finally Geocodio will geocode your addresses and return a downloadable csv file. The cost  and the time of this process depends on the size of your data. For example, 250,000 addresses can be geocoded for $123.75 and will take about an hour to process. For estimates of both cost and time click [here](https://www.geocod.io/pricing/)

## Example

rgeocodio allows you to access the Geocodio platform in R studio. Instead of the steps mentioned above you can use the rgeocodio to perform the same functions. 

In order to install `rgeocodio` you will need to load the `devtools` package. Install it if you haven't already `install.packages("devtools")`. Once `devtools` is loaded run:`devtools::install_github('hrbrmstr/rgeocodio')`.

rgeocodio uses an API that you can get from the geocodio website. To get an API visit [geocodio's website](https://www.geocod.io/features/api/). Then save it in your **Renviron**. 

To save the API in your **Renvrion**:
1. Open the **Renviron** by running `usethis::edit_r_environ()` 
2. Once you are in the **Renviron** name and save the API you got from Geocodio. Maybe something like:
```r
#geocodio_API = 'your api`
```
3. Save your **Renviron** and then restart your R session just to be sure that the API is saved.

Now that you have your API saved in R you still need to authorize the API in your R session. Do so by running `gio_auth()`. 
```r
# If necessary
# install.packages(c('rgeocodio','readxl','tidyverse'))

library(rgeocodio)
gio_auth(force = F) 

```
A quick note, `force` makes you set a new geocodio API key for the current environment. In general you will want to run `force=F`. 
Lets try a regeocodio example. Say you want to get the coordinates of the White House. You could run:
```r
rgeocodio::gio_geocode('1600 Pennsylvania Ave NW, Washington DC 20500')
```

Most of these variables are intuitive but I want to spend a few seconds on **accuracy** and **accuracy type** which we can learn more about [here](https://www.geocod.io/docs/#accuracy-score).

1. Accuracy: because geocodio is interpolating the output will tell you how confident geocodio is in its estimation. Anything below 0.8 should be considered not accurate enough, but that is up to the user.

2. Accuracy Type: interpolation uses the closest know geocodes. So if the closest geocodes are, for instance two ends of a street and you are trying to geocode a location somewhere on that street then the accuracy type will be "street." In this case the accuracy type is "rooftop" which means the buildings on either side of the location were used to interpolate your query. Again, [smartystreets](https://smartystreets.com/articles/what-are-geocodes) has a good explanation of this.

What if we want to geocode a bunch of addresses at once? To geocode multiple addresses at once we will use `gio_batch_geocode`. The data that we enter will need to be a *character vector of addresses*. 

```r
library(readxl)
library(tidyverse)

addresses<- c('Yosemite National Park, California', '1600 Pennsylvania Ave NW, Washington DC 20500', '2975 Kincaide St Eugene, Oregon, 97405')

gio_batch_geocode(addresses)
```

You will notice that the output is a list with dataframes of the results embedded. There are a number of ways to extract the relevant data but one approach would be:

```r
addresses<- c('Yosemite National Park, California', '1600 Pennsylvania Ave NW, Washington DC 20500', '2975 Kincaide St Eugene, Oregon, 97405')

extract_function<- function(addresses){

data<-gio_batch_geocode(addresses)
vector<- (1: length(addresses))

df_function<-function(vector){
  df<-data$response_results[vector]
  df<-df%>%as.data.frame()
}

geocode_data<-do.call(bind_rows, lapply(vector, df_function))
return(geocode_data)
}

extract_function(addresses)
```

Reverse geocoding uses `gio_reverse` and `gio_batch_reverse`.

For `gio_reverse` you submit a longitude-latitude pair:

```r
gio_reverse(38.89767, -77.03655)
```

For `gio_batch_reverse` we will submit a vector of numeric entries ordered by c(longitude, latitude):

```r
#make a dataset 
data<-data.frame(
  lat = c(35.9746000, 32.8793700, 33.8337100, 35.4171240),
  lon = c(-77.9658000, -96.6303900, -117.8362320, -80.6784760)
)

gio_batch_reverse(data)
```

Notice that the output gives us multiple accuracy types.

What about geocoding the rest of the world, chico?

```r
rgeocodio::gio_batch_geocode('523-303, 350 Mokdongdong-ro, Yangcheon-Gu, Seoul, South Korea 07987')
```

*gasp* Geocodio only works, from my understanding, in the United States and Canada. We would need to use a different service like **Google's geocoder** to do the rest of the world.
