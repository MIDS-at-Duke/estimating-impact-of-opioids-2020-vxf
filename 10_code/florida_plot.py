import pandas as pd
import numpy as np
from plot_functions import diff_in_diff_plot, pre_post_plot

###########################################
# Plot diff-in-diff and pre-post for Florida
###########################################

# FL
mor_pop = pd.read_csv('../20_intermediate_files/mortality_transformed_final.csv')

# ### Diff in Diff
df_treatment_FL = mor_pop[mor_pop['State_Abrv'] == 'FL'].copy()
df_control_FL = mor_pop[(mor_pop['State_Abrv'] == 'AL') | (mor_pop['State_Abrv'] == 'GA') | (mor_pop['State_Abrv'] == 'SC')].copy()
policy_implementation_year_FL = 2010

df_treatment_FL = df_treatment_FL[(df_treatment_FL['YEAR'] >= 2005) & (df_treatment_FL['YEAR'] <= 2015)]
df_control_FL = df_control_FL[(df_control_FL['YEAR'] >= 2005) & (df_control_FL['YEAR'] <= 2015)]

plot = diff_in_diff_plot(df_treatment_FL, df_control_FL, policy_implementation_year_FL, 'Deaths_Per_Cap')

print(plot)


# ### Pre-Post Plots
plot = pre_post_plot(df_treatment_FL, policy_implementation_year_FL, 'Deaths_Per_Cap')
print(plot)


## Opioid Shipment

op_pop = pd.read_csv('../20_intermediate_files/opioid_transformed_final.csv')
# diff in diff
df_treatment_op_pop_FL = op_pop[op_pop['State_Abrv'] == 'FL'].copy()
df_control_op_pop_FL = op_pop[(op_pop['State_Abrv'] == 'AL') | (op_pop['State_Abrv'] == 'SC') | (op_pop['State_Abrv'] == 'GA')].copy()
policy_implementation_year_FL = 2010


plot = diff_in_diff_plot(df_treatment_op_pop_FL, df_control_op_pop_FL, policy_implementation_year_FL, 'MME_SHIPPED')
print(plot)

# pre-post
plot = pre_post_plot(df_treatment_op_pop_FL, policy_implementation_year_FL, 'MME_SHIPPED')
print(plot)