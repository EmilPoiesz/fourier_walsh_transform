import numpy as np
import itertools
import argparse

#########################################################################
#                                                                       #
#                  FOURIER-WALSH-TRANSFORM                              #
#                                                                       #
#   Any boolean function can be calculated as a polynomial              #
#   with rational coefficients using the Fourier-Walsh transform.       #
#   This program has the majority boolean function as default.          #
#                                                                       #
#   https://en.wikipedia.org/wiki/Walsh_function                        #
#                                                                       #
#   This project was meant for my own exploration. It is not an         #
#   efficient way to calculate boolean functions                        #
#                                                       -Emil Poiesz    #
#########################################################################

def main(args):

    print('This python program comutes the output of any boolean function using a Fourier-Walsh transform.')
    print('Read more here: https://en.wikipedia.org/wiki/Walsh_function')
    print()
    print()
    print('You can choose between the following boolean functions:')
    print('majority => majority([T,F,T]) = T') 
    print('minority => minority([T,F,T]) = F') 
    print('ratio    => ratio([T,F,T,T])  = 0.75')
    print('weighted sum => weighted_sum([T,F,T]) = #T + 2#F = 4')
    print('majority sum => majority_sum([T,F,T]) = #T - #F = 1')
    print('three in a row => three_in_a_row([T,F,F,F,T]) = T')
    print('alternating => alternating([T,F,T,F,T]) = T')
    print('Please type the boolean function you wish to use. (Default is "majority")')

    user_input = input('To exit type "0" \n')
    
    while user_input != "0":
        if user_input == '': boolean_function = 'majority'
        else: boolean_function = user_input

        print('Please enter a comma-seperated list containing only two distinct elements.\n')
        user_input = input('Example: x,y,x,x,y \n')
        user_input = list(user_input.split(','))

        if not validate_inputs(boolean_function, user_input):
            print('Please type the boolean function you wish to use. (Default is "majority")') 
            user_input = input('To exit type "0" \n')
            continue
        
        boolean_function = boolean_function_dict[boolean_function]
        output = fourer_walsh_transform(user_input, boolean_function)
        print(output)

        user_input = input('\nTo exit, type "0", or try again. Which boolean function do you wish to use? \n')

# Boolean functions
def majority(x: list) -> int:
    assert len(x) % 2 == 1
    return 1 if sum(x) > 0 else -1

def minority(x: list):
    assert len(x) % 2 == 1
    return 1 if sum(x) < 0 else -1

def ratio(x: list) -> float:
    elements = list(dict.fromkeys(x))
    if len(elements) == 1: return 1.0
    a, _ = elements
    return x.count(a) / len(x)

def weighted_sum(x: list) -> int:
    elements = list(dict.fromkeys(x))
    if len(elements) == 1: return sum(x)
    a, b = elements
    return x.count(a) + (2*x.count(b))

def majority_sum(x: list) -> int:
    return sum(x)

def three_in_a_row(x: list) -> int:
    if len(x) < 3: return -1
    for i in range(2,len(x)):
        if x[i] == x[i-1] and x[i] == x[i-2]: return 1
    return -1

def alternating(x: list) -> int:
    if len(x) == 1: return 1
    for i in range(1, len(x)):
        if x[i] == x[i-1]: return -1
    return 1
    

#Fourier-Walsh transform
def fourer_walsh_transform(user_input: str, boolean_function) -> str:
    
    input_length        = len(user_input)
    input_permutations  = list(itertools.product([1,-1], repeat=input_length))
    permutation_results = [boolean_function(list(inputs)) for inputs in input_permutations]

    coefficients = {}
    boolean_products = itertools.product([0,1], repeat=len(input_permutations[0]))
    for subset in boolean_products:
        subset          = np.array(subset)
        subset_products = np.prod(np.power(input_permutations, subset), axis=1)
        coefficient     = np.mean(subset_products * permutation_results)
        coefficients[tuple(subset)] = coefficient

    converted_input = input_to_int(user_input, list(dict.fromkeys(user_input))) #Convert input to {-1, 1}
    result = 0
    for permutation, coefficient in coefficients.items():
        permutation_sign = np.prod([converted_input[i] if permutation[i] == 1 else 1 for i in range(input_length)])
        result += permutation_sign * coefficient

    if boolean_function in [majority, minority]:          result = int_to_output(result, list(dict.fromkeys(user_input)))
    if boolean_function in [three_in_a_row, alternating]: result = int_to_bool(result)
    
    result = f'\nThe answer is {result}'
    if args.verbose: result += f'\nThe formula is: {formula_string_builder(coefficients)}'

    return result

# Fourier-Walsh transform needs the boolean values to be interpreted as 1 or -1
def input_to_int(inputs: list, elements: list) -> int:
    return [1 if x == elements[0] else -1 for x in inputs]

def int_to_bool(result:int) -> bool:
    if result == 1: return True
    return False

def int_to_output(value: float, elements:list) -> str:
    return elements[0] if value == 1.0 else elements[1]

def validate_inputs(boolean_function, user_input: str) -> bool:
    elements = list(dict.fromkeys(user_input))
    if boolean_function not in boolean_function_dict: 
        print('That is not a valid boolean function.')
        return False
    if len(elements) > 2: 
        print('The list must not contain more than two distinct elements.')
        return False
    
    return True

def formula_string_builder(coefficients: dict) -> str:
    unique_coefficients = {}
    for subset in coefficients.keys():
        if sum(subset) not in unique_coefficients.keys():
            unique_coefficients[sum(subset)] = coefficients[subset]

    output_str = ""
    for i, coefficient in enumerate(unique_coefficients):
        if unique_coefficients[coefficient] == 0.0: continue
        monomial = "".join([f'X{n}' for n in range(1, i+1)])
        output_str += f" {unique_coefficients[coefficient]}\u03A3({monomial}) +"
    output_str = output_str[:-2]

    return output_str


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true', help='Output verbosity')
    args = parser.parse_args()

    boolean_function_dict ={
        'majority'    : majority,
        'minority'    : minority,
        'ratio'       : ratio,
        'weighted sum': weighted_sum,
        'majority sum': majority_sum,
        'three in a row': three_in_a_row,
        'alternating' : alternating 
    }
    
    main(args)