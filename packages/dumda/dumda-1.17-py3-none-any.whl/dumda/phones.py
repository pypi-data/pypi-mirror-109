def generate_number():
    """
    Generates a random phone number
    """
    from random import randint
    NPA = str(randint(201, 999))
    NXX = str(randint(2, 9)) + str(randint(00, 99))
    XXXX = str(randint(0000, 9999))
    phone = NPA + "-" + NXX + "-" + XXXX

    return phone
