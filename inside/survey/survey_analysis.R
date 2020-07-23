library(tidyverse)
library(ggplot2)
library(ggpubr)

survey <- read.csv(file = 'survey_all.csv',sep = ',')
complexity <- survey[survey$questiontype == 'complexity',]
interest <- survey[survey$questiontype == 'interest',]
attention <- survey[survey$questiontype == 'attention',]
positive <- survey[survey$questiontype == 'positive',]
negative <- survey[survey$questiontype == 'negative',]
arouse <- survey[survey$questiontype == 'arouse',]
calm <- survey[survey$questiontype == 'calm',]
real <- survey[survey$questiontype == 'real',]

#convert to long form
complexity <- gather(complexity, stimulus, rating, day_kit, day_bat, day_bed, day_off, day_liv, night_bat, night_bed, night_liv, night_kit, night_off, new_kit, new_bat, new_bed, new_off, new_liv)
interest <- gather(interest, stimulus, rating, day_kit, day_bat, day_bed, day_off, day_liv, night_bat, night_bed, night_liv, night_kit, night_off, new_kit, new_bat, new_bed, new_off, new_liv)
attention <- gather(attention, stimulus, rating, day_kit, day_bat, day_bed, day_off, day_liv, night_bat, night_bed, night_liv, night_kit, night_off, new_kit, new_bat, new_bed, new_off, new_liv)
positive <- gather(positive, stimulus, rating, day_kit, day_bat, day_bed, day_off, day_liv, night_bat, night_bed, night_liv, night_kit, night_off, new_kit, new_bat, new_bed, new_off, new_liv)
negative <- gather(negative, stimulus, rating, day_kit, day_bat, day_bed, day_off, day_liv, night_bat, night_bed, night_liv, night_kit, night_off, new_kit, new_bat, new_bed, new_off, new_liv)
arouse <- gather(arouse, stimulus, rating, day_kit, day_bat, day_bed, day_off, day_liv, night_bat, night_bed, night_liv, night_kit, night_off, new_kit, new_bat, new_bed, new_off, new_liv)
calm <- gather(calm, stimulus, rating, day_kit, day_bat, day_bed, day_off, day_liv, night_bat, night_bed, night_liv, night_kit, night_off, new_kit, new_bat, new_bed, new_off, new_liv)
real <- gather(real, stimulus, rating, day_kit, day_bat, day_bed, day_off, day_liv, night_bat, night_bed, night_liv, night_kit, night_off, new_kit, new_bat, new_bed, new_off, new_liv)

#plot results
#complexity
View(compare_means(rating ~ stimulus,  data = complexity))
png(file="complexity.png",width=1000, height=550)
ggboxplot(complexity, x = "stimulus", y = "rating",
          color = "stimulus")+
  stat_compare_means()
dev.off()
#interest
View(compare_means(rating ~ stimulus,  data = interest))
png(file="interest.png",width=1000, height=550)
ggboxplot(interest, x = "stimulus", y = "rating",
          color = "stimulus")+
  stat_compare_means()
dev.off()
#attention
View(compare_means(rating ~ stimulus,  data = attention))
png(file="attention.png",width=1000, height=550)
ggboxplot(attention, x = "stimulus", y = "rating",
          color = "stimulus")+
  stat_compare_means()
dev.off()
#positive
View(compare_means(rating ~ stimulus,  data = positive))
png(file="positive.png",width=1000, height=550)
ggboxplot(positive, x = "stimulus", y = "rating",
          color = "stimulus")+
  stat_compare_means()
dev.off()
#negative
View(compare_means(rating ~ stimulus,  data = negative))
png(file="negative.png",width=1000, height=550)
ggboxplot(negative, x = "stimulus", y = "rating",
          color = "stimulus")+
  stat_compare_means()
dev.off()
#arouse
View(compare_means(rating ~ stimulus,  data = arouse))
png(file="arouse.png",width=1000, height=550)
ggboxplot(arouse, x = "stimulus", y = "rating",
          color = "stimulus")+
  stat_compare_means()
dev.off()
#calm
View(compare_means(rating ~ stimulus,  data = calm))
png(file="calm.png",width=1000, height=550)
ggboxplot(calm, x = "stimulus", y = "rating",
          color = "stimulus")+
  stat_compare_means()
dev.off()
#real
View(compare_means(rating ~ stimulus,  data = real))
png(file="real.png",width=1000, height=550)
ggboxplot(real, x = "stimulus", y = "rating",
          color = "stimulus")+
  stat_compare_means()
dev.off()
