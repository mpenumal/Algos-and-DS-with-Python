"""
This file provides implementation of Print Neatly functionality.
It basically takes a list of words and max_line length (M) as inputs and
provides the most optimum way of arranging the words in a paragraph of
max_line length = M. It also provides the cost associated with this arrangement.
"""
import sys
INFINITY = sys.maxint


def print_neatly(words, M):
    """
    Print text neatly.
    Parameters
    ----------
    words: list of str
        Each string in the list is a word from the file.
    M: int
        The max number of characters per line including spaces

    Returns
    -------
    cost: number
        The optimal value as described in the textbook.
    text: str
        The entire text as one string with newline characters.
        It should not end with a blank line.

    Details
    -------
        Look at print_neatly_test for some code to test the solution.
    >>> print_neatly(["World","Map"], 10)
    (0, 'World Map')
    """
    word_count = len(words)
    word_length = [0] * word_count
    extra_spaces = [[0 for x in range(word_count)] for x in range(word_count)]
    line_cost = [[INFINITY for x in range(word_count)] for x in range(word_count)]

    optimum_cost_word_position = [0] * word_count

    # finding the number of characters in each word
    for i in range(0, word_count):
        word_length[i] = len(words[i])

    # finding the extra spaces and cost associated with all possible combinations of words per line.
    for i in range(0, word_count):		# let i be the first word of a given line
        for j in range(i, word_count): 	# let j be the last word of a given line. i <= j
            if i == j:
                extra_spaces[i][j] = M - word_length[i]
            else:
                extra_spaces[i][j] = extra_spaces[i][j-1] - word_length[j] - 1

            if extra_spaces[i][j] >= 0:		# combination of words will fit in a line.
                if j == word_count-1:		# last line
                    line_cost[i][j] = 0
                else:
                    line_cost[i][j] = (extra_spaces[i][j])**3

    cost, optimum_cost_word_position = get_cost_and_paragraph(word_count, line_cost, optimum_cost_word_position)

    # preparing the text output
    last_word_pos = word_count-1
    first_word_pos = optimum_cost_word_position[last_word_pos]
    text = ''
    while first_word_pos >= 0 and last_word_pos >= 0:
        temp_text = ''
        for i in range(first_word_pos, last_word_pos+1):
            temp_text += ' ' + words[i]
        last_word_pos = first_word_pos - 1
        first_word_pos = optimum_cost_word_position[last_word_pos]
        text = '\n' + temp_text[1:] + text

    return cost, text[1:]


def get_cost_and_paragraph(word_count, line_cost, optimum_cost_word_position):
    """
    finding best combination of words for each line and the cost assoicated with it.
    :return: cost and best combination of words for each line
    """
    cost = [INFINITY] * word_count
    for j in range(0, word_count):		# let j be the last word of a given line
        for i in range(0, j+1):			# let i be the first word of a given line. i <= j
            if i == 0:
                if line_cost[i][j] < cost[j]:			# updating the cost when considering words from 1 to j.
                    cost[j] = line_cost[i][j]			# updating position when new "least cost" is identified.
                    optimum_cost_word_position[j] = i
            # check if sum of cost of words from [i to j] & cost at i-1 is less than cost at j
            elif cost[i-1] + line_cost[i][j] < cost[j]:
                cost[j] = cost[i-1] + line_cost[i][j]  # updating the cost when considering words from 1 to j.
                optimum_cost_word_position[j] = i	   # updating position when new "least cost" is identified.
    return cost[-1], optimum_cost_word_position
