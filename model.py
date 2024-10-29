"""
AI/ML: Julian Vilfort
HM Encryption: Matthew Tujague
"""

#!/usr/bin/env python
# coding: utf-8

# ### Import data

# In[100]:


from dataCreation import generate_data
import tenseal as ts
import pandas as pd
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


# ### Create test and train data

# In[101]:


data = generate_data(100)
x_train = np.array([
                        data['time'], 
                        data['correct_response'], 
                        data['page_centered_omission_score'], 
                        data['string_centered_omission_score'],
                        data['age']
                    ])
y_train = data['isImpaired']
print(x_train.shape, y_train.reshape(-1,1).shape)


# In[102]:


def get_context():
    poly_modulus_degree = 8192 * 2
    coeff_mod_bit_sizes = [60, 50, 50, 50, 50, 60]
    context = ts.context(
        ts.SCHEME_TYPE.CKKS, poly_modulus_degree, -1, coeff_mod_bit_sizes
    )
    context.global_scale = 2 ** 40
    context.generate_galois_keys()
    return context

def encrypt(vector):
    # Initialize CKKS context
    context = get_context()

    # Encrypt data vectors
    encrypted_data_vectors = [
        ts.ckks_vector(context, data_vector.tolist()) for data_vector in vector
    ]
    return encrypted_data_vectors

def encrypted_logistic_regression_train(data_vectors, labels_vector, num_epochs=10, reinit_interval=5):
    """
    Trains a logistic regression model on CKKS encrypted data, simulating bootstrapping by
    reinitializing the encrypted vectors before noise limit is reached.

    Parameters:
    - data_vectors: List of feature vectors (e.g., [[357, 112, 2, 5, 80], ...])
    - labels_vector: List of labels (0 or 1)
    - num_epochs: Number of training epochs
    - reinit_interval: Number of epochs after which to refresh encryption
    """

    # Get encryption context
    context = get_context()


    # Convert data to NumPy arrays
    data_vectors = data_vectors.reshape(100,5)
    labels_vector = labels_vector.reshape(-1, 1)
    num_samples, num_features = data_vectors.shape
    
    # Check that data and labels have compatible shapes
    assert len(data_vectors) == len(labels_vector), "Data and labels must have the same length."
    

    # Encrypt data vectors
    encrypted_data_vectors = encrypt(data_vectors)
    encrypted_label_vectors = encrypt(labels_vector)

    # Initialize logistic regression model
    model = nn.Linear(num_features, 1)
    optimizer = optim.SGD(model.parameters(), lr=0.0001)

    # Simulate bootstrapping by tracking operations
    operations_count = 0
    max_operations = reinit_interval

    # Training loop
    for epoch in range(num_epochs):
        print(f"Epoch {epoch + 1}/{num_epochs}")

        total_loss = 0.0

        for i in range(num_samples):
            # Encrypt the model weights
            weights = model.weight.data.numpy()
            bias = model.bias.data.numpy()
            encrypted_weights = ts.ckks_vector(context, weights.flatten().tolist())
            encrypted_bias = ts.ckks_vector(context, bias.tolist())

            # Encrypted forward pass
            enc_data = encrypted_data_vectors[i]
            enc_linear = enc_data.dot(encrypted_weights) + encrypted_bias

            # Sigmoid approximation: sigmoid(x) ≈ 0.5 + 0.197 x - 0.004 x^3
            x = enc_linear
            x_cube = x * x * x
            enc_pred = x * 0.197 + x_cube * (-0.004) + 0.5

            # Compute encrypted loss: (prediction - label)^2
            label = labels_vector[i][0]
            enc_label = ts.ckks_vector(context, [label])
            enc_error = enc_pred - enc_label
            enc_loss = enc_error * enc_error

            # Decrypt loss for logging
            loss = enc_loss.decrypt()[0]
            total_loss += loss

            # Decrypt prediction for gradient computation
            pred = enc_pred.decrypt()[0]
            error = pred - label

            # Compute gradient (plaintext)
            gradient = error * data_vectors[i]
            bias_grad = error

            # Update model weights
            with torch.no_grad():
                model.weight.data -= optimizer.param_groups[0]['lr'] * torch.tensor(gradient).reshape_as(model.weight.data)
                model.bias.data -= optimizer.param_groups[0]['lr'] * torch.tensor(bias_grad)

            operations_count += 1

            # Simulate bootstrapping if operations exceed max_operations
            if operations_count >= max_operations:
                print("Refreshing encrypted data vectors...")
                encrypted_data_vectors = [
                    ts.ckks_vector(context, vec.decrypt()) for vec in encrypted_data_vectors
                ]
                operations_count = 0  # Reset operation count

        avg_loss = total_loss / num_samples
        print(f"Average loss: {avg_loss}")

    # Return the trained model
    return model


# In[103]:


encrypted_logistic_regression_train(x_train, y_train, reinit_interval=1)


# In[ ]:
