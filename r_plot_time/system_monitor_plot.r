library(ggplot2)

data <- read.table("c:\\backup\\src\\prd6287\\system_monitor_parser_tinky.csv",
                   header=TRUE,
                   sep=",",
                   quote="\"")
data$timestamp_obj <- as.POSIXct(data$timestamp, format="%Y:%M:%D %H:%M:%S")
dfm1 <- melt(data, id="timestamp_obj", measure=c("kernel_size", "total_process_rss", "page_cache_size", "used_memory"))

# variable scales
# qplot(timestamp_obj, value, data=dfm1, geom="line", colour=variable) + facet_grid(facets = variable ~ ., scales="free") + opts(title=expression("aku"))

# constant scales
qplot(timestamp_obj, value, data=dfm1, geom="line", colour=variable) + facet_grid(facets = variable ~ .) + opts(title=expression("tinky"), panel.grid.major = theme_line("grey", size=0.1))
