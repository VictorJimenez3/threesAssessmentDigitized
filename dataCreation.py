"""
Programmed by Julian Vilfort
"""

#!/usr/bin/env python
# coding: utf-8

# In[1045]:


import pandas as pd
import numpy as np

# ## Mean and Standard error data by age range for model parameters
# 
# 

# In[ ]:


# Function to calculate impaired means based on percentage increase from healthy mean to cutoff
def calculate_impaired_mean(healthy_mean, cutoff):
    percent_increase = (cutoff - healthy_mean) / healthy_mean
    return healthy_mean * (1 + percent_increase)

# Healthy and impaired data parameters for each age group
age_groups = {
    'middle_age': {
        'healthy': {
            'time': {'mean': 181.4, 'sd': 50.6, 'rlo': 94, 'rhi': 336},
            'correct_response': {'mean': 116.9, 'sd': 3.2, 'rlo': 107, 'rhi': 120},
            'page_centered_omission_score': {'low': -3, 'high': 3, 'mean': -0.1, 'sd': 1.6, 'rlo': -5, 'rhi': 4},
            'string_centered_omission_score': {'low': -3, 'high': 5, 'mean': 0.4, 'sd': 2.4, 'rlo': -9, 'rhi': 7}
        },
        'cutoff': {
            'time': 293,
            'correct_response': 110
        }
    },
    'elderly_age': {
        'healthy': {
            'time': {'mean': 198.0, 'sd': 48.0, 'rlo': 123, 'rhi': 325},
            'correct_response': {'mean': 116.2, 'sd': 3.0, 'rlo': 108, 'rhi': 120},
            'page_centered_omission_score': {'low': -3, 'high': 3, 'mean': -0.1, 'sd': 1.6, 'rlo': -4, 'rhi': 4},
            'string_centered_omission_score': {'low': -3, 'high': 5,'mean': 0.7, 'sd': 2.6, 'rlo': -6, 'rhi': 8}
        },
        'cutoff': {
            'time': 289,
            'correct_response': 110
        }
    },
    'advanced_age': {
        'healthy': {
            'time': {'mean': 243.3, 'sd': 85.3, 'rlo': 129, 'rhi': 456},
            'correct_response': {'mean': 114.1, 'sd': 4.8, 'rlo': 103, 'rhi': 120},
            'page_centered_omission_score': {'low': -3, 'high': 3, 'mean': 0.3, 'sd': 3.4, 'rlo': -9, 'rhi': 12},
            'string_centered_omission_score': {'low': -3, 'high': 5, 'mean': 0.6, 'sd': 3.1, 'rlo': -7, 'rhi': 9}
        },
        'cutoff': {
            'time': 411,
            'correct_response': 105
        }
    }
}

# Generate impaired data by adjusting healthy means based on cutoff values
for age_group, data in age_groups.items():
    healthy = data['healthy']
    cutoff = data['cutoff']
    
    impaired = {
        'time': {'mean': calculate_impaired_mean(healthy['time']['mean'], cutoff['time']), 'sd': healthy['time']['sd'] * 1.2, 'rlo': 60, 'rhi': 600},
        'correct_response': {'mean': calculate_impaired_mean(healthy['correct_response']['mean'], cutoff['correct_response']), 'sd': healthy['correct_response']['sd'] * 1.1, 'rlo': 0, 'rhi': 120},
        'page_centered_omission_score': {'low': -3, 'high': 3, 'sd': healthy['page_centered_omission_score']['sd'] * 1.2, 'rlo': -9, 'rhi': 12},
        'string_centered_omission_score': {'low': -3, 'high': 5, 'sd': healthy['string_centered_omission_score']['sd'] * 1.2, 'rlo': -9, 'rhi':9}
    }
    
    age_groups[age_group]['impaired'] = impaired  # Add impaired data to each age group

# Print to verify structure
age_groups


# ## Define data creation helper functions

# In[1047]:


# Function to generate truncated normal distribution within bounds
def generate_truncated_normal(mean, sd, lower, upper, num_samples):
    samples = []
    while len(samples) < num_samples:
        batch = np.random.normal(mean, sd, num_samples)
        filtered_batch = batch[(batch >= lower) & (batch <= upper)]
        samples.extend(filtered_batch)
    return np.array(samples[:num_samples]).astype(int)

# Bimodal distribution function for omissions
def generate_bimodal_omissions(low_mean, high_mean, sd, num_samples, low_bound, high_bound):
    half_samples = 1 if num_samples == 1 else num_samples // 2
    low_cluster = generate_truncated_normal(low_mean, sd, low_bound, high_bound, half_samples)
    high_cluster = generate_truncated_normal(high_mean, sd, low_bound, high_bound, half_samples)
    bimodal_distro = np.concatenate([low_cluster, high_cluster])
    np.random.shuffle(bimodal_distro)
    return bimodal_distro if num_samples > 1 else np.array([np.random.choice(bimodal_distro)])

# Consolidated data generation function
def generate_data_by_ad(age_group: str, health_state: str, num_samples: int):
    data = {}
    if age_group not in ['middle_age', 'elderly_age', 'advanced_age']:
        raise ValueError(f"{age_group} must be 'middle_age', 'elderly_age', or 'advanced_age'")
    if health_state not in ['healthy', 'impaired']:
        raise ValueError(f"{health_state} must be 'healthy' or 'impaired'")

    for category, params in age_groups[age_group][health_state].items():
        if category in ["page_centered_omission_score", "string_centered_omission_score"]:
            data[category] = generate_bimodal_omissions(params['low'], params['high'], params['sd'], num_samples, params['rlo'], params['rhi'])
        else:
            data[category] = generate_truncated_normal(params['mean'], params['sd'], params['rlo'], params['rhi'], num_samples)
    
    if age_group == 'middle_age':
        data['age'] = np.random.randint(40, 60, num_samples)
    elif age_group == 'elderly_age': 
        data['age'] = np.random.randint(60, 80, num_samples)
    else:
        data['age'] = np.random.randint(80, 100, num_samples)


    if health_state == 'healthy':
        data['isImpaired'] = np.zeros(num_samples).astype(int)
    else:
        data['isImpaired'] = np.ones(num_samples).astype(int)
    
    return data


# ## Compare relevant statistics between healthy and impaired data

# In[ ]:


# In[ ]:


# Generate a dataset with both healthy and impaired samples
def generate_data(num_samples: int):
    total_data = {'age': [], 'time': [], 'correct_response': [], 'page_centered_omission_score': [], 'string_centered_omission_score': [], 'isImpaired': []}
    for i in range(num_samples):
        age_group = np.random.choice(['middle_age', 'elderly_age', 'advanced_age'])
        health_status = np.random.choice(['healthy', 'impaired'])
        current_data = generate_data_by_ad(age_group, health_status, 1)
        
        # Aggregate data, assuming consistent structure in `current_data`
        for key in total_data.keys():
            total_data[key].append(current_data[key][0])  # Append the first element since it's a single-sample
    
    # Convert lists to arrays for consistent access
    for key in total_data:
        total_data[key] = np.array(total_data[key])
    
    # Shuffle the data by applying a random permutation
    permutation = np.random.permutation(num_samples)
    for key in total_data:
        total_data[key] = total_data[key][permutation]
    
    return total_data


# In[ ]:


def jawn():
    print('yuh')
