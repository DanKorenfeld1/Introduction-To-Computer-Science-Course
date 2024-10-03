def input_list():
    """
    function that input from user numbers and return the list of them,
    and the sum of all the number as the last index.
    :return: list (int) of all the number and the sum as the last index.
    """
    count = 0  # count the sum of all the number
    list_of_number = []

    number_from_user = input()
    while not number_from_user == "":
        count += float(number_from_user)
        list_of_number.append(float(number_from_user))

        number_from_user = input()
    list_of_number.append(count)
    return list_of_number


def inner_product(vec_1, vec_2):
    """
    function that return the inner product of 2 vectors
    :param vec_1: list of number (int or float)
    :param vec_2: list of number (int or float)
    :return: number (list or float) -> the result of the inner product
    """
    if (len(vec_1) == 0) and (len(vec_2) == 0):
        return 0
    elif len(vec_1) != len(vec_2):
        return None

    the_inner_products = 0
    for i in range(len(vec_1)):
        the_inner_products += vec_1[i] * vec_2[i]
    return the_inner_products


def monotonically_rising(sequence):
    """
    check if the list is monotonically rising
    :param sequence: list of int or float
    :return: Boolean (True or False) -> if the list is monotonically rising
                                        or not
    """
    for i in range(1, len(sequence)):
        if sequence[i - 1] > sequence[i]:
            return False
    return True


def monotonically_really_rising(sequence):
    """
    check if the list is monotonically really rising
    :param sequence: list of int or float
    :return: Boolean (True or False) -> if the list is monotonically relly
                                        rising or not
    """
    for i in range(1, len(sequence)):
        if sequence[i - 1] > sequence[i] or sequence[i - 1] == sequence[i]:
            return False
    return True


def monotonically_descending(sequence):
    """
    check if the list is monotonically descending
    :param sequence: list of int or float
    :return: Boolean (True or False) ->if the list is monotonically descending
                                        or not
    """
    for i in range(1, len(sequence)):
        if sequence[i - 1] < sequence[i]:
            return False
    return True


def monotonically_really_descending(sequence):
    """
    check if the list is monotonically really descending
    :param sequence: list of int or float
    :return: Boolean (True or False) -> if the list is monotonically relly
                                        descending or not
    """
    for i in range(1, len(sequence)):
        if sequence[i - 1] < sequence[i] or sequence[i - 1] == sequence[i]:
            return False
    return True


def sequence_monotonicity(sequence):
    """
    function that check if sequence is monotonicity:
    monotonically rising
    monotonically really rising
    monotonically descending
    monotonically really descending
    :param sequence: list of numbers (int or float)
    :return: list of boolean of the sequence is monotonicity
    """
    if len(sequence) <= 1:
        return [True, True, True, True]
    list_of_monotonicity = []  # list of boolean
    list_of_monotonicity.append(monotonically_rising(sequence))
    list_of_monotonicity.append(monotonically_really_rising(sequence))
    list_of_monotonicity.append(monotonically_descending(sequence))
    list_of_monotonicity.append(monotonically_really_descending(sequence))
    return list_of_monotonicity


def monotonicity_inverse(def_bool):
    """
    function that return example of sequence monotonicity from the list of
    boolean
    :param def_bool: list of boolean (the rule of the sequence)
    :return: list of numbers (list or float) that present sequence
    """
    # example_of_sequence: key (list of boolean)-> value: example of boolean
    example_of_sequence = {(True, True, False, False): [1, 2, 3, 4],
                           (True, False, False, False): [1, 2, 2, 4],
                           (False, False, True, True): [4, 3, 2, 1],
                           (True, False, True, False): [1, 1, 1, 1],
                           (False, False, True, False): [4, 2, 2, 1],
                           (False, False, False, False): [4, 2, 4, 1]
                           }
    for i in example_of_sequence.keys():
        if i == tuple(def_bool):
            return example_of_sequence[i]
    return None


def is_prime(n):
    """
    check if number is prime or not
    :param n: the number that the funciton check
    :return: boolean (if is prime or not)
    """
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def primes_for_asafi(n):
    """
    function that return list of the "n" first prime number (from number 2)
    :param n: the number of the prime and the len of the list
    :return: list (int) of prime numbers
    """
    i = 2
    list_of_prime = []
    while len(list_of_prime) < n:
        if is_prime(i):
            list_of_prime.append(i)
        i += 1
    return list_of_prime


def sum_of_vectors(vec_lst):
    """
    function that return the number of the sum of vectors
    :param vec_lst: list of vectors (list of list)
    :return: (int or float) the sum of the vectors
    """
    if len(vec_lst) == 0:
        return None

    sum_list = []
    for i in range(len(vec_lst[0])):  # want to find the length of each list
        count = 0
        for vector in vec_lst:  # scan every list in specific index
            # for example: all the value from the list in
            # index 0-> index 1....
            count += vector[i]
        sum_list.append(count)
    return sum_list


def num_of_orthogonal(vectors):
    """
    function that return the number of the pair of vertical vectors
    (their multiple is 0)
    :param vectors: list of vectors -> list of number list
    :return: (int or float) the number of the pair
    """
    count_of_pair = 0
    for i_vector in range(len(vectors)):
        for j_vevtor in range(i_vector + 1, len(vectors)):
            if inner_product(vectors[i_vector], vectors[j_vevtor]) == 0:
                count_of_pair += 1
    return count_of_pair
