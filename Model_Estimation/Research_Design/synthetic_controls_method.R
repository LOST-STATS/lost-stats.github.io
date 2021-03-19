pacman::p_load(dplyr, Synth, ggplot2)

data("basque")
data("synth.data")



dataprep_out = dataprep(
  foo = synth.data, 
  predictors = c("X1", "X2", "X3"),
  predictors.op = "mean", 
  time.predictors.prior = c(1984:1989),
  dependent = "Y", 
  unit.variable = "unit.num",
  unit.names.variable = "name", 
  time.variable = "year",
  treatment.identifier = 7, 
  controls.identifier = c(2, 13, 17, 29, 
                          32, 36, 38), 
  time.optimize.ssr = c(1984:1990), 
  time.plot = c(1984:1996)
)

synth_out = dataprep_out %>% synth()

synth_out %>%
  path.plot(dataprep.res = dataprep_out, tr.intake = 1990)

synth_control = dataprep_out$Y0plot %*% synth_out$solution.w




table_basque = synth.tab(synth.res = synth_basque,
                         dataprep.res = dataprep_basque)


W = synth_basque$solution.w
Y_0 = dataprep_basque$Y0plot
Y_1 = dataprep_basque$Y1plot
control = Y_0 %*% W

plot = tibble("year" = c(1955:1997), "treatment" = Y_1, "control" = control) %>%
  ggplot(aes(x = year)) +
  geom_line(mapping = aes(y = treatment), col = "blue") +
  geom_line(mapping = aes(y = control), col = "red")















