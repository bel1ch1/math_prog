def caesar_cipher(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            shift_base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            result += char
    return result

def main():
    action = input("Выберите действие (шифрование/дешифрование): ").strip().lower()
    text = input("Введите текст: ")
    shift = int(input("Введите сдвиг: "))

    if action == "шифрование":
        print("Зашифрованный текст:", caesar_cipher(text, shift))
    elif action == "дешифрование":
        print("Расшифрованный текст:", caesar_cipher(text, -shift))
    else:
        print("Неверное действие!")

if __name__ == "__main__":
    main()
