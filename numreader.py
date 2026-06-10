is_num = lambda num: isinstance(num, (int, float)) and not isinstance(num,bool)

is_int = lambda num: isinstance(num, int) 

is_pos = lambda num: num > 0 

is_natural = lambda num: is_int(num) and is_pos(num)

is_par = lambda num: is_int(num) and num % 2 == 0 


def is_prime(num):
  if not is_natural(num) or num <= 1:
    return False
  if num <= 1:
    return False
  i = 2
  while i * i <= num:
    if num % i == 0:
      return False
    i += 1
  return True


def is_perfect(num):
  if not is_natural(num) or num <= 1:
    return False

  total = 1
  i = 2
  while i * i <= num:
    if num % i == 0:
      total += i
      pair = num // i
      if pair != i:
        total += pair
    i += 1

  return total == num


def categorize_numlist(nums: list) -> dict:
  num = {}
  for n in nums:
    num[n] = {
      "Entero": is_int(n),
      "Positivo": is_pos(n),
      "Par": is_par(n),
      "Primo": is_prime(n),
      "Perfecto": is_perfect(n)
    }
  return num
