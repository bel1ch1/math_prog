al = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяабвгдеёжзийклмнопрстуфхцчшщъыьэюя'
chois = int(input())

if chois == 1: # шифровка
    val = input()
    key = int(input())
    val_lov = val.lower()
    vald = ''

    for letter in val_lov:
        pos = al.find(letter)
        new_pos = pos + key
        if letter in al:
            vald = vald + al[new_pos]
        else: vald = vald+ letter
    print(vald)

elif chois == 2: # Расшифровка
    val = input()
    key = int(input())
    val_lov = val.lower()
    vald = ''

    for letter in val_lov:
        pos = al.find(letter)
        new_pos = pos - key
        if letter in al:
            vald = vald + al[new_pos]
        else: vald = vald+ letter
    print(vald)
