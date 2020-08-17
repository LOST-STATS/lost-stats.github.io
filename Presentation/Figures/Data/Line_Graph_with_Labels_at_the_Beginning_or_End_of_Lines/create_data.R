library(gtrendsR)
library(tidyverse)
library(Hmisc)
library(lubridate)

# Request made at 10:26PM PST on Oct. 20, 2019
gt <- gtrends(keyword = c('physics nobel',
                          'chemistry nobel',
                          'medicine nobel',
                          'economics nobel'),
              time = 'today 1-m')

gttime <- gt$interest_over_time

gttime <- gttime %>%
  select(-time, -gprop, -category) %>%
  mutate(name = capitalize(str_replace(keyword," nobel","")),
         hits = as.numeric(str_replace(hits,"<1","0")),
         date = ymd(date))

write_csv(gttime, 'Research_Nobel_Google_Trends.csv')
