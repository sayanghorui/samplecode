
class my_dictionary(dict):

    def __init__(self):
        self = dict()

    def add(self, key, value):
        self[key] = value


f = open('data_input.txt', "r")
lines = f.read()
f.close()
# print(lines)
elements = lines.splitlines()

# read the lines in the input file and divide them into three list
rule_list = []
fuzzy_sets = []
measurements = []

for items in elements:
    if 'Rule' in items:
        rule_list.append(items)
    elif '=' in items:
        measurements.append(items)
    else:
        fuzzy_sets.append(items)
fuzzy_sets = [i for i in fuzzy_sets if i != '']
print('rule list: ', rule_list)
print('fuzzy sets: ', fuzzy_sets)
print('measurements: ', measurements)

# Iterating the Fuzzy_set and Measurements(input) lists to generate dictionary for the same
def parse_fuzzy_sets_measurements(fuzzy_sets, measurements):
    fuzzy_sets_copy = fuzzy_sets.copy()
    dict_fuzzy_sets = my_dictionary()
    dict_measurements = my_dictionary()
    new_list = []
    new_list_list = []

    for items in fuzzy_sets_copy:
        new_list.append(items)

        if ' ' not in items:
            new_list.remove(items)
            new_list = []
            new_list.append(items)
            new_list_list.append(new_list)
    # print(new_list_list)

    for items in new_list_list:
        dict_obj = my_dictionary()
        for item in items:
            if ' ' in item:
                x = item.split(' ', 1)
                keys = x[0]
                values = [int(s) for s in x[1].split(' ')]
                dict_obj.add(keys, values)
        dict_fuzzy_sets.add(items[0], dict_obj)

    for measurement in measurements:
        x = measurement.split(' =')
        dict_measurements.add(x[0], int(x[1]))

    return dict_fuzzy_sets, dict_measurements

dict_fuzzy_sets, dict_measurements = parse_fuzzy_sets_measurements(fuzzy_sets, measurements)
#print('measurement dictionary: ', dict_measurements)
#print('fuzzy sets dictionary: ', dict_fuzzy_sets)

# helper function to calculate membership degree
def membership_function(x, list_range):
    a = list_range[0]
    b = list_range[1]
    alpha = list_range[2]
    beta = list_range[3]
    membership_degree = 0
    if x <= (a - alpha):
        membership_degree = 0
    elif (a - alpha) < x < a:
        membership_degree = (x - a + alpha) / alpha
    elif a <= x <= b:
        membership_degree = 1
    elif b < x < (b + beta):
        membership_degree = (b + beta - x) / beta
    elif x >= (b + beta):
        membership_degree = 0
    return round(membership_degree,3)

# function for Fuzzy AND operation
def min_calculation(list_of_values):
    z = min(list_of_values)
    return z

# function for Fuzzy OR operation
def max_calculation(list_of_values):
    z = max(list_of_values)
    return z

# Fuzzification
def membership_value_calculation(dict_measurements, dict_fuzzy_sets):
    membership_value_dict = my_dictionary()
    for items in dict_measurements.keys():
        if items in dict_fuzzy_sets.keys():
            membership_value_dictionary = my_dictionary()
            for keys, values in dict_fuzzy_sets[items].items():
                membership_values = membership_function(dict_measurements[items], values)
                membership_value_dictionary.add(keys, membership_values)
        membership_value_dict.add(items, membership_value_dictionary)
    return membership_value_dict

membership_value_dictionary = membership_value_calculation(dict_measurements, dict_fuzzy_sets)
#print('membership values dictionary: ', membership_value_dictionary)

'''def parse_calculate_rule(rule_list, membership_value_dictionary):
    rule_dictionary = my_dictionary()
    for items in rule_list:
        if ':' in items:
            x = items.split()
            for words in x:
                if words == 'If' or words == 'then' or words == 'Rule' or words == 'is':
                    x.remove(words)
            #print(len(x))
            blank_list = []
            if x[3] == 'and':
                if x[1] in membership_value_dictionary.keys():
                    for keys, values in membership_value_dictionary[x[1]].items():
                        if keys == x[2]:
                            blank_list.append(values)
                if x[4] in membership_value_dictionary.keys():
                    for keys, values in membership_value_dictionary[x[4]].items():
                        if keys == x[5]:
                            blank_list.append(values)
                if x[len(x) - 1] in rule_dictionary.keys():
                    current_value = rule_dictionary[x[len(x) - 1]]
                    rule_dictionary.add(x[len(x) - 1],max(current_value, min_calculation(blank_list)))
                else:
                    rule_dictionary.add(x[len(x) - 1], min_calculation(blank_list))
            if x[3] == 'or':
                if x[1] in membership_value_dictionary.keys():
                    for keys, values in membership_value_dictionary[x[1]].items():
                        if keys == x[2]:
                            blank_list.append(values)
                if x[4] in membership_value_dictionary.keys():
                    for keys, values in membership_value_dictionary[x[4]].items():
                        if keys == x[5]:
                            blank_list.append(values)
                if x[len(x) - 1] in rule_dictionary.keys():
                    current_value = rule_dictionary[x[len(x) - 1]]
                    rule_dictionary.add(x[len(x) - 1],max(current_value, max_calculation(blank_list)))
                else:
                    rule_dictionary.add(x[len(x) - 1], max_calculation(blank_list))

    return rule_dictionary'''

# Inference Engine
def parse_calculate_rule(rule_list, membership_value_dictionary):
    rule_dictionary = my_dictionary()
    for items in rule_list:
        if ':' in items:
            x = items.split()
            for words in x:
                if words == 'If' or words == 'then' or words == 'Rule' or words == 'is':
                    x.remove(words)
            blank_list = []
            if 'and' in x and 'or' not in x:
                for i in range(1,(len(x)-2),3):
                    #print(x[i])
                    if x[i] in membership_value_dictionary.keys():
                        for keys, values in membership_value_dictionary[x[i]].items():
                            if keys == x[i+1]:
                                blank_list.append(values)
                if x[len(x) - 1] in rule_dictionary.keys():
                    current_value = rule_dictionary[x[len(x) - 1]]
                    rule_dictionary.add(x[len(x) - 1],max(current_value, min_calculation(blank_list)))
                else:
                    rule_dictionary.add(x[len(x) - 1], min_calculation(blank_list))
            if 'or' in x and 'and' not in x:
                for i in range(1,(len(x)-2),3):
                    #print(x[i])
                    if x[i] in membership_value_dictionary.keys():
                        for keys, values in membership_value_dictionary[x[i]].items():
                            if keys == x[i+1]:
                                blank_list.append(values)
                if x[len(x) - 1] in rule_dictionary.keys():
                    current_value = rule_dictionary[x[len(x) - 1]]
                    rule_dictionary.add(x[len(x) - 1],max(current_value, max_calculation(blank_list)))
                else:
                    rule_dictionary.add(x[len(x) - 1], max_calculation(blank_list))
    return rule_dictionary

dict_rules_fuzzified = parse_calculate_rule(rule_list, membership_value_dictionary)
print('fuzzified rule dictionary: ', dict_rules_fuzzified)

# Defuzzification
# helper function for Centroid Calculation
def centroid_calculation(list_range):
    a = list_range[0]
    b = list_range[1]
    alpha = list_range[2]
    beta = list_range[3]
    starting_point = a - alpha
    end_point = b + beta
    lower_base = end_point - starting_point
    upper_base = b - a
    height = 1

    if a == b:
        mid_point = starting_point + (lower_base/2)
        centroid = a + (((mid_point - a)*2)/3)
    else:
        centroid = (((2 * lower_base) + upper_base)/(3 * (lower_base + upper_base))) * height

    return round(centroid,3)

# helper function for area calculation
def area_calculation(list_range):
    fuzzified_value = list_range[0]
    a = list_range[1]
    b = list_range[2]
    alpha = list_range[3]
    beta = list_range[4]
    starting_point = a - alpha
    end_point = b + beta
    lower_base = end_point - starting_point
    upper_base = b - a

    result_area = 0.5 * fuzzified_value * (lower_base + ((1 - fuzzified_value) * lower_base))
    return round(result_area, 3)

def defuzzification(dict_fuzzy_sets,dict_measurements,dict_rules_fuzzified):
    keys_fuzzy_sets = []
    keys_measurements = []
    for items in dict_fuzzy_sets.keys():
        keys_fuzzy_sets.append(items)
    for items in dict_measurements.keys():
        keys_measurements.append(items)

    for items in keys_fuzzy_sets:
        if items not in keys_measurements:
            result_variable = items

    if result_variable in dict_fuzzy_sets.keys():
        values_dictionary = dict_fuzzy_sets[result_variable]
    #print(values_dictionary)

    centroid_dictionary = my_dictionary()
    for items in values_dictionary.keys():
        #print(values_dictionary[items])
        centroid_dictionary.add(items, centroid_calculation(values_dictionary[items]))
    #print('centroid dictionary: ', centroid_dictionary)

    area_dictionary = my_dictionary()
    for items in values_dictionary.keys():
        new_list = []
        if items in dict_rules_fuzzified.keys():
            new_list.append(dict_rules_fuzzified[items])
            for item in values_dictionary[items]:
                new_list.append(item)
            area_dictionary.add(items, area_calculation(new_list))

    #print('area dictionary: ', area_dictionary)

    area_centroid = 0
    area = 0
    for items in centroid_dictionary.keys():
        if items in area_dictionary.keys():
            area_centroid += (centroid_dictionary[items]) * (area_dictionary[items])
            area += area_dictionary[items]
    if area != 0:
        result = (area_centroid/area)
    else:
        result = 0
    return result

output = defuzzification(dict_fuzzy_sets,dict_measurements,dict_rules_fuzzified)
print('Crisp output:',output)