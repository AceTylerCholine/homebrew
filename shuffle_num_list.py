import random

def generate_shuffled_numbers(start, end):
    numbers = list(range(start, end + 1))
    random.shuffle(numbers)
    return numbers

def create_text_file(numbers):
    with open('shuffled_numbers.txt', 'w') as file:
        file.write("Shuffled Numbers\n")
        for num in numbers:
            file.write(str(num) + '\n')

    print("Text file 'shuffled_numbers.txt' has been created successfully.")

start_num = 100
end_num = 999

shuffled_numbers = generate_shuffled_numbers(start_num, end_num)
create_text_file(shuffled_numbers)
