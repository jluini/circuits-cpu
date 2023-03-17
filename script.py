code = '''
  'h' -> Write
  'e' -> Write
  'l' -> Write
  'l' -> Write
  'o' -> Write
  ' ' -> Write
  'w' -> Write
  'o' -> Write
  'r' -> Write
  'l' -> Write
  'd' -> Write
  '!' -> Write
  '\\n' -> Write
  'J' -> Write
  'A' -> Write
  
  # 'l' -> A
  # A -> write
  # 'l' -> A
  # A -> write
  # 'o' -> A
  # A -> write
  # ' ' -> A
  # A -> write
  # 'w' -> A
  # A -> write
  # 'o' -> A
  # A -> write
  # 'r' -> A
  # A -> write
  # 'l' -> A
  # A -> write
  # 'd' -> A
  # A -> write
'''

import re

def run(code):
  # print('Hola')

  # print(code)

  # print('Chau')

  print(parse(code))

def parse(code):
  out = []
  
  for line_index, line in enumerate(code.splitlines()):
    # print(f'Line {line_index + 1} of length {len(line)}: \'{line}\'')
    print(f'{line_index + 1}: {line}')
    
    if '#' in line:
      line = line[:line.index('#')]
    
    line = line.strip()
    
    if len(line) == 0:
      continue
    
    match1 = re.compile(r'^(.+)->(.+)$').match(line)
    
    if match1 == None:
      print(f'Line {line_index + 1} is invalid: \'{line}\'')
      return []
    
    left_term, right_term = match1.groups()
    
    left_valid, left_coso1, left_coso2 = parse_term(left_term)
    right_valid, right_coso1, right_coso2 = parse_term(right_term)
    
    if not left_valid:
      print(f'Line {line_index + 1}: left term \'{left_term}\' is invalid')
      return []
    
    if not right_valid or right_coso1 != 'register':
      print(f'Line {line_index + 1}: right term \'{right_term}\' is invalid')
      return []
    
    source = 0
    constant = 0
    action = right_coso2 + 2
    
    if left_coso1 == 'constant':
      constant = (left_coso2 << 19)
    else:
      if left_coso2 > 1:
        print(f'Line {line_index + 1}: left term \'{left_term}\' is invalid')
        return []
      
      source = left_coso2 + 2
    
    # action = right_coso2 + 2
    
    instruction = 0
    instruction |= constant
    instruction |= action
    instruction |= source << (4 + 3 * right_coso2)
    
    print(f'{constant} {source} {right_coso2} {action} => {bin(instruction)}')
    
    out.append(instruction)
  
  return out
  
def parse_term(term):
  term = term.strip()
  
  out = 0
  
  if term == 'A':
    return True, 'register', 0
  elif term == 'B':
    return True, 'register', 1
  elif term.lower() in ['write', 'w']:
    return True, 'register', 2
  
  constant_regex = re.compile(r'\'(..?)\'')
  constant_match = constant_regex.match(term)
  
  if constant_match:
    char = constant_match.group(1)
    if len(char) > 1:
      if char != '\\n':
        return False, 'invalid', 0
      return True, 'constant', 13 # ord('\n')
    elif not char.isascii():
      return False, 'invalid', 0
    
    return True, 'constant', ord(char)
  
  # raise BaseException(f'Término inválido: {term}')
  return False, 'invalid', 0
  
run(code)
