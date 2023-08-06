#!/usr/bin/env Rscript

####################################### define functions #######################################

check.packages <- function(pkg){
    new.pkg <- pkg[!(pkg %in% installed.packages()[, "Package"])]
    if (length(new.pkg))
        install.packages(new.pkg, dependencies = TRUE)
    sapply(pkg, require, character.only = 1)
}

split_list_element = function(list_in, sep_symbol){
  
  list_in_split = strsplit(list_in, sep_symbol)
  
  group_list = c()
  for (element in list_in_split){
    group_list = c(group_list, element[1])
  }
  
  return(group_list)
}

remove_zero_rows_cols = function(matrix_in){
  
  remove_zero_rows = function(matrix_in){
    
    row_sum = rowSums(matrix_in)
    mat_with_row_sum = cbind(matrix_in, row_sum)
    mat_non_zero_row_tmp = mat_with_row_sum[mat_with_row_sum$row_sum > 0, ]
    mat_non_zero_row = subset(mat_non_zero_row_tmp, select = -c(row_sum))
    
    return(mat_non_zero_row)
  }
  
  mat_non_zero_row = remove_zero_rows(mat)
  mat_non_zero_row_t = as.data.frame(t(mat_non_zero_row))
  mat_non_zero_row_col_t = remove_zero_rows(mat_non_zero_row_t)
  mat_non_zero_row_col = t(mat_non_zero_row_col_t)
  
  return(mat_non_zero_row_col)
}

####################################### install packages #######################################

packages<-c("optparse", "circlize")
invisible(suppressMessages(check.packages(packages)))

####################################### argument parser ######################################

options(warn=-1)

option_list = list(
  
  make_option(c("-m", "--matrix"), type="character", help="input matrix"),
  make_option(c("-p", "--plot"),   type="character", help="output plot"));

within_group_gap = 1
between_group_gap = 6
group_separator = '____'

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

mat = read.table(opt$matrix, header = TRUE)

png(filename=opt$plot, units="in", width=25, height=25, pointsize=12, res=300)
grid.col = c(A = 'brown1', B = 'lawngreen', C = 'mediumorchid', D = 'mediumslateblue', E = 'royalblue', F = 'sandybrown')
par(mar = rep(0,4), cex = 1.2)

# set label_order
label_order = sort(union(rownames(mat), colnames(mat)))

# Set larger gaps between groups
label_order_on_plot = sort(union(rownames(remove_zero_rows_cols(mat)), colnames(remove_zero_rows_cols(mat))))
group_list_on_plot = split_list_element(label_order_on_plot, group_separator)
gap_between_group_list = c()
last_group = 'None'
for(group_id in group_list_on_plot){
  if (last_group == 'None'){
    last_group = group_id
  } else if (group_id == last_group){
    gap_between_group_list = c(gap_between_group_list, within_group_gap)
  } else if (group_id != last_group){
    gap_between_group_list = c(gap_between_group_list, between_group_gap)
    last_group = group_id
  }
}

if (group_list_on_plot[[1]] == group_list_on_plot[[length(group_list_on_plot)]]){
  gap_between_group_list = c(gap_between_group_list, within_group_gap)
} else {
  gap_between_group_list = c(gap_between_group_list, between_group_gap)
}

# Set larger gaps between groups
circos.par(gap.after = gap_between_group_list)

# plot chordDiagram
chordDiagram(t(mat), order = label_order, annotationTrack = "grid", preAllocateTracks = 1, grid.col = grid.col)

# add extra track
color_list = terrain.colors(length(label_order_on_plot))
current_group = 'None'
current_group_member = c()
for (label in label_order_on_plot){
  label_split = strsplit(label, group_separator)
  label_group = label_split[[1]][1]
  if (current_group == 'None'){
    current_group = label_group
    current_group_member = c(current_group_member, label)
  } else if (label_group == current_group){
    current_group_member = c(current_group_member, label)
  } else if (label_group != current_group){
    highlight.sector(current_group_member, track.index = 1, col = sample(terrain.colors(length(label_order_on_plot)), 1), padding=c(0, 0, 0.3, 0), niceFacing = TRUE)
    #highlight.sector(current_group_member, track.index = 1, col = randomColor(), padding=c(0, 0, 0.3, 0), niceFacing = TRUE)
    current_group = label_group
    current_group_member = c(label)
  }
}

highlight.sector(current_group_member, track.index = 1, col = sample(terrain.colors(30), 1), padding=c(0, 0, 0.3, 0), niceFacing = TRUE)
# highlight.sector(current_group_member, track.index = 1, col = "lightblue", padding=c(0, 0, 0.3, 0), text = '', cex = 0.8, text.col = "black", niceFacing = TRUE)

# rorate label
circos.trackPlotRegion(track.index = 1, panel.fun = function(x, y) {
  xlim = get.cell.meta.data("xlim")
  ylim = get.cell.meta.data("ylim")
  sector.name = get.cell.meta.data("sector.index")
  circos.text(mean(xlim), ylim[1] + .1, sector.name, facing = "clockwise", niceFacing = TRUE, adj = c(0, 0.5))
  circos.axis(h = "top", labels.cex = 0.5, major.tick.percentage = 0.2, sector.index = sector.name, track.index = 2)
}, bg.border = NA)


#circos.track(circos.text, facing = "clockwise")
invisible(dev.off())

circos.clear()

rm(list=ls())
