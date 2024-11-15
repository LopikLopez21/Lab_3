import re
import unittest


def validate_gmail(email):
    pattern = r'^(?!.*\.\.)([a-zA-Z0-9](?:[a-zA-Z0-9.]{4,28})[a-zA-Z0-9])@gmail\.com$'
    return re.match(pattern, email) is not None


def validate_mail_ru(email):
    pattern = r'^(?![._-])(?!.*[._-]{2})([a-zA-Z0-9][a-zA-Z0-9._-]{3,29}[a-zA-Z0-9])@(mail|bk|internet|inbox|list)\.ru$'
    return re.match(pattern, email) is not None


def validate_yandex(email):
    pattern = r'^[a-zA-Z](?!.*[.-]{2})(?!.*\.\.)(?!.*--)[a-zA-Z0-9.-]{0,29}[a-zA-Z0-9]@(yandex\.ru|ya\.ru)$'
    return re.match(pattern, email) is not None


def validate_rambler(email):
    pattern = r'^[a-zA-Z0-9](?!.*[._-]{2})[a-zA-Z0-9._-]{1,30}[a-zA-Z0-9]@rambler\.ru$'
    return re.match(pattern, email) is not None


def validate_email(email):
    if '@gmail.com' in email:
        return validate_gmail(email)
    elif any(domain in email for domain in ['@mail.ru', '@bk.ru', '@internet.ru', '@inbox.ru', '@list.ru']):
        return validate_mail_ru(email)
    elif '@yandex.ru' in email or '@ya.ru' in email:
        return validate_yandex(email)
    elif '@rambler.ru' in email:
        return validate_rambler(email)
    else:
        return False


def search_emails_in_file(filename):
    try:
        with open(filename, 'r') as file:
            content = file.read()
            emails = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)
            return [email for email in emails if validate_email(email)]
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return []


def menu():
    while True:
        print("\nМеню:")
        print("1. Проверить e-mail адрес")
        print("2. Найти все e-mail адреса в файле")
        print("3. Выйти")

        choice = input("Выберите действие (1/2/3): ").strip()

        if choice == '1':
            user_email = input("Введите e-mail для проверки: ").strip()
            if validate_email(user_email):
                print(f"{user_email} является действительным.")
            else:
                print(f"{user_email} НЕ является действительным.")

        elif choice == '2':
            filename = input("Введите имя файла для поиска e-mail адресов: ").strip()
            valid_emails = search_emails_in_file(filename)
            if valid_emails:
                print(f"Действительные e-mail адреса, найденные в файле {filename}:")
                for email in valid_emails:
                    print(email)
            else:
                print(f"В файле {filename} не найдено действительных e-mail адресов.")

        elif choice == '3':
            print("Выход из программы.")
            break

        else:
            print("Некорректный ввод. Пожалуйста, выберите 1, 2 или 3.")


# Юнит-тесты
class TestEmailValidation(unittest.TestCase):
    def test_gmail(self):
        self.assertTrue(validate_gmail('user123@gmail.com'))
        self.assertFalse(validate_gmail('user@gmail.com'))  # too short
        self.assertFalse(validate_gmail('user.name..name@gmail.com'))  # three consecutive dots
        self.assertFalse(validate_gmail('user_name@gmail.com'))  # underscore not allowed
        self.assertFalse(validate_gmail('user_name.@gmail.com'))  # . end

    def test_mail_ru(self):
        self.assertTrue(validate_mail_ru('user123@mail.ru'))
        self.assertFalse(validate_mail_ru('user123.@mail.ru'))
        self.assertTrue(validate_mail_ru('user.name@bk.ru'))
        self.assertFalse(validate_mail_ru('us@mail.ru'))  # too short
        self.assertFalse(validate_mail_ru('usasd.-d@mail.ru'))
        self.assertTrue(validate_mail_ru('user.name.name@mail.ru'))  # three consecutive dots

    def test_yandex(self):
        self.assertFalse(validate_yandex('u@yandex.ru'))
        self.assertTrue(validate_yandex('u1@yandex.ru'))
        self.assertTrue(validate_yandex('user.name@ya.ru'))
        self.assertTrue(validate_yandex('user.name.name@yandex.ru'))  # three consecutive dots
        self.assertFalse(validate_yandex('1user.name.name@yandex.ru'))
        self.assertFalse(validate_yandex('user-@yandex.ru'))  # ends with hyphen
        self.assertFalse(validate_yandex('user.-s@yandex.ru'))

    def test_rambler(self):
        self.assertTrue(validate_rambler('user123@rambler.ru'))
        self.assertTrue(validate_rambler('123user123@rambler.ru'))
        self.assertFalse(validate_rambler('us@rambler.ru'))  # too short
        self.assertFalse(validate_rambler('user..name.name@rambler.ru'))  # three consecutive dots


if __name__ == '__main__':
    # Запуск тестов
    unittest.main(exit=False)

    # Запуск меню
    menu()