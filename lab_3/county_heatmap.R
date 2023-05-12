#install.packages('usmap')
library('usmap')
library('ggplot2')

adf = read.csv('republican_county_adjacencies.csv')
fips = adf$FIPS
district = adf$District


# fips and fake predicted probability:
N = length(fips) # Total number of counties
vals = runif(N) # Predicted probability of going Dem or Rep for each county
df <- data.frame(
  fips = as.character(fips),
  values = vals
) 
plot_usmap(data = df, include = 'VA')+
  scale_fill_continuous(
    low = "blue", high = "red", name = "Affiliation", label = scales::comma
  ) +ggtitle("Predicted Party Affiliation")


# fips and log population:
df <- data.frame(
  fips = as.character(fips),
  values = log(adf$Population2022)
) 
plot_usmap(data = df, include = 'VA')+
  ggtitle("Log Population")



# fips and current district:
df <- data.frame(
  fips = as.character(fips),
  values = factor(adf$District)
) 
plot_usmap(data = df, include = 'VA')+
  ggtitle("Current Districts")


