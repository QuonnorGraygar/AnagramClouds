# Anagram Cloud Creator Notebook

The following repository contains a notebook `Anagram_Cloud.ipynb`, which is used to make anagram clouds. Anagram clouds are variations on word clouds emphasize words in a visual display using a metric other than frequency. In order to make your own anagram clouds, you must prepare a dataframe that has the following two columns:
- `text`: the words that make up a single data point of the word cloud.
- `example`: the binary label of whether the data point does or doesn't display traits of a given theme. The word example is used here as a placeholder and can be swapped out in the notebook at the user's discretion.

Within the notebook, there is a placeholder example that shows the differences between a word cloud and an anagram cloud. The example found within `ladded_example.csv` deals with students answering a question relating to the change in a ladder's slope as its height is adjusted to be twice its initial value. Certain students answering this question exhibit clear 'math variable relationship' skills based on the way that they describe their answer. We isolate these students and then generate both a word cloud and an anagram cloud from their corpus of text responses. The two included `.png` files show the resulting clouds made from each method.

Visualization provided by this notebook:
- Scatterplot comparison of frequency values vs. permutation importance scores for feature tokens (both in raw value and ranked integer value)
- Venn Diagram showing overlap that exists between $n$ words that are most frequent within a theme vs. the words that have the highest permutation importance score.
- Word Clouds and Anagram Clouds.
