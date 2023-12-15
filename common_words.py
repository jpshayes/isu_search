import pandas as pd
from collections import Counter

# Load the keywords CSV into a DataFrame
# Assumes each row in the CSV contains a URL and its associated keywords
file_path = 'keywords.csv'
df = pd.read_csv(file_path)

# Initialize an empty list to store all keywords from the CSV
all_keywords = []

# Iterate over each row in the DataFrame to extract and combine keywords
for keywords in df['Keywords']:
    # Split the keywords string into a list and extend the all_keywords list
    all_keywords.extend(keywords.split(', '))

# Use the Counter class from the collections module to count the frequency of each keyword
word_freq = Counter(all_keywords)

# Set a threshold for identifying common words
# Words appearing more frequently than this threshold are considered common
common_word_threshold = 10  # Adjust this number based on your specific needs and data

# Filter out common words based on the threshold
# Creates a list of words whose frequency is greater than the common_word_threshold
common_words = [word for word, freq in word_freq.items() if freq > common_word_threshold]

# Write the list of common words to a text file
with open('common_words.txt', 'w') as file:
    for word in common_words:
        # Each word is written on a new line
        file.write(f"{word}\n")

# Print the number of common words found for confirmation
print(f"Common words list generated with {len(common_words)} words.")
