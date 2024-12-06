Predicting Player Deaths in Dota 2 using Machine Learning

### Contents
- [Introduction](#introduction)
- [Parser](#parser)
- [Reproduce Results w/ Provided Data](#reproducing-results-with-provided-data)
- [Reproducing the Entire Pipeline](#reproducing-the-entire-pipeline)
- [Preprocessor Usage](#preprocessor-usage)
- [Dataset Links](#dataset-links)

# Introduction

The following is a proposed method for predictive analysis of deaths in Dota for identifying potentially risky scenarios in Dota 2.

The method performs predictions on player_0 in the dataset. Data formatting can be viewed in the [Processed CSVs](https://drive.google.com/drive/u/0/folders/1aE0tIW2qA6lz4NDHtfyODJOi9ATQS1oX) used in our dataset. The model uses 422 features for model prediction, but was tested using less with >80% results.

Models explored include
- K Nearest Neighbors
- Random Forest (Best Performing)
- Decision Tree

Experimental results demonstrate the effectiveness of the proposed approach, achieving an F1 score of 89% in predicting deaths within a five-second interval (Random Forest) and an F1 score of ~98% when the time frame is extended to 15 seconds (Random Forest).

Potential applications for this research include informing real time, in game, decision-making as well as assisting in camera direction for ESports events.

# Parser

To parse results, we utilized the [Clarity](https://github.com/skadistats/clarity)(a Java parsing library for Dota .dem match files) as a base to create a custom parser. This allows extraction of .dem files (default encoded format of Dota 2 files) to easily readable CSV files for use in model prediction. The [custom Clarity parser](https://github.com/srl3630/CS584_Game_Parsers/tree/main) can be found here.

# Reproducing Results with Provided Data:
1) Download [training data](https://drive.google.com/drive/u/0/folders/1TKzBp9inrMeUl_YeN2scXc4pKwJBgAjb) or use generated CSV dataset following steps below in [reproduce processed dataset](#reproduce-processed-dataset)
2) Load [train.ipynb](https://github.com/CombustibleToast/584-Project/blob/main/train.ipynb) using your preferred notebook engine (Colab or Jupyter(hub/lab) work)
3) Change the path referred to in the second cell of [train.ipynb](https://github.com/CombustibleToast/584-Project/blob/main/train.ipynb) to the path to the downloaded [training data](https://drive.google.com/drive/u/0/folders/1TKzBp9inrMeUl_YeN2scXc4pKwJBgAjb) 
4) Run the cells in sequence
5) Change the clf variable in `Classification Model`(EX. `clf=DecisionTreeClassifier()` for decision trees) and LAG variable in `Generate Label` (EX. `LAG=15` for a 15-second prediction window) cells as needed to validate prediction time ranges as well as different models (default is Random Forest for 5 second time range).

# Reproducing the Entire Pipeline:
1) Download (subset of) [raw dataset](https://drive.google.com/drive/u/0/folders/1BhPDWVsEoONzgv8mJaPm0vxTkEls5tdg) 
2) Clone repository locally `git clone https://github.com/CombustibleToast/584-Project.git`
3) Parse downloaded dataset using [custom Clarity parser](https://github.com/srl3630/CS584_Game_Parsers/blob/main/README.md) (Note: may require unzipping files before processing, batch script will parse an entire zipped directory automatically)
4) Run [preprocessor](https://github.com/CombustibleToast/584-Project/blob/main/preprocessing/run3.py) on parsed dataset. See [preprocessor usage](#preprocessor-usage)
5) Concatenate results of processed CSVs into a single CSV
6) Follow steps above in [reproduce paper results](#reproducing-results-with-provided-data) to reproduce results

# Preprocessor Usage

`python3 run.py <input folder> <output folder>`

# Dataset Links:
- [Raw Dataset](https://drive.google.com/drive/u/0/folders/1BhPDWVsEoONzgv8mJaPm0vxTkEls5tdg) (Raw replay files from Dota 2 .dem.bz2)
- [Parsed Replays](https://drive.google.com/drive/u/0/folders/10GY-Z_bzzpBv2IYb3bJyrPCzLxcqwwfh) (.CSV format)
- [Processed CSVs](https://drive.google.com/drive/u/0/folders/1aE0tIW2qA6lz4NDHtfyODJOi9ATQS1oX) (.CSV format)
- [Training Data](https://drive.google.com/drive/u/0/folders/1TKzBp9inrMeUl_YeN2scXc4pKwJBgAjb) (.CSV format)

