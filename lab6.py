import argparse
import random
from abc import ABC, abstractmethod

from faker import Faker

ESV = 1760


class Employee(ABC):
    def __init__(self, code, surname):
        self.code = code
        self.surname = surname

    @abstractmethod
    def salary(self):
        pass

    @abstractmethod
    def tax(self):
        pass


class HourlyEmployee(Employee):
    def __init__(self, code, surname, rate):
        super().__init__(code, surname)
        self.rate = rate

    def salary(self):
        return 20.8 * 8 * self.rate

    def tax(self):
        return self.salary() * (0.18 + 0.015)


class FixedEmployee(Employee):
    def __init__(self, code, surname, monthly):
        super().__init__(code, surname)
        self.monthly = monthly

    def salary(self):
        return self.monthly

    def tax(self):
        return self.salary() * (0.18 + 0.015)


class FOPEmployee(HourlyEmployee):
    def __init__(self, code, surname, rate, group):
        super().__init__(code, surname, rate)
        self.group = group

    def salary(self):
        return super().salary() * 1.1

    def tax(self):
        return self.salary() * 0.05 + ESV


class SelfEmployed(Employee):
    def __init__(self, code, surname, line_price, lines):
        super().__init__(code, surname)
        self.line_price = line_price
        self.lines = lines

    def salary(self):
        return self.line_price * self.lines

    def tax(self):
        return self.salary() * (0.18 + 0.015) + ESV


def generate_employees(n):
    fake = Faker("uk_UA")
    employees = []
    for _ in range(n):
        code = fake.unique.numerify("##########")
        surname = fake.last_name()
        kind = random.randint(1, 4)
        if kind == 1:
            employees.append(HourlyEmployee(code, surname, random.randint(150, 600)))
        elif kind == 2:
            employees.append(FixedEmployee(code, surname, random.randint(20000, 100000)))
        elif kind == 3:
            employees.append(FOPEmployee(code, surname, random.randint(150, 600), random.randint(1, 3)))
        else:
            employees.append(SelfEmployed(code, surname, random.randint(5, 30), random.randint(1000, 5000)))
    return employees


def sort_employees(employees):
    return sorted(employees, key=lambda e: (-e.salary(), e.surname))


def print_employees(employees):
    for e in employees:
        print(f"{e.code} {e.surname:<15} {e.salary():>10.2f} {e.tax():>10.2f}")


def main():
    parser = argparse.ArgumentParser(description="Працівники ІТ підприємства")
    commands = parser.add_subparsers(dest="command")
    commands.add_parser("group", help="ФОП за групою").add_argument("group", type=int, choices=[1, 2, 3])
    commands.add_parser("income", help="ФОП з доходом не менше заданого").add_argument("min", type=float)
    commands.add_parser("tax", help="ФОП з податком не менше заданого").add_argument("min", type=float)
    args = parser.parse_args()

    employees = sort_employees(generate_employees(20))
    fops = [e for e in employees if isinstance(e, FOPEmployee)]

    if args.command == "group":
        employees = [e for e in fops if e.group == args.group]
    elif args.command == "income":
        employees = [e for e in fops if e.salary() >= args.min]
    elif args.command == "tax":
        employees = [e for e in fops if e.tax() >= args.min]

    print_employees(employees)


if __name__ == '__main__':
    main()
