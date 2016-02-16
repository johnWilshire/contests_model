contests_exp <- read.csv("contest_logs.csv", stringsAsFactors = FALSE)

contests_lin <- read.csv("contest_logs_lin.csv", stringsAsFactors = FALSE)

contests$gen <- as.numeric(contests$gen)
contests$defender_mass <- as.numeric(contests$defender_mass) 
contests$attacker_mass <- as.numeric(contests$attacker_mass)

contests_lin$gen <- as.numeric(contests_lin$gen)
contests_lin$defender_mass <- as.numeric(contests_lin$defender_mass) 
contests_lin$attacker_mass <- as.numeric(contests_lin$attacker_mass)


ggplot(contests_exp, aes( x = factor(gen), y = fight_cost)) +
  geom_boxplot() +
  ggtitle("exp")

ggplot(contests_lin, aes( x = factor(gen), y = fight_cost)) +
  geom_boxplot() +
  ggtitle("lin")

ggplot(contests_exp, aes( x = factor(gen), y = attacker_commitment)) +
  geom_boxplot() +
  ggtitle("exp")

ggplot(contests_lin, aes( x = factor(gen), y = attacker_commitment)) +
  geom_boxplot() +
  ggtitle("lin")
  