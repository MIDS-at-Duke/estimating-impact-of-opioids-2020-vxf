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
    
    df_treatment['standardized_year'] = df_treatment['YEAR'] - policy_implementation_year
    df_control['standardized_year'] = df_control['YEAR'] - policy_implementation_year
    
    lower_lim = df_treatment['standardized_year'].min()
    upper_lim = df_treatment['standardized_year'].max()
    
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
    + xlab('standardized_year') + ylab(resp_variable)
    + scale_x_continuous(breaks=range(lower_lim,upper_lim,1))
        
    )

    return plot


# # Pre Post Plot
def pre_post_plot(df_treatment, policy_implementation_year, resp_variable):
    
    df_treatment['standardized_year'] = df_treatment['YEAR'] - policy_implementation_year
    
    lower_lim = df_treatment['standardized_year'].min()
    upper_lim = df_treatment['standardized_year'].max()
    
    plot = (
    ggplot() +
    geom_smooth(df_treatment[df_treatment['standardized_year'] < 0], 
                aes(x='standardized_year', y=resp_variable, color='treatment_status'), method='lm') + 
    geom_smooth(df_treatment[df_treatment['standardized_year'] >= 0], 
                aes(x='standardized_year', y=resp_variable, color='treatment_status'), method='lm')
        
    + geom_vline(xintercept = 0) 
    + xlab('standardized_year') + ylab(resp_variable)
    + scale_x_continuous(breaks=range(lower_lim,upper_lim,1))
        
    )

    return plot