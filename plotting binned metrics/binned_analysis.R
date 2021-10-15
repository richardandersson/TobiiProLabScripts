# Plot binned data, for Tobii Pro Lab webinar 2021-10-21

# The exported metrics file is of type: AOI-based with binning (.tsv)
# Exported with Tobii Pro Lab 1.171.

# You need packages ggplot2, dplyr, and plotrix installed. {install.packages("NAME")}


library(ggplot2)
#library(dplyr)

dat <- read.delim2("C:/YOUR PATH TO THE FILE/Tobii Pro Lab Demo - Decision Making Metrics AOIbased.tsv",
                  header=TRUE, sep="\t", comment.char="#", fileEncoding="UTF-8")

# Dropping response box AOIs, as they are not that interesting and we want to declutter the plot.
dat <- dat[(!dat$AOI %in% c("I would buy", "I would not buy")),]




dat2 <- dat %>% 
  dplyr::group_by(Participant, Bin, AOI) %>% 
  dplyr::summarise(mean = mean(Total_duration_of_fixations), se=plotrix::std.error(Total_duration_of_fixations))

dat3 <- dat2 %>% # summarizing again from dat2 mean we now have the mean of the means (of each participant)
  dplyr::group_by(Bin, AOI) %>% 
  dplyr::summarise(mean = mean(mean), se=plotrix::std.error(mean))



# Plot: show the total duration of fixations for each bin and AOI (in this case aggregated AOIs).
# Use grand average curves, and confidence band from the standard error of the mean of the participants' means.
ggplot(data=dat3, aes(x=Bin, y=mean, ymin=mean-se, ymax=mean+se, fill=AOI, linetype=AOI)) + 
  geom_smooth() + 
  geom_ribbon(alpha=0.5) + 
  xlab("Bin number") + 
  ylab("Total duration of fixations (ms)") + 
  ggtitle("Total fixation duration per bin per area of interest")

