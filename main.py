# Loel var 2
print('start code …')
import transport, os


operations_count = 0
clients = []
transports = []
transportcompanys = []

def add_transport_company():
    global operations_count
    print("=" * 30)
    name = input("Введите имя Транспортной компании: ")
    transportcompanys.append(transport.TransportCompany(name))
    print("Транспортная компания добавлена")
    print("=" * 30)
    operations_count += 1
    menu()


def add_client():
    global operations_count
    print("=" * 30)
    name = input("Введите имя клиента: ")
    cargo_weight = float(input("Введите вес груза (в тоннах): "))
    if cargo_weight <= 0:
        print("Ошибка: Вес груза должен быть положительным!")
        menu()
    vip_input = input("VIP клиент? (1 - да/2 - нет): ")
    if vip_input == "1":
        is_vip = True
    elif vip_input == '2':
        is_vip = False
    else:
        print("Ошибка: Введено не число 1 или 2!")
        menu()

    client = transport.Client(name, cargo_weight, is_vip)
    clients.append(client)
    print("Клиент добавлен")
    print("=" * 30)
    operations_count += 1
    menu()

def all_transport():
    global operations_count
    print("=" * 30)
    for i, tr in enumerate(transports):
        print(f"{i+1}. ID: {tr.vehicle_id}, грузоподъёмность: {tr.capacity}, текущая загрузка: {tr.current_load}, список клиентов чьи грузы загружены: {tr.clients_list}")
    print("=" * 30)
    operations_count += 1
    menu()

def all_clients():
    global operations_count
    print("=" * 30)
    for i, cl in enumerate(clients):
        print(f"{i+1}. Имя {cl.name}, вес груза {cl.cargo_weight}, VIP-статус {cl.is_vip}")
    print("=" * 30)
    operations_count += 1
    menu()

def add_transport():
    global operations_count
    print("=" * 30)
    name = input("Вы хотите создать: 1 - Ship, 2 - Truck, 3 - Другой транспорт?")
    capacity = input("Введите грузоподъемность (в тоннах): ")
    if isinstance(capacity, float):
        print("Ошибка: Грузоподъемность должна быть числом!")
        menu()
    capacity = float(capacity)
    if capacity <= 0:
        print("Ошибка: Грузоподъемность должна быть положительным числом!")
        menu()
    if name == "1":
        name = input("Введите название судна: ")
        tra = transport.Ship(capacity, name)
        transports.append(tra)
    elif name == "2":
        color = input("Введите цвет грузовика: ")
        tra = transport.Truck(capacity, color)
        transports.append(tra)
    elif name == "3":
        tra = transport.Vehicle(capacity)
        transports.append(tra)
    else:
        print("Ошибка: Введено неправильное число!")
        menu()
    print("Транспорт добавлен")
    print("=" * 30)
    operations_count += 1
    menu()

def load_transport():
    global operations_count
    print("=" * 30)
    id = input("Введите ID машины: ")
    found = False
    for i in transports:
        if str(i.vehicle_id) == id:
            found = True
            tran = i
    if found == False:
        print("Транспорта с таким ID не существует")
        menu()
    else: 
        name_client = input("Введите имя клиента: ")
        for i in clients:
            if str(i.name) == name_client:
                found = True
                cli = i
        if found == False:
            print("Клиента с таким именем не существует")
            menu()
    tran.load_cargo(cli)
    print("Груз заружен!")
    print("=" * 30)
    operations_count += 1
    menu()

def optimize_cargo():
    global operations_count
    print("=" * 30)
    transportcompanys[0].optimize_cargo_distribution()


    print("=" * 30)
    operations_count += 1
    menu()


def exit_program():
    global operations_count
    print(f"\nКоличество выполненных операций: {operations_count}")
    print('end code …')
    os._exit()




def menu():
    global operations_count
    print('1 - Создать транспортную компанию ') #
    print('2 - Вывести весь транспорт ') #
    print('3 - Вывести всех клиентов ')#
    print('4 - Создать клиента ') #
    print('5 - Добавить транспорт ')#
    print('6 - Загрузить определённый транспорт ')#
    print('7 - Распределить грузы клиентов по транспортным средствам ')
    print('8 - Выйти из программы\n') #

    choice = input("Выберите пункт меню (1-5): ")
    if choice.isdigit() == True:
        choice = int(choice)
        if choice > 0 and choice < 9:
            pass
        else:
            print("Это неправильное число")
    else:
        print("Это не число!\n")
        menu()
    if choice == 1:
        add_transport_company()

    elif choice == 2:
        all_transport()

    elif choice == 3:
        all_clients()

    elif choice == 4:
        add_client()
    
    elif choice == 5:
        add_transport()

    elif choice == 6:
        load_transport()

    elif choice == 7:
        optimize_cargo()

    elif choice == 8:
        exit_program()


menu()