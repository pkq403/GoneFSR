import itertools, time

def formula(f):
  if f: 
    value = f.pop()
    if value == 0:
      return f'{formula(f)} + {formula(f)}'
    elif value == 1:
      return f'{formula(f)} * {formula(f)}'
    elif value == 2:
      return f'not {formula(f)}'
    else:
      return f'x{value-3}'
  else:
    return "S"

def evaluation(f, values):
  if f: 
    value = f.pop()
    if value == 0:
      return evaluation(f,values) ^ evaluation(f,values)
    elif value == 1:
      return evaluation(f,values) and evaluation(f,values)
    elif value == 2:
      return not evaluation(f,values)
    else:
      return values[value-3]
  else:
    return False
  
def calc_all_form_results(num_variables, num_op):
    tiempo = time.time()
    all_eval = set()
    for t in itertools.product(range(num_variables + 3), repeat=num_op):
        string = formula(list(t))
        if 'S' not in string:
            result = []
            for values in itertools.product([False, True], repeat=num_variables):
                result.append(evaluation(list(t), values))
            all_eval.add(tuple(result))
    return time.time() - tiempo, len(all_eval)
