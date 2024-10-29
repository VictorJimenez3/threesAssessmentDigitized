"""
Programmed by Matthew Tujague
"""

import firebase_admin
from firebase_admin import credentials, firestore
import json
import datetime
import os
from dotenv import load_dotenv

from pprint import pprint

from model import predictImpairment, trainModel


# Load environment variables from .env file if needed
load_dotenv()

# Path to Firebase service account key
firebase_key_path = os.environ.get("FIREBASE_KEY_PATH")
# Initialize Firebase
cred = credentials.Certificate(firebase_key_path)
firebase_admin.initialize_app(cred)
db = firestore.client()

def encodeDataForTransmission(data):
    """Encodes data into JSON format for Firestore storage."""
    return json.dumps(data)

def decodeDataForTraining(data):
    """Decodes JSON data retrieved from Firestore."""
    return json.loads(data)

def addTestToFirebase(test):
    """
    Adds a test object with a timestamp to Firestore.
    """
    try:
        # Prepare the test data with a timestamp
        test_data = {
            "test": test,
            "timestamp": int(datetime.datetime.utcnow().timestamp())
        }

        # Add data to Firestore
        db.collection("tests").add(test_data)
        print("Test data added to Firebase Firestore.")

    except Exception as e:
        print("Error adding test data to Firebase:", e)

def retrieveAllTests():
    """
    Retrieve all test objects stored in the Firestore database.
    """
    all_tests = []
    try:
        # Retrieve all documents in the "tests" collection
        docs = db.collection("tests").stream()

        for doc in docs:
            # Decode and append each test entry
            test_data = doc.to_dict()
            all_tests.append(test_data)

        return all_tests

    except Exception as e:
        print("Error retrieving test data from Firebase:", e)
        return all_tests  # Return whatever was collected, even if incomplete

def formatTestsToModel(tests):
    pprint(tests)

    times, correctResponses, pageCenteredOmissions, stringCenteredOmissions, ages, labels = [], [], [], [], [], []
    for test in tests:
        times.append(test["test"]["time"])
        correctResponses.append(test["test"]["correctResponses"])
        pageCenteredOmissions.append(test["test"]["pageCenteredOmissions"])
        stringCenteredOmissions.append(test["test"]["stringCenteredOmissions"])
        ages.append(test["test"]["age"])
        labels.append(test["test"]["isImpaired"])

    values = [times, correctResponses, pageCenteredOmissions, stringCenteredOmissions, ages]
    
    return values, labels

def trainModelToNewData(newTest: dict) -> bool:
    """
    returns bool to represent whether newTest was detected to have an impairment or not
    (True) : Impairment, (False) : No Impairment
    """
    isImpaired = predictImpairment(newTest)
    oldData, labels = formatTestsToModel(retrieveAllTests())
    
    values = ("time", "correctResponses", "pageCenteredOmissions", "stringCenteredOmissions", "age")
    
    for i in range(len(oldData)):
        oldData[i].append(newTest[values[i]])
    labels.append(isImpaired)

    trainModel(oldData, labels)
    addTestToFirebase(newTest)

    return isImpaired
