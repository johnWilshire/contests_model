# what is what we are plotting the density of
# returns a ggplot2 object
density_plot <- function (data, x = "patch_area", y, title) {
  return(
    ggplot(data, aes_string(x = x, y = y)) + 
    stat_density2d(aes(fill = ..density.. ), geom = "tile", contour = FALSE) + 
    ggtitle(title)
  )
}

# plots the number of winners
winners_plot <- function (df){
  plot( table( df$patch_area), 
        ylab = "Number of Winning Males", 
        xlab = "Patch Size",
        main = "Winning males"
  )
}

# plots k parameter 
k_density_plot <- function(df) {
  density_plot(df, "k", "Aggression parameter k density")
}

# plots e_0 density against area
e_0_density_plot <- function(df) {
  density_plot(df, "e_0", "Aggression parameter e_0 density")
}

# plots exploration trait density
exploration_density_plot <- function (df){
  df$exploration <- 2 * df$speed * df$radius
  density_plot(df, "exploration", "Exploration Trait density")
}

# select the last generation 
# and adds some different variables
get_generation <- function(m, gen){
  final <- m[m$generation == gen,]
  final$total_e <- final$contest_energy + final$occupying_energy + final$search_energy
  final$contest_as_pc <- final$contest_energy / final$total_e
  final$occupying_as_pc <- final$occupying_energy / final$total_e
  final$search_as_pc <- final$search_energy / final$total_e
  final$e_per_winner <- final$total_e / final$num_winners
  return(final)
}

commitment <- seq(0,5, by = 0.01)

escalation_curve <- function (t){
  t^2
}

example_escalation <- function (){
  commitment <- seq(0,5, by = 0.01)
  escalation_curve <- function (t){
    t^2
  }
  df <- data.frame("Commitment" = commitment, "Intensity" = escalation_curve(commitment))
  ggplot(df,  aes( x = Commitment, y = Intensity )) +
    geom_line() +
    geom_vline(xintercept = 3) + 
    geom_vline(xintercept = 4) +
    geom_polygon(data = rbind(c(0,0), subset(df, commitment < 3), c(3, 0)), 
                 aes(alpha = 0.3, fill = "")) + 
    guides(fill = FALSE, alpha = FALSE) + 
    annotate("text", x = 2.8, y = 10, label = "c_ i") +
    annotate("text", x = 3.8, y = 20, label = "c_ j")
}


# returns a dataframe that can be used to make plots that show the % energy spending
as_stackable_pc <- function (m){
  contest <- data.frame("patch_area" = m$patch_area, "energy" = m$contest_as_pc, "type" = "contest")
  search <- data.frame("patch_area" = m$patch_area, "energy" = m$search_as_pc, "type" = "search")
  occupy <- data.frame("patch_area" = m$patch_area, "energy" = m$occupying_as_pc, "type" = "occupying")
  return(rbind(contest, search, occupy))
}

# returns a dataframe that can be used to show the total energy used at a generation
# for patch area
as_stackable_total <- function (m){
  contest <- data.frame("patch_area" = m$patch_area, "energy" = m$contest_energy, "type" = "contest")
  search <- data.frame("patch_area" = m$patch_area, "energy" = m$search_energy, "type" = "search")
  occupy <- data.frame("patch_area" = m$patch_area, "energy" = m$occupying_energy, "type" = "occupying")
  return(rbind(contest, search, occupy))
}

# returns a ggplot2 object
# this plot doesnt show the multiple clusters
# not very good as it doesnt show co-existence
history_plot <- function(df, what, bounds,  title) {
  return(
    ggplot(data = df, aes(patch_area)) +
      geom_ribbon(
        aes_string(
          ymin = paste(what, "-", bounds),
          ymax = paste(what, "+", bounds)
        ),
        fill = "grey70") +
      geom_line(aes_string(y = what)) +
      ggtitle(title)
  )
}

# returns a ggplot2 object
energy_stack_plot <- function (df, title, what="patch_area"){
  return(
    ggplot(df, aes_string(x = what, y = "energy")) + 
      geom_area(aes(fill = type)) + 
      ggtitle(title)
  )
}

# wrapper for a % energy plot
energy_pc_plot <- function (m, what="patch_area"){
  energy_stack_plot(as_stackable_pc(m), 
    "Energy spending across population", what)
}

# wrapper for a less "full plot that shows the decline in energy"
energy_total_plot <- function(m){
  energy_stack_plot(as_stackable_total(m), 
      "Energy spending across population")
}


# plyr is so cool
# split on patch area, apply culstering, reapply
clustered_plot <- function(dff, select_every = 200, title ="Coexistance", what, ylab){
  pamk_clusters <- ddply(dff[dff$patch_area %in% seq(min(dff$patch_area), max(dff$patch_area), by = select_every), ],
                         .variables = .(patch_area), 
                         .fun = function (df){
                           m <- pamk(df[what], krange = 1:3, alpha = 1e-12)
                           cluster <- m$pamobject$clustering
                           mediod <- m$pamobject$medoids[cluster]
                           distance <- m$pamobject$clusinfo[cluster, "diameter"]
                           nc <- max(cluster)
                           unique(data.frame(cluster, mediod, distance, nc))
                         })
  
  ggplot(pamk_clusters, aes(x = patch_area, y = mediod)) +
    geom_errorbar(aes( ymin = mediod - (distance/2), ymax = mediod + (distance/2))) +
    geom_point(aes(col=as.factor(nc))) + 
    ylab(ylab) + 
    ggtitle(title) + 
    scale_colour_discrete(name="Number\nof\nClusters")
}

trait_evolution_plot <- function(df, what, title){
  return(
    ggplot(df, aes_string(x = "generation", y = what, group = "patch_area" )) +
      geom_line(aes(col = patch_area)) +
      ggtitle(title)
  )
}


# plots the given trait against patch area
# takes a population (not trait history)
# like a clearer density plot...
pop_values <- function (df, x, y, title){
  ggplot(df, aes_string(x = x, y = y)) + 
    geom_point() +
    ggtitle(title)
}


# visualise how contest traits change with increasing density
# takes a population (not a history)
# creates a gif at the filepath given
# with the given title string
# if delete pngs it cleans up the contest_gif directory
trait_scatter_gif <- function(dataset, filepath = "../scrap/contest_gifs/", 
                              progress = TRUE,
                              plot_title = "my_gif",
                              delete_pngs = FALSE){
  
  # get the limits
  k_limits = c(min(dataset$k), max(dataset$k))
  e_0_limits = c(min(dataset$e_0), max(dataset$e_0))
  
  # create the pngs
  # dlply split dataframe return list of dataframes
  for (simulation in dlply(dataset, .(patch_area))){
    filename <- sprintf("%06d_%s.png", simulation$patch_area[1], plot_title)
    filename <- paste(filepath, filename, sep = "")
    if(progress) print(filename)
    
    png(filename = filename)
    print(
      ggplot(simulation, aes(x = k, y = e_0)) +
        geom_point() +
        scale_x_continuous(limits=k_limits) +
        scale_y_continuous(limits=e_0_limits) +
        ggtitle(paste(plot_title, "Patch Area", simulation$patch_area[1], 
                      "Density: ", log(simulation$N[1] / simulation$patch_area[1])))
    )
    dev.off()
  }
  
  # this makes the gifs
  # I am not sure if this will work on mac...
  command <- paste("convert -delay 20 -loop 0 ", filepath,"*.png ", filepath, plot_title,".gif", sep = "")
  if (progress) print(command)
  system(command)
  
  # deleting the pngs
  # THIS COULD FUCK UP YOUR SHIT IF YOUR PLOT TITLE HAS A " " in it
  command <- paste("rm ", filepath, "*", plot_title, ".png", sep = "")
  if (progress) print(command)
  if(delete_pngs) system(command)
  
}

