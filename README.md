# Anagram Cloud Creator Notebook

The following repository contains a notebook `Anagram_Cloud.ipynb`, which is used to make anagram clouds. Anagram clouds are variations on word clouds that emphasize words in a visual display using a metric other than frequency. In order to make your own anagram clouds, you must prepare a dataframe that has the following two columns:
- `text`: the words that make up a single text entry for the data set.
- `theme`: the binary label of whether the data point does or doesn't display traits of a given theme. The word theme is used here as a placeholder and should be swapped out with whatever appropriate column label is used during the creation of the anagram cloud.

Within the notebook, one can go through the process of designing both an anagram and word cloud in order to compare them directly. There are three example suites to choose from each with their own set of labels. The first example `twit_emo.csv` contains a set of twitter posts that are given a multi-classification labelling based on a variety of different emotions: joy, sadness, anger, anticipation, and fear. The anagram and word clouds made for each emotion attempt to visualize the topics being communicated by people based on their mood. The second example found within `pos_exp.csv` deals with people communicating a recent positive experience that they were willing to share. These positive experiences are categorized into one of seven labels. By selecting one of the labels, we can construct either a word or an anagram cloud that visualizes the key terms used by people who exhibit that label. The third example `title_topic.csv` labels academic paper titles with a field of study. Unlike the first example set, text entries in this set may exhibit multiple labels simultaneously. The `.png` files in the two folders `word_cloud` and `anagram_cloud` show the resulting clouds made from each respective method.

Visualization provided by this notebook:
- Scatterplot comparison of frequency values vs. permutation importance scores for feature tokens (both in raw value and ranked integer value)
- Venn Diagram showing overlap that exists between $n$ words that are most frequent within a theme vs. the words that have the highest permutation importance score.
- Word Clouds and Anagram Clouds.
