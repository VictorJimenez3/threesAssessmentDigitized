# 3S Spatial Awareness Assessment

## Short Description
The 3S Spatial Awareness Assessment is a privacy-first cognitive testing platform designed to digitize and enhance spatial neglect assessments. Leveraging secure encryption and adaptive machine learning models, it enables continuous, real-world cognitive monitoring without compromising user data privacy. Inspired by validated clinical research, the system provides a scalable, secure foundation for future cognitive health applications.

## Features
- **Privacy-Preserving Data Collection**: End-to-end encrypted cognitive test results.
- **Adaptive AI Model**: Continuously improves accuracy as more tests are performed.
- **Secure Real-Time Updates**: User data remains protected while enhancing model performance.
- **Web-Based Platform**: Lightweight, accessible system for both practitioners and researchers.

## Tech Stack
- **Python**: Backend development, data processing.
- **Flask**: Server-side web application framework.
- **PyTorch**: Machine learning model development.
- **TenSEAL**: Encrypted computations using CKKS scheme.
- **HTML/CSS/JavaScript/Jinja**: Frontend interface.

## Challenges and Solutions
- **Encrypted Model Training**: Architected a workflow that allows efficient model updates while data remains encrypted, solving major performance and scalability hurdles.
- **CKKS Computation Overhead**: Tuned system resources and workflows to support CKKS homomorphic encryption without major latency penalties.
- **End-to-End Security**: Designed middleware that guarantees encryption persistence across all data handling stages.

## Key Outcomes / Metrics
- **Award Winner**: Earned Best Security Hack, sponsored by Nord Security, at HackRU Fall 2024.
- **Functional End-to-End Prototype**: Achieved encrypted cognitive assessment and adaptive model learning on real data inputs.
- **Security-First Design**: Successfully demonstrated privacy-preserving machine learning workflows.

## How to Use
The 3S Spatial Awareness Assessment is a research prototype. To run it:

1. Clone the repository and install dependencies:
   
       git clone https://github.com/Binimal101/3sSpacialAwarenessAssessment.git
       cd 3sSpacialAwarenessAssessment
       pip install -r requirements.txt

2. Launch the server:

       python app.py

3. Access the assessment tool through your browser at `http://localhost:5000`.

*Note: For demonstration and academic use only. Production deployment would require formal clinical review.*

## Links
- [GitHub Repository](https://github.com/VictorJimenez3/threesAssessmentDigitized/)
- [Devpost Project Page](https://devpost.com/software/3s-spacial-awareness-assessment)

## Copyright
This project digitizes and extends the 3S Spreadsheet Test from:

Chen, P., & Toglia, J. (2022). *The 3S Spreadsheet Test version 2 for assessing egocentric viewer-centered and allocentric stimulus-centered spatial neglect.* Applied Neuropsychology: Adult, 29(6), 1369–1379.  
[https://doi.org/10.1080/23279095.2021.1878462](https://doi.org/10.1080/23279095.2021.1878462)

All rights and references to the original 3S-v2 Test belong to the authors.
