#install.packages('usmap')
library('usmap')
library('ggplot2')

df = read.csv('county_adjacencies.csv')
head(df)

N = dim(df)[1]
units = df[,1]
conn = df[,5:dim(df)[2]]
A = matrix(0,N,N)
rownames(A) = units
colnames(A) = units
fips = df$FIPS

# Build an adjacency matrix:
for( i in 1:N){
  conn_i = match(conn[i,],units)
  conn_i = conn_i[ is.na(conn_i)==FALSE]
  A[i,conn_i] = 1
}

sum( !(A == t(A)) )  # Symmetric matrix? 
for(i in 1:N){
  for(j in 1:N){
    if(A[i,j]>A[j,i]){
      print( paste(units[j],units[i],sep=' is missing a link to ') )
    }
  }
}


# Plot all adjacency maps for visual check:
for( i in 1:N){
  neighbors = match( conn[i,], units )
  neighbors = neighbors[is.na(neighbors)==FALSE]
  nighbors = c(neighbors,i)
  highlight = matrix(0,N,1)
  highlight[neighbors]=1
  highlight[i]=2
  #
  gdf <- data.frame(
    fips = as.character(fips),
    values = highlight
  )
  #
  plot = plot_usmap(data = gdf, include = 'VA')+
    scale_fill_continuous(low = "white", high = "black", 
                          name = "Affiliation", label = scales::comma)+
    ggtitle(units[i])
  #
  print(plot)
}





