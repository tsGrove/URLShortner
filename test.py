import random
import string

length = 12
characters = string.ascii_letters + string.digits
generated_string = ''.join(random.choices(characters, k=length))
print(generated_string)

user_data = {"username": "Pierce"}

print(user_data["username"])