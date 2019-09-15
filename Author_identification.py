import collections
import matplotlib.pyplot as plt
from math import fabs


alphabet = list("абвгдеєжзиіїклмнопрстуфхцшчьюя \n")


def char_count(openfile):
    """
    Read the text content of a file and keep a running count of how often each character appears.
    :param openfile: file pointer with input text
    :return: dictionary with each character and its absolute frequency
    """
    sorted_char = dict(sorted(collections.Counter(c for l in openfile for c in l).items()))
    sorted_char = {k: v for k, v in sorted_char.items() if k in alphabet}
    return sorted_char


def read_file(file):
    f = open(file, "r")
    text = f.read().lower()
    f.close()
    return text


def count_char_frequency(char_count):
    """
    Determine relative frequency from absolute
    :param char_count: dictionary with each character and its absolute frequency
    :return: character and its relative frequency
    """
    character = []
    frequency = []
    for ch, fr in char_count.items():
        character.append(ch)
        frequency.append(fr)
    frequency = [i / sum(frequency) for i in frequency]
    return  character, frequency


def visualize_frequency(char, frequency, author):
    """
    Plot a histogram of relative character frequencies
    :param author: author's name
    """
    plt.bar(char, frequency, color='#0504aa', alpha=0.7)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Символ', fontsize=15)
    plt.ylabel('Частота', fontsize=15)
    plt.xticks(fontsize=8)
    plt.yticks(fontsize=10)
    plt.title('Частотний розподіл символів - ' + author, fontsize=15)
    plt.show()


def find_author_standart(author_composition):
    """
    Define the distribution functions of the authors and visualize them
    :param author_composition: dictionary with author and his composition
    :return: dictionary with author and his reference distribution function
    """
    author_standart = {}
    for author in author_composition:
        file = read_file(author_composition[author])
        file_char_count = char_count(file)
        char, frequency = count_char_frequency(file_char_count)
        char = ['sp' if i == ' ' else i for i in char]
        author_standart[author] = dict(zip(char, frequency))
        visualize_frequency(char, frequency, author)
    return author_standart


def find_input_frequency(open_file):
    """
    Define the distribution function of the input file and visualize it
    :param open_file: text
    :return: dictionary with char and it frequency
    """
    file = read_file(open_file)
    file_char_count = char_count(file)
    char, frequency = count_char_frequency(file_char_count)
    char = ['sp' if i == ' ' else i for i in char]
    visualize_frequency(char, frequency, "Вхід")
    return dict(zip(char, frequency))


def identify_author(standarts, input):
    """
    The author of the text is considered to be one of the authors
    for whom the norm of the difference between the density
    of the distribution function of the input text and the average
    author's density of the distribution function is minimal
    :param standarts: dictionary with author and his/her standart
    :param input: checked text
    :return: author's name
    """
    distance = dict(zip(list(standarts), [0 for i in range(len(standarts))]))
    for author in standarts:
        for char in input:
            if char in standarts[author]:
                distance[author] += fabs(input[char] - standarts[author][char])
    return min(distance, key=distance.get)


if __name__ == '__main__':
    #Dictionary - {Author: "his/her composition"}
    authors = {'Іван Драч': "drach-chornobyl.txt", 'Ліна Костенко': "kostenko-churai.txt"}
    #Author's standard - weighted average value of the density of the distribution function
    author_standart = find_author_standart(authors)
    # input - text to be attributed to one of the authors
    input_char_frequency = find_input_frequency("input.txt")
    print (identify_author(author_standart, input_char_frequency))