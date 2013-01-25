def tdee(weight=200, height=72, age=39, sex='m', multiplier=1.2):
  '''Calculates daily energy expenditue from weight(lbs), height(in), age, sex and activity level.
  Multipliers for activity level are:
    Sedentary:          1.2   (default, little exercise)
    Lightly active:     1.375 (light exercise)
    Moderately active:  1.55  (moderate exercise)
    Very active:        1.725 (hard exercise)
    Extremely active:   1.9   (hard exercise daily)'''

  weight = weight * 0.453592  # convert to kg
  height = height * 2.54      # convert to cn
  if sex == 'm':
    return (66 + (13.7 * weight) + (5 * height) - (6.8 * age)) * multiplier
  elif sex == 'f':
    return (655 + (9.6 * weight) + 1.8 * height - (4.7 * age)) * multiplier
  else:
    return None

def bmi(weight=200, height=72):
  '''Calculates BMI from weight (lbs) and height (in)'''
  
  return (weight * 703) / (height ** 2)
  
