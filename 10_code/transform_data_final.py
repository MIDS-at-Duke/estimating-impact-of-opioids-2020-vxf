##########################################################################
# This script ingests the mortality and opioid shipment data and merges 
# it with the population census data, to derive the opioid mortality 
# rates and opioid shipment rates.
##########################################################################
import pandas as pd
import numpy as np


# Load Mortality Data
mortality = pd.read_csv('../20_intermediate_files/mortality_non_aggregated.csv')
mortality = mortality.drop('Unnamed: 0', axis =1)


# Derive full-state names.
mortality.loc[mortality['State'] == 'AL', 'STATE'] = 'Alabama'
mortality.loc[mortality['State'] == 'FL', 'STATE'] = 'Florida'
mortality.loc[mortality['State'] == 'SC', 'STATE'] = 'South Carolina'
mortality.loc[mortality['State'] == 'GA', 'STATE'] = 'Georgia'
mortality.loc[mortality['State'] == 'TX', 'STATE'] = 'Texas'
mortality.loc[mortality['State'] == 'OK', 'STATE'] = 'Oklahoma'
mortality.loc[mortality['State'] == 'WA', 'STATE'] = 'Washington'
mortality.loc[mortality['State'] == 'NC', 'STATE'] = 'North Carolina'
mortality.loc[mortality['State'] == 'CO', 'STATE'] = 'Colorado'
mortality.loc[mortality['State'] == 'AZ', 'STATE'] = 'Arizona'
mortality.loc[mortality['State'] == 'CA', 'STATE'] = 'California'
mortality.loc[mortality['State'] == 'UT', 'STATE'] = 'Utah'

StateL = ['Florida', 'Alabama', 'South Carolina', 'Georgia', 'Texas', 'Arizona', 
          'California', 'Oklahoma','Washington','North Carolina','Utah','Colorado']


mortality = mortality[mortality['STATE'].isin(StateL)]
mortality.columns = ['YEAR', 'State_Abrv', 'COUNTY', 'DEATHS', 'STATE']
mortality['YEAR'] = mortality['YEAR'].astype(int)


# ### Import Population Dataset
pop_2000_to_2010 = pd.read_csv('../00_source/co-est00int-tot.csv', encoding='latin-1')
pop_2000_to_2010 = pop_2000_to_2010[['STNAME', 'CTYNAME',
                                    'POPESTIMATE2000', 'POPESTIMATE2001', 'POPESTIMATE2002',
                                    'POPESTIMATE2003', 'POPESTIMATE2004', 'POPESTIMATE2005',
                                    'POPESTIMATE2006', 'POPESTIMATE2007', 'POPESTIMATE2008',
                                    'POPESTIMATE2009', 'POPESTIMATE2010']]



pop_2000_to_2010 = pop_2000_to_2010.melt(id_vars=['STNAME', 'CTYNAME'])
pop_2000_to_2010.columns = ['STATE', 'COUNTY', 'YEAR', 'TOTAL_POP']
pop_2000_to_2010['YEAR'] = [x[-4:] for x in pop_2000_to_2010['YEAR'].tolist()]

pop_2010_to_2019 = pd.read_csv('../00_source/co-est2019-alldata.csv', encoding='latin-1')
pop_2010_to_2019 = pop_2010_to_2019[['STNAME', 'CTYNAME', 'POPESTIMATE2011',
                                    'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014',
                                    'POPESTIMATE2015', 'POPESTIMATE2016', 'POPESTIMATE2017',
                                    'POPESTIMATE2018', 'POPESTIMATE2019']]


pop_2010_to_2019 = pop_2010_to_2019.melt(id_vars=['STNAME', 'CTYNAME'])
pop_2010_to_2019.columns = ['STATE', 'COUNTY', 'YEAR', 'TOTAL_POP']
pop_2010_to_2019['YEAR'] = [x[-4:] for x in pop_2010_to_2019['YEAR'].tolist()]

pop_df = pop_2000_to_2010.append(pop_2010_to_2019)
pop_df = pop_df.sort_values(['YEAR', 'STATE', 'COUNTY'])
pop_df = pop_df.reset_index(drop=True)
pop_df['YEAR'] = pop_df['YEAR'].astype(int)

pop_df['COUNTY_Abrv'] = [x[:-7] for x in pop_df['COUNTY']]
pop_df['COUNTY_Abrv'] = pop_df['COUNTY_Abrv'].str.upper()

StateL = ['Florida', 'Alabama', 'South Carolina', 'Georgia', 'Texas', 'Arizona', 
          'California', 'Oklahoma','Washington','North Carolina','Utah','Colorado']

pop_df = pop_df[pop_df['STATE'].isin(StateL)]
pop_df = pop_df[(pop_df['YEAR'] >= 2003) & (pop_df['YEAR'] <= 2015)]


# ### Merging Mortality Rate and Population Dataset
merge_cols = ['YEAR', 'STATE','COUNTY']
mor_pop = pd.merge(pop_df, mortality, how='left', on=merge_cols, indicator = True)
mor_pop = mor_pop[['YEAR', 'STATE', 'State_Abrv', 'COUNTY', 'DEATHS', 'TOTAL_POP', '_merge']]
mor_pop.columns = ['YEAR', 'STATE', 'State_Abrv', 'COUNTY', 'DEATHS', 'TOTAL_POP', '_merge_old']


mor_pop['COUNTY'] = mor_pop['COUNTY'].str.upper()
mor_pop['COUNTY_Abrv'] = [x[:-7] for x in mor_pop['COUNTY'].tolist()]


# ### Handle Missing Mortality data counties
state_grouped = mor_pop[['YEAR', 'STATE', 'DEATHS','TOTAL_POP']].groupby(['YEAR', 'STATE'], as_index=False).sum()
state_grouped['mortality_rate_state_avg'] = state_grouped['DEATHS'] / state_grouped['TOTAL_POP']

merge_cols = ['YEAR', 'STATE']
mor_pop = pd.merge(mor_pop, state_grouped[['YEAR', 'STATE','mortality_rate_state_avg']], how='inner', on=merge_cols, indicator = True)


def derive_deaths(row):
    if np.isnan(row['DEATHS']):
        row['DEATHS'] = round(min(10,row['TOTAL_POP'] * row['mortality_rate_state_avg']))

    return row['DEATHS']

mor_pop['DEATHS'] = mor_pop.apply(derive_deaths, axis=1)
mor_pop.head()


# ### Calculate Mortality/Deaths Per Capita
mor_pop['Deaths_Per_Cap'] = mor_pop['DEATHS'] / mor_pop['TOTAL_POP']

treatment_list = ['FL', 'WA', 'TX']
mor_pop['treatment_status'] = 'Control'
mor_pop.loc[mor_pop['State_Abrv'].isin(treatment_list), 'treatment_status'] = 'Treatment'
mor_pop['treatment_status'] = pd.Categorical(mor_pop['treatment_status'])



# # Opioid Shipment Analysis
# ### Note: 
# This part only needs to be run once. The data has been extracted to a csv file for later steps
# ### Load Opioid Shipment Data
def transform_shipment_data():
    opioid_df = pd.read_csv('../00_source/opioid_chunked_source.zip')
    opioid_df['Year'] = [str(x)[-4:] for x in opioid_df['TRANSACTION_DATE'].tolist()]
    opioid_df['Year'] = opioid_df['Year'].astype(int)
    opioid_df = opioid_df.drop(['TRANSACTION_DATE','Unnamed: 0','BUYER_CITY'], axis =1)
    opioid_df ['DRUG_TOTAL'] = opioid_df.MME_Conversion_Factor * opioid_df.Weight_gram * 1000

    opioid_df.columns = ['STATE', 'COUNTY', 'DRUG_NAME', 'MME_CONVERSION_FACTOR', 'WEIGHT_GRAM', 'YEAR', 'MME_SHIPPED']
    opioid_df = opioid_df[['YEAR', 'STATE', 'COUNTY', 'MME_SHIPPED']]
    opioid_df = opioid_df.groupby(['YEAR', 'STATE', 'COUNTY'], as_index = False).sum()

    opioid_df.columns = ['YEAR', 'State_Abrv', 'COUNTY_Abrv', 'MME_SHIPPED']

    opioid_df.loc[opioid_df['State_Abrv'] == 'FL', 'STATE'] = 'Florida'
    opioid_df.loc[opioid_df['State_Abrv'] == 'AL', 'STATE'] = 'Alabama'
    opioid_df.loc[opioid_df['State_Abrv'] == 'SC', 'STATE'] = 'South Carolina'
    opioid_df.loc[opioid_df['State_Abrv'] == 'GA', 'STATE'] = 'Georgia'
    opioid_df.loc[opioid_df['State_Abrv'] == 'TX', 'STATE'] = 'Texas'
    opioid_df.loc[opioid_df['State_Abrv'] == 'AZ', 'STATE'] = 'Arizona'
    opioid_df.loc[opioid_df['State_Abrv'] == 'CA', 'STATE'] = 'California'
    opioid_df.loc[opioid_df['State_Abrv'] == 'OK', 'STATE'] = 'Oklahoma'
    opioid_df.loc[opioid_df['State_Abrv'] == 'WA', 'STATE'] = 'Washington'
    opioid_df.loc[opioid_df['State_Abrv'] == 'NC', 'STATE'] = 'North Carolina'
    opioid_df.loc[opioid_df['State_Abrv'] == 'UT', 'STATE'] = 'Utah'
    opioid_df.loc[opioid_df['State_Abrv'] == 'CO', 'STATE'] = 'Colorado'

    treatment_list = ['FL', 'WA', 'TX']
    opioid_df['treatment_status'] = 'Control'
    opioid_df.loc[opioid_df['State_Abrv'].isin(treatment_list), 'treatment_status'] = 'Treatment'
    opioid_df['treatment_status'] = pd.Categorical(opioid_df['treatment_status'])
    opioid_df.to_csv('../20_intermediate_files/opioid_shipment_extract.csv')

#transform_shipment_data()

# ### Subset to Florida and its Reference States (for now)
opioid_df = pd.read_csv('../20_intermediate_files/opioid_shipment_extract.csv')
opioid_df = opioid_df.drop('Unnamed: 0', axis=1)

opioid_df = opioid_df[opioid_df['State_Abrv'].isin(['FL', 'AL', 'SC', 'GA','WA','NC','UT','CO','TX','AZ','CA','OK'])]

opioid_df.State_Abrv.value_counts()


# ### Merge Opioid Shipment data with Population data
merge_list = ['YEAR', 'STATE', 'COUNTY_Abrv']
op_pop = pd.merge(opioid_df, pop_df, how='inner', indicator = True, on=merge_list)

op_pop = op_pop.rename(columns={'MME_SHIPPED':'MME_Total'})
op_pop['MME_SHIPPED'] = op_pop['MME_Total'] / op_pop['TOTAL_POP']
op_pop.head()


# # Create csv files with transformed data
mor_pop.to_csv('../20_intermediate_files/mortality_transformed_final.csv')
op_pop.to_csv('../20_intermediate_files/opioid_transformed_final.csv')