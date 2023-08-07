![Duplicate Question Pairs](https://github.com/shengjie94/AIM5011-Group4/blob/main/logo/duplicatequestionpairs.png)
This project is an end-to-end web-based work product primarily designed to determine whether two given problems are duplicated. The output will be displayed regardless of whether the given problem set is repeated or not.
## Motivation
Online platforms like Quora, Yahoo, Stack Overflow and Grapple with a significant issue i.e.,  questions with identical intents spread across separate pages. For example, consider these queries: "Most populous US state?" and "Which state has the most people in the United States?" Such duplication hampers efficient knowledge-sharing.

The Duplicate Question Pairs provides a concise and easy-to-use web page. Users can input questions to determine if the problem is repeated. For the future, we will try to add additional features, which may include intention classification, emotion analysis, and automatic summarization.
## Models
This repository centers around the application and evaluation of various BERT-based models, all aimed at detecting similarity and possible duplication in pairs of questions. Of the different models implemented and examined, DistilBert emerges as the most effective choice for this specific task.
### Sentence Bert Model
In the domain of sentence pair tasks, the Sentence BERT (SBERT) model is one of the effective methods we have studied. It utilizes Siamese network architecture, which is a powerful strategy for comparing different entities.
#### Overview
SBERT is a variation of the renowned BERT (Bidirectional Encoder Representations from Transformers) model. Here, each sentence of a pair passes through the same BERT model, which is why it's dubbed a 'Siamese' architecture. This process generates sentence embeddings. The model then computes the distance between these embeddings, utilizing this measure to gauge whether the two sentences are semantically similar or not.
#### Features
- **Connected network architecture:** This architecture allows two different inputs to pass through the same subnet. Then compare the outputs to predict if the inputs are similar.
- **BERT:** We use BERT to generate sentence embeddings. It is good at understanding the context of words in sentences, making it very suitable for Natural language processing tasks.
- **Custom Dataset Processing:** We have included a custom DataLoader that can preprocess datasets and arrange them into a format suitable for our Sentence BERT model.
- **Performance monitoring:** the code also contains functions for calculating key performance indicators, such as accuracy, F1 score and Loss function (binary Cross entropy with Logits loss). These provide a comprehensive evaluation of model performance.
- **Learning rate scheduling:** We have implemented a Learning rate scheduler "ReduceLROnPlateau". It adjusts the Learning rate and optimizes the training process according to the performance of the model.

Although the sentence BERT model provides excellent features and functionality, DistilBert (a refined and more efficient variant of BERT) has been proven to be our best choice for detecting specific tasks related to repetitive problems. More information about the DistilBert model and its implementation can be found in the appropriate section of this repository.
### Distilbert Model
The main focus of this repository is the implementation and optimization of the DistilBert model for detecting duplicate problem pairs of tasks. DistilBert is a lightweight and computationally efficient variant of the BERT model developed by Hugging Face. This model demonstrates the potential of model distillation, which involves training smaller models to mimic the performance of larger models, while maintaining high performance and being faster and more cost-effective.
#### Overview
DistilBert uses a converter based model architecture specifically designed to handle problem pairs. It evaluates the similarity between two problems to determine if they are duplicated, similar to the Siamese network architecture.
#### Features
- **DistilBert architecture:** DistilBert is a condensed version of the BERT model. Although smaller, faster, cheaper, and lighter, it can still maintain a high level of performance.
- **Paired problem analysis:** This model aims to handle paired problems and evaluate their similarity to identify potential duplicates.
- **Powerful tokenization:** We utilize the DistilBertTokenizer, an efficient tool that decomposes input text into tokens and is then processed by our DistilBert model. This word breaker is specifically designed for use with DistilBert to perform tasks such as adding special tags and handling different sequence lengths.
- **Custom dataset processing:** We also include a custom class called QuoraDataset. This class preprocesses the dataset and organizes it into a format that the DistilBert model can process. This involves using a word breaker to convert text into input IDs and attention masks.
- **Learning rate scheduling:** In order to optimize our training process, we use the "ReduceLROnPlateau" Learning rate scheduler, which adjusts the Learning rate according to the performance of the model.

By comprehensively evaluating different BERT based models and their performance in identifying repetitive problems on tasks, DistilBert has become our preferred choice due to its impressive balance between performance and efficiency.
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
