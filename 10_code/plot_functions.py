##################################################
# Contains functions for diff-in-diff plot 
# and pre-post plot.
##################################################
import pandas as pd
import numpy as np
import os
import sys
from plotnine import *

# # Diff in Diff Plot
def diff_in_diff_plot(df_treatment, df_control, policy_implementation_year, resp_variable):
    
    treatment_state = str(list(df_treatment.STATE.unique())[0])
    
    df_treatment['standardized_year'] = df_treatment['YEAR'] - policy_implementation_year
    df_control['standardized_year'] = df_control['YEAR'] - policy_implementation_year
    
    lower_lim = df_treatment['standardized_year'].min()
    upper_lim = df_treatment['standardized_year'].max()+1
    
    plot = (
    ggplot() +
    geom_smooth(df_treatment[df_treatment['standardized_year'] < 0], 
                aes(x='standardized_year', y=resp_variable, color='treatment_status'), method='lm') + 
    geom_smooth(df_treatment[df_treatment['standardized_year'] >= 0], 
                aes(x='standardized_year', y=resp_variable, color='treatment_status'), method='lm') + 
        
    geom_smooth(df_control[df_control['standardized_year'] < 0], 
                aes(x='standardized_year', y=resp_variable, color='treatment_status'), method='lm') + 
    geom_smooth(df_control[df_control['standardized_year'] >= 0], 
                aes(x='standardized_year', y=resp_variable, color='treatment_status'), method='lm')
    + geom_vline(xintercept = 0) 
    + xlab('Years before/after Policy Implementation Year: '+str(policy_implementation_year) 
    + '. \nRepresented as "0" on the x-axis.') 
    + ylab(str(resp_variable) + ' \n(Adding 95% confidence interval)')
    + scale_x_continuous(breaks=range(lower_lim,upper_lim,1))
    + labs(title=str("Difference in Difference Plot - "+treatment_state))
        
    )
    return plot


# # Pre Post Plot
def pre_post_plot(df_treatment, policy_implementation_year, resp_variable):
    
    treatment_state = str(list(df_treatment.STATE.unique())[0])
    
    df_treatment['standardized_year'] = df_treatment['YEAR'] - policy_implementation_year
    
    lower_lim = df_treatment['standardized_year'].min()
    upper_lim = df_treatment['standardized_year'].max()+1
    
    plot = (
    ggplot() +
    geom_smooth(df_treatment[df_treatment['standardized_year'] < 0], 
                aes(x='standardized_year', y=resp_variable, color='treatment_status'), method='lm') + 
    geom_smooth(df_treatment[df_treatment['standardized_year'] >= 0], 
                aes(x='standardized_year', y=resp_variable, color='treatment_status'), method='lm')
        
    + geom_vline(xintercept = 0) 
    + xlab('Years before/after Policy Implementation Year: '+str(policy_implementation_year) 
    + '. \nRepresented as "0" on the x-axis.') 
    + ylab(str(resp_variable) + ' \n(Adding 95% confidence interval)')
    + scale_x_continuous(breaks=range(lower_lim,upper_lim,1))
    + labs(title=str("Pre Post Plot - "+treatment_state))
        
    )

    return plot