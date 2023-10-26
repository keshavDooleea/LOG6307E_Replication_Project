# Replication Project: Source Code Properties of Defective Infrastructure as Code Scripts

## Overview

This project is a replication study aimed to validate the empirical findings of the original research paper, "Source Code Properties of Defective Infrastructure as Code Scripts" by Akhond Rahman and Laurie Williams. Our goal is to corroborate the original study's evidence, which identifies specific code properties correlated with defects in Infrastructure as Code (IaC) scripts.


## Installation

Instructions to install any required packages, software, or data sets to replicate this study.

1. Clone this repository to your local machine.

For mining repositories section
2.1 cd Dataset_Mining\

For building prediction model
2.2 cd Prediction_Model\

## Data Mining

We collected data from repositories of organizations such as Mirantis, OpenStack, and Wikimedia. The data mining process involved applying specific filtering criteria to isolate repositories containing potentially defective IaC scripts.

## Building prediction model

1. **Data Preprocessing**: Processed commit messages and isolated those mentioning at least one potentially problematic IaC script.
2. **Principal Component Analysis (PCA)**: Used for feature selection before model training.
3. **Model Training**: Applied statistical learning algorithms to build predictive models.
4. **Validation**: Utilized 10x10-fold cross-validation to assess the models' predictive accuracy.


