
# Voting Data
df_VA = df[df$state =='VIRGINIA',]
write.csv(df_VA,file='voting_VA.csv')
head(df_VA)


# Census Data
