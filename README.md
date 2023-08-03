![Duplicate Question Pairs](https://github.com/shengjie94/AIM5011-Group4/blob/main/logo/duplicatequestionpairs.png)
This project is an end-to-end web-based work product primarily designed to determine whether two given problems are duplicated. The output will be displayed regardless of whether the given problem set is repeated or not.
## Motivation
Considering that some companies wish to retain text (such as discussion forums and query threads) for ease of management and subsequent user queries. We design a Duplicate problem recognizer to help filter out duplicate problems.

The Duplicate problem recorder provides a concise and easy-to-use web page. Users can input questions to determine if the problem is repeated. For the future, we will try to add additional features, which may include intention classification, emotion analysis, and automatic summarization.
## Quick Get Start
### Dataset Description
This dataset is designed for the task of predicting whether pairs of questions have the same meaning. Comprising a mix of genuine questions from Quora and computer-generated pairs added by Kaggle as an anti-cheating measure, the dataset is labeled by human experts. While these labels represent a generally accepted consensus, they are acknowledged to be 'informed' rather than absolute truths, and may contain inaccuracies. You can find it in the [Kaggle competition](https://www.kaggle.com/competitions/quora-question-pairs/data). At the same time, you can also view and download content in our [ques pairs extra](https://github.com/shengjie94/AIM5011-Group4/blob/main/ques/ques_pairs_extra.csv).
#### Here is some Details:
- Objective: Predict if question pairs have the same meaning.
- Source: Genuine examples from Quora, supplemented with artificial pairs by Kaggle.
- Size: 523.24 MB
- Type: Available in zip and csv formats.
- Files: 4 files
- Fields:
  - `id`: ID of a training set question pair
  - `qid1`, `qid2`: Unique IDs of each question (train.csv only)
  - `question1`, `question2`: Full text of each question
  - `is_duplicate`: Target variable, 1 if questions have the same meaning, 0 otherwise.
### Installation instructions: 
- Install Python environment: Ensure that your computer has Python installed. If not installed, you can download and install it on the [Python official website](https://www.python.org/downloads/).
- Install necessary dependencies: In the project root directory, you can use the following command to install the necessary dependency libraries.
  - `Machine Learning`: The dependencies you may need for [machine learning files](https://github.com/shengjie94/AIM5011-Group4/blob/main/Part_1_Machine_Learning_Models.ipynb)
    ```
    pip install pandas matplotlib seaborn beautifulsoup4 nltk wordcloud distance xgboost scikit-learn tabulate
    ```
  - `Deep Learning`:The dependencies you may need for [Deep learning files](https://github.com/shengjie94/AIM5011-Group4/blob/main/Part_2_Deep_Learning_Models_using_Transformers.ipynb)
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
  - In the code, we first downloaded the pre trained DistilBERT model and made minor adjustments. After completing the training of the model, save it as distilbert50_ V2.pth. You can view the example in [distilbert50_v2](https://github.com/shengjie94/AIM5011-Group4/blob/main/distilbert50_v2/distilbert50_v2.pth).
  - We have created a simple web interface through Graph for using trained models for problem repetition determination. You can input two questions through this interface and obtain the predicted results of the model, that is, whether they are duplicate questions.
## Report Issues
Report bugs or feature requests using the [Duplicate problem recognizer issue tracker](https://github.com/shengjie94/AIM5011-Group4/issues).
At the same time, we also have a reporting function on the webpage. If there is a problem during use, click the 'Flag' button to mark it.
