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
    print('Please type the boolean function you wish to use. (Default is "majority")')

    user_input = input('To exit type "0" \n')
    
    while user_input != "0":
        if user_input == '': boolean_function = 'majority'
        else: boolean_function = user_input

        print('Please enter a comma-seperated list containing only two distinct elements.\n')
        user_input = input('Example: x,y,x,x,y \n')
        user_input = list(user_input.split(','))
        elements = list(dict.fromkeys(user_input))

        if not validate_inputs(boolean_function, elements):
            print('Please type the boolean function you wish to use. (Default is "majority")') 
            user_input = input('To exit type "0" \n')
            continue

        output = fourer_walsh_transform(user_input, boolean_function_dict[boolean_function])
        print(output)

        user_input = input('\nTo exit, type "0", or try again. Which boolean function do you wish to use? \n')

# Boolean functions
def majority(x):
    assert len(x) % 2 == 1
    return 1 if sum(x) > 0 else -1

def minority(x):
    assert len(x) % 2 == 1
    return 1 if sum(x) < 0 else -1

def ratio(x):
    elements = list(dict.fromkeys(x))
    if len(elements) == 1: return 1.0
    a, b = elements
    return x.count(a) / len(x)

#Fourier-Walsh transform
def fourer_walsh_transform(user_input, boolean_function):
    
    input_list = to_bool(user_input, list(dict.fromkeys(user_input)))
    inputs = list(itertools.product([1,-1], repeat=len(input_list)))
    bool_func_values = [boolean_function(list(input_values)) for input_values in inputs]
    coefficients = fourier_coefficients(inputs, bool_func_values)

    result = 0
    for subset, coefficient in coefficients.items():
        subset_prod = np.prod([input_list[i] if subset[i] == 1 else 1 for i in range(len(input_list))])
        result += subset_prod * coefficient

    output_conversion = args.output_conversion
    if boolean_function in [majority, minority]: output_conversion = True
    if output_conversion: result = to_outputs(result, list(dict.fromkeys(user_input)))
    
    result = f'\nThe answer is {result}'
    if args.verbose: result += f'\nThe formula is: {formula_string_builder(coefficients)}'

    return result


def fourier_coefficients(inputs, bool_func_values):
    coefficients = {}
    boolean_products = itertools.product([0,1], repeat=len(inputs[0]))
    
    for subset in boolean_products:
        subset = np.array(subset)
        subset_products = np.prod(np.power(inputs, subset), axis=1)
        coefficient = np.mean(subset_products * bool_func_values)
        coefficients[tuple(subset)] = coefficient

    return coefficients

# Fourier-Walsh transform needs the boolean values to be interpreted as 1 or -1
def to_bool(inputs, elements):
    return [1 if x == elements[0] else -1 for x in inputs]

def to_outputs(value, elements):
    return elements[0] if value == 1.0 else elements[1]

def validate_inputs(boolean_function, elements):
    if boolean_function not in boolean_function_dict: 
        print('That is not a valid boolean function.')
        return False
    if len(elements) > 2: 
        print('The list must not contain more than two distinct elements.')
        return False
    
    return True

def formula_string_builder(coefficients):
    
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
    parser.add_argument('-o', '--output_conversion', action='store_true', help='Output conversion to original values')

    boolean_function_dict ={
        'majority': majority,
        'minority': minority,
        'ratio'   : ratio
    }

    args = parser.parse_args()
    main(args)