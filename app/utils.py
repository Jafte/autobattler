

def plural(n: int, forms: list):
    if len(forms) != 3:
        return
    form_index = 2
    if n % 10 == 1 and n % 100 != 11:
        form_index = 0
    elif 2 <= n % 10 <= 4 and (n % 100 < 10 or n % 100 >= 20):
        form_index = 1

    return f"{n} {forms[form_index]}"


def divide_chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]
