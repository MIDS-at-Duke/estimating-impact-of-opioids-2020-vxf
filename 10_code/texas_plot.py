import pandas as pd
import numpy as np
from plot_functions import diff_in_diff_plot, pre_post_plot

###########################################
# Plot diff-in-diff and pre-post for Texas
###########################################

# Texas
mor_pop = pd.read_csv('../20_intermediate_files/mortality_transformed_final.csv')

# ### Diff in Diff
df_treatment_TX = mor_pop[mor_pop['State_Abrv'] == 'TX'].copy()
df_control_TX = mor_pop[(mor_pop['State_Abrv'] == 'AZ') | (mor_pop['State_Abrv'] == 'CA') | (mor_pop['State_Abrv'] == 'OK')].copy()
policy_implementation_year_TX = 2007

plot = diff_in_diff_plot(df_treatment_TX, df_control_TX, policy_implementation_year_TX, 'Deaths_Per_Cap')
print(plot)


# ### Pre-Post Plots
plot = pre_post_plot(df_treatment_TX, policy_implementation_year_TX, 'Deaths_Per_Cap')
print(plot)
