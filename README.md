# Replication Project: Source Code Properties of Defective Infrastructure as Code Scripts

## Overview

This project is a replication study aimed to validate the empirical findings of the original research paper, "Source Code Properties of Defective Infrastructure as Code Scripts" by Akhond Rahman and Laurie Williams. Our goal is to corroborate the original study's evidence, which identifies specific code properties correlated with defects in Infrastructure as Code (IaC) scripts.

## Installation

To replicate this study, you'll need to install the required packages, software, or data sets. Below are the steps for different parts of the project.

### General Setup

1. Clone this repository to your local machine.

   ```bash
   git clone https://github.com/keshavDooleea/LOG6307E_Replication_Project
   ```

2. Create a `.env` file on the root and add your GitHub API token as follows.
   ```bash
   GITHUB_TOKEN=abcd..
   ```

### For Mining Repositories

1. Navigate to the `Dataset_Mining` directory.

   ```bash
   cd Dataset_Mining/
   ```

2. Create a virtual environment.

   ```
   python -m venv venv
   ```

3. Activate the virtual environment.

   ````bash
   source venv/bin/activate  # On macOS and Linux
   .\venv\Scripts\Activate   # On Windows    ```

   ````

4. Install the required packages from `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

5. To run the section 3.1.1. Repository Collection and 3.1.2. Commit Messaging Processing:

   ```bash
   cd dataset_mining\src
   python main.py
   ```

6. To run the Mann-Whitney U test and Cliff's Delta:

   ```bash
      cd dataset_mining\src\steps\tests
      python main.py
   ```

### For Building Prediction Model

1. Navigate to the `Prediction_Model` directory.

   ```bash
   cd Prediction_Model/
   ```

2. Navigate further into the `src` folder.

   ```bash
   cd src/
   ```

3. Create a virtual environment.

   ```
   python -m venv venv
   ```

4. Activate the virtual environment.

   ```bash
   source venv/bin/activate  # On macOS and Linux
   .\venv\Scripts\Activate   # On Windows
   ```

5. Install the required packages from `requirements.txt`.

   ```bash
   pip install -r requirements.txt
   ```

6. Run the main script to build the prediction model.
   ```bash
   python main.py
   ```

Follow these steps to set up and run the prediction model part of the project.

## Data Mining

We collected data from repositories of organizations such as Mirantis, OpenStack, and Wikimedia. The data mining process involved applying specific filtering criteria to isolate repositories containing potentially defective IaC scripts.

## Building prediction model

1. **Data Preprocessing**: Processed commit messages and isolated those mentioning at least one potentially problematic IaC script.
2. **Principal Component Analysis (PCA)**: Used for feature selection before model training.
3. **Model Training**: Applied statistical learning algorithms to build predictive models.
4. **Validation**: Utilized 10x10-fold cross-validation to assess the models' predictive accuracy.
