source("R/load_datasets.R")
#source("R/make_plots.R")
library(plyr)
library(jsonlite)
library(ggplot2)
library(dplyr)
library(fpc)

m <- load_population(directory = "data")
#`h <- load_trait_history("data")


# qplot(m$generation, m$k)
# qplot(m$gen, m$e_0)

e <- ggplot(m, aes(x = generation, y = e_0))

# e + geom_point(aes(col = as.factor(patch_area)))
  

e + geom_point() + 
  facet_grid(. ~ patch_area)

ggplot(m, aes(x = generation, y = k)) + geom_point(aes(alpha = 0.01)) + 
  facet_grid(. ~ patch_area)


gplot(m, aes(x = generation, y = maturation_t1ime)) +
  geom_point(aes(col = as.factor(patch_area)))


e_dens <- e + stat_density_2d(geom = "raster", aes(fill = ..density..), contour = FALSE)


#clustered_plot(m, select_every = 1, what = "e_0")



e + 
  stat_density_2d(geom = "raster", aes(fill = ..density..), contour = FALSE) +
  scale_fill_distiller(palette = "Spectral") + 
  facet_grid(. ~ patch_area)

ggplot(m, aes(x = generation, y = k)) + 
  stat_density_2d(geom = "raster", aes(fill = ..density..), contour = FALSE) +
  scale_fill_distiller(palette = "Spectral") + 
  facet_grid(. ~ patch_area)

#BrBG, PiYG, PRGn, PuOr, RdBu, RdGy, RdYlBu, RdYlGn, Spectral
#e_dens + scale_fill_distiller(palette = "set2")

#qplot(h$generation, h$search_energy)

#ggplot(h, aes(generation, contest_energy)) + geom_line()


