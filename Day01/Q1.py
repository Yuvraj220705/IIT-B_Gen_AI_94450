sentence = input("Enter a sentence: ")
count_characters = len(sentence)
print(count_characters)

count_words = len(sentence.split())
print(count_words)

count_vowels = 0
vowels = 'aeiouAEIOU'
for char in sentence:
    if char in vowels:
        count_vowels = count_vowels + 1
        
print(count_vowels)