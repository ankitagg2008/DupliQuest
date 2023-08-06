![Duplicate Question Pairs](https://github.com/shengjie94/AIM5011-Group4/blob/main/logo/duplicatequestionpairs.png)
This project is an end-to-end web-based work product primarily designed to determine whether two given problems are duplicated. The output will be displayed regardless of whether the given problem set is repeated or not.
## Motivation
Online platforms like Quora, Yahoo, Stack Overflow and Grapple with a significant issue i.e.,  questions with identical intents spread across separate pages. For example, consider these queries: "Most populous US state?" and "Which state has the most people in the United States?" Such duplication hampers efficient knowledge-sharing.

The Duplicate Question Pairs provides a concise and easy-to-use web page. Users can input questions to determine if the problem is repeated. For the future, we will try to add additional features, which may include intention classification, emotion analysis, and automatic summarization.
## Main models
### Sentence Bert Model
This repository contains the implementation of a Sentence BERT (SBERT) model utilizing a Siamese Network architecture, primarily for the task of sentence or question pair similarity prediction.
#### Overview
The Siamese Sentence BERT model, as implemented here, is a variation of the well-known BERT (Bidirectional Encoder Representations from Transformers) model, which is designed specifically for sentence-pair tasks. In this model, each sentence in a pair passes through the same BERT model (hence the term 'Siamese'), producing sentence embeddings. The model then calculates the distance between these embeddings to decide whether the two sentences are semantically similar.
#### Features
- **Siamese Network Architecture:** We exploit a Siamese network architecture, where two different inputs pass through the same sub-network. The outputs of these subnetworks are then compared to predict whether the inputs are similar.
- **BERT:** We leverage the BERT model to generate sentence embeddings, leveraging its powerful ability to understand the context of words in a sentence, enabling it to efficiently perform natural language processing (NLP) tasks.
- **Custom dataset processing:** We include a custom DataLoader that preprocesses and organizes the dataset into a format suitable for our Siamese Sentence BERT model.
- **Performance Monitoring:** The code also includes functions for computing key performance metrics such as accuracy, F1 score, and the loss function (Binary Cross Entropy with Logits Loss), giving a comprehensive evaluation of the model's performance.
- **Learning Rate Scheduling:** We've implemented a learning rate scheduler, ‘ReduceLROnPlateau’, which adjusts the learning rate based on the model's performance, ensuring an efficient training process.
### Distilbert Model
The project also implements a text classification model using DistilBert, a lightweight and efficient variant of the BERT model developed by Hugging Face.
#### Overview
DistilBert is a transformer-based model that utilizes the concept of model distillation. It is trained to mimic a larger model (in our case, BERT), which allows DistilBert to achieve high performance while being more computationally efficient.
#### Features
- **DistilBert Architecture:** We leverage the DistilBert model, which is a refined version of the BERT model. DistilBert is smaller, faster, cheaper and lighter, yet still maintains a high level of performance. It is specifically designed for tasks like ours, where we use Transformer encoders instead of decoders.
- **Pairwise Question Analysis:** The model is designed to handle pairs of questions, assessing the similarity between the two to determine if they're duplicates. This is similar to a Siamese Network Architecture, where two distinct inputs pass through identical subnetworks.
- **Powerful Tokenization:** We leverage an efficient tool, DistilBertTokenizer, that breaks down input text into tokens that can then be processed by our DistilBert model. This tokenizer is specifically designed to work with DistilBert and manages tasks such as adding special tokens and handling different sequence lengths.
- **Custom Dataset Processing:** This same model also includes a custom class called QuoraDataset that preprocesses the dataset and organizes it into a format suitable for our DistilBert model. This involves using a tokenizer to convert text into input IDs and attention masks that the model can process.
- **Learning Rate Scheduling:** We also use the ReduceLROnPlateau learning rate scheduler to help optimize our training process.
## Quick Get Start
### Dataset Description
This dataset is designed for the task of predicting whether pairs of questions have the same meaning. Comprising a mix of genuine questions from Quora and computer-generated pairs added by Kaggle as an anti-cheating measure, the dataset is labeled by human experts. While these labels represent a generally accepted consensus, they are acknowledged to be 'informed' rather than absolute truths, and may contain inaccuracies. You can find it in the [Kaggle competition](https://www.kaggle.com/competitions/quora-question-pairs/data). At the same time, you can also view and download content in our [ques pairs extra](https://github.com/shengjie94/AIM5011-Group4/blob/main/ques/ques_pairs_extra.csv).
#### Here is some Details:
- **Objective:** Predict if question pairs have the same meaning.
- **Source:** Genuine examples from Quora, supplemented with artificial pairs by Kaggle.
- **Size:** 523.24 MB
- **Type:** Available in zip and csv formats.
- **Files:** 4 files
- **Fields:**
  - `id`: ID of a training set question pair
  - `qid1`, `qid2`: Unique IDs of each question (train.csv only)
  - `question1`, `question2`: Full text of each question
  - `is_duplicate`: Target variable, 1 if questions have the same meaning, 0 otherwise.
### Installation instructions: 
- **Install Python environment:** Ensure that your computer has Python installed. If not installed, you can download and install it on the [Python official website](https://www.python.org/downloads/).
- **Install necessary dependencies:** In the project root directory, you can use the following command to install the necessary dependency libraries.
  - **Machine Learning:** The dependencies you may need for [machine learning files](https://github.com/shengjie94/AIM5011-Group4/blob/main/Part_1_Machine_Learning_Models.ipynb)
    ```
    pip install pandas matplotlib seaborn beautifulsoup4 nltk wordcloud distance xgboost scikit-learn tabulate
    ```
  - **Deep Learning:** The dependencies you may need for [Deep learning files](https://github.com/shengjie94/AIM5011-Group4/blob/main/Part_2_Deep_Learning_Models_using_Transformers.ipynb)
    ```
    pip install torch transformers gradio
    ```
### Usage
#### Machine Learning Models
- **Environmental preparation:**
  - Ensure that Python and related libraries (pandas, scikit learn, numpy, matplotlib) are installed.
  - Download training and testing data, such as CSV files.
- **Run Code:**
  - Before running the code, it is necessary to ensure that the [data file](https://github.com/shengjie94/AIM5011-Group4/blob/main/ques/ques_pairs_extra.csv) is ready and placed in the correct Working directory. Ensure that the data file contains columns 'question1' and 'question2', as well as' is_ Duplicate' column as label.
  - Run the code in the Python environment and ensure that all required dependency libraries (such as 'numpy', 'pandas', 'matplotlib', 'seaborn', 'bs4', 'wordcloud', 'nltk', etc.) are installed. The steps to run the code include data cleaning, feature extraction, model training, etc.
  - Several different classifiers are used in the code (such as Random Forest, XGBoost, Logistic Regression, etc.), which you can use in the train_ The evaluation function shows the training and evaluation process of each classifier. The code will divide the data into training and testing sets, then fit the model on the training set, make predictions on the testing set, and calculate the accuracy, accuracy, recall, and F1 score of the model. The code also outputs a Confusion matrix to view the prediction effect of the classifier.
#### Machine Learning Models
- **Environmental preparation:**
  - Ensure that the required dependency libraries, including 'torch', 'transformers', and 'graphics', are installed in your Python environment.
- **Run Code:**
  - In the code, we first downloaded the pre trained DistilBERT model and made minor adjustments. After completing the training of the model, save it as distilbert50_ v3.pth. You can view the example in [distilbert50_v3](https://github.com/shengjie94/AIM5011-Group4/blob/main/distilbert50_v3/distilbert50_v3.pth).
  - We have created a simple web interface through Graph for using trained models for problem repetition determination. You can input two questions through this interface and obtain the predicted results of the model, that is, whether they are duplicate questions.
## Report Issues
Report bugs or feature requests using the [Duplicate problem recognizer issue tracker](https://github.com/shengjie94/AIM5011-Group4/issues).
At the same time, we also have a reporting function on the webpage. If there is a problem during use, click the 'Flag' button to mark it.
