
if (!require("pacman")) install.packages("pacman")
pacman::p_load(dplyr, MatchIt, here, ggthemes)
here::i_am("matching.R")
ecls <- read.csv("ecls.csv")

ecls <- ecls %>% mutate(w3income_1k = w3income / 1000)
m_ps <- glm(catholic ~ race_white + w3income_1k + p5hmage + p5numpla + w3momed_hsb,
            family = binomial(), data = ecls)
summary(m_ps)

prs_df <- data.frame(pr_score = predict(m_ps, type = "response"),
                     catholic = m_ps$model$catholic)
head(prs_df)

ggplot(prs_df, aes(pr_score, fill = as.factor(catholic))) + 
  geom_density(alpha=0.1) + 
  theme_pander(base_size = 12, 
               base_family = "Fira Sans Book") +
  xlab("Probability of Going to Catholic School") +
  scale_fill_discrete(name = "", labels = c("Non-Catholic School", "Catholic School")) 

ecls_cov <- c('race_white', 'p5hmage', 'w3income', 'p5numpla', 'w3momed_hsb')
ecls_nomiss <- ecls %>%
  select(c5r2mtsc_std, catholic, one_of(ecls_cov)) %>%
  na.omit()
mod_match <- matchit(catholic ~ race_white + w3income + p5hmage + p5numpla + w3momed_hsb, method = "nearest", data = ecls_nomiss)
summary(mod_match)

dta_m <- match.data(mod_match)

lm_treat1 <- lm(c5r2mtsc_std ~ catholic, data = dta_m)
summary(lm_treat1)

lm_treat2 <- lm(c5r2mtsc_std ~ catholic + race_white + p5hmage +
                  I(w3income / 10^3) + p5numpla + w3momed_hsb, data = dta_m)
summary(lm_treat2)