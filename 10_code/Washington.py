import pandas as pd
import numpy as np
from plot_functions import diff_in_diff_plot, pre_post_plot

###########################################
# Plot diff-in-diff and pre-post for Washington
###########################################

# Washington
mor_pop = pd.read_csv('../20_intermediate_files/mortality_transformed_final.csv')

# ### Diff in Diff
df_treatment_WA = mor_pop[mor_pop['State_Abrv'] == 'WA'].copy()
df_control_WA = mor_pop[(mor_pop['State_Abrv'] == 'UT') | (mor_pop['State_Abrv'] == 'CO') | (mor_pop['State_Abrv'] == 'NC')].copy()
policy_implementation_year_WA = 2012

df_treatment_WA = df_treatment_WA[(df_treatment_WA['YEAR'] >= 2007) & (df_treatment_WA['YEAR'] <= 2015)]
df_control_WA = df_control_WA[(df_control_WA['YEAR'] >= 2007) & (df_control_WA['YEAR'] <= 2015)]

plot = diff_in_diff_plot(df_treatment_WA, df_control_WA, policy_implementation_year_WA, 'Deaths_Per_Cap')
print(plot)

# ### Pre-Post Plots
plot = pre_post_plot(df_treatment_WA, policy_implementation_year_WA, 'Deaths_Per_Cap')
print(plot)
