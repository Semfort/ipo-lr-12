# Loel вар 2
print('start code...')
import transport

operations_count = 0
clients = []
transports = []
transport_companies = []

def add_transport_company():
    global operations_count
    print("=" * 30)
    name = input("Введите название транспортной компании: ")
    transport_companies.append(transport.TransportCompany(name))
    print("Транспортная компания добавлена")
    print("=" * 30)
    operations_count += 1
    menu()

def add_client():
    global operations_count
    print("=" * 30)
    name = input("Введите имя клиента: ")
    
    try:
        cargo_weight = float(input("Введите вес груза (в тоннах): "))
        if cargo_weight <= 0:
            print("Ошибка: Вес груза должен быть положительным!")
            menu()
            return
    except ValueError:
        print("Ошибка: Введите корректное число!")
        menu()
        return
    
    vip_input = input("VIP клиент? (1 - да/2 - нет): ")
    if vip_input == "1":
        is_vip = True
    elif vip_input == '2':
        is_vip = False
    else:
        print("Ошибка: Введите 1 или 2!")
        menu()
        return

    client = transport.Client(name, cargo_weight, is_vip)
    clients.append(client)
    print("Клиент добавлен")
    print("=" * 30)
    operations_count += 1
    menu()

def all_transport():
    global operations_count
    print("=" * 30)
    
    if not transports:
        print("Нет доступного транспорта")
    else:
        print("Весь транспорт:")
        for i, tr in enumerate(transports, 1):
            print(f"{i}. ID: {tr.vehicle_id}")
            print(f"   Тип: {type(tr).__name__}")
            print(f"   Грузоподъёмность: {tr.capacity} т")
            print(f"   Текущая загрузка: {tr.current_load} т")
            if hasattr(tr, 'clients_list') and tr.clients_list:
                print(f"   Загруженные клиенты: {[client.name for client in tr.clients_list]}")
            else:
                print("   Нет загруженных клиентов")
            print("-" * 20)
    
    print("=" * 30)
    operations_count += 1
    menu()

def all_clients():
    global operations_count
    print("=" * 30)
    
    if not clients:
        print("Нет клиентов")
    else:
        print("Все клиенты:")
        for i, cl in enumerate(clients, 1):
            vip_status = "VIP" if cl.is_vip else "не VIP"
            print(f"{i}. Имя: {cl.name}")
            print(f"   Вес груза: {cl.cargo_weight} т")
            print(f"   Статус: {vip_status}")
            print("-" * 20)
    
    print("=" * 30)
    operations_count += 1
    menu()

def add_transport():
    global operations_count
    print("=" * 30)
    
    print("Выберите тип транспорта:")
    print("1 - Корабль (Ship)")
    print("2 - Грузовик (Truck)")
    print("3 - Другой транспорт")
    
    choice = input("Ваш выбор (1-3): ")
    
    try:
        capacity = float(input("Введите грузоподъемность (в тоннах): "))
        if capacity <= 0:
            print("Ошибка: Грузоподъемность должна быть положительным числом!")
            menu()
            return
    except ValueError:
        print("Ошибка: Грузоподъемность должна быть числом!")
        menu()
        return
    
    if choice == "1":
        name = input("Введите название судна: ")
        tra = transport.Ship(capacity, name)
        transports.append(tra)
            
    elif choice == "2":
        color = input("Введите цвет грузовика: ")
        tra = transport.Truck(capacity, color)
        transports.append(tra)
            
    elif choice == "3":
        tra = transport.Vehicle(capacity)
        transports.append(tra)
    else:
        print("Ошибка: Введите число от 1 до 3!")
        menu()
        return
    
    print(f"Транспорт добавлен (ID: {tra.vehicle_id})")
    print("=" * 30)
    operations_count += 1
    menu()

def load_transport():
    global operations_count
    print("=" * 30)
    
    if not transports:
        print("Ошибка: Нет доступного транспорта!")
        menu()
        return
    
    if not clients:
        print("Ошибка: Нет клиентов!")
        menu()
        return
    
    print("Доступный транспорт:")
    for i, tr in enumerate(transports, 1):
        print(f"{i}. ID: {tr.vehicle_id},"
              f"Свободно: {tr.capacity - tr.current_load}/{tr.capacity} т")
    
    vehicle_id = input("\nВведите ID транспорта: ")
    
    for tr in transports:
        if str(tr.vehicle_id) == vehicle_id:
            found_transport = tr
            break
    
    if not found_transport:
        print("Ошибка: Транспорта с таким ID/номером не существует")
        menu()
        return
    
    print("\nДоступные клиенты:")
    for i, cl in enumerate(clients, 1):
        print(f"{i}. Имя: {cl.name}, Груз: {cl.cargo_weight} т")
    
    client_name = input("\nВведите имя клиента: ")
    
    for cl in clients:
        if cl.name == client_name:
            found_client = cl
            break
    
    if not found_client:
        print("Ошибка: Клиента с таким именем/номером не существует")
        menu()
        return
    
    try:
        success = found_transport.load_cargo(found_client)
        if success:
            print(f"Груз клиента '{found_client.name}' загружен на транспорт ID: {found_transport.vehicle_id}")
        else:
            print("Ошибка загрузки: недостаточно места или клиент уже загружен")
    except Exception as e:
        print(f"Ошибка при загрузке: {e}")
    
    print("=" * 30)
    operations_count += 1
    menu()

def optimize_cargo():
    global operations_count
    print("=" * 30)
    
    if not transport_companies:
        print("Ошибка: Сначала создайте транспортную компанию!")
        menu()
        return
    
    idc = input("Введите номер компании: ")
    try: 
        company = transport_companies[idc-1]
    except:
        print("Ошибка: Такого номера компании не существует")
        menu()
        return
    
    for client in clients:
        if client not in company.clients:
            company.clients.append(client)
    
    for vehicle in transports:
        if vehicle not in company.vehicles:
            company.vehicles.append(vehicle)
    
    company.optimize_cargo_distribution()
    print("Оптимизация завершена!")


    
    print("=" * 30)
    operations_count += 1
    menu()

def exit_program():
    global operations_count
    print("=" * 30)
    print(f"\nКоличество выполненных операций: {operations_count}")
    
    print("\nИтоговая статистика:")
    print(f"Клиентов: {len(clients)}")
    print(f"Транспортных средств: {len(transports)}")
    print(f"Транспортных компаний: {len(transport_companies)}")
    
    print('end code...')
    exit()

def menu():
    global operations_count
    print("\n" + "=" * 40)
    print("Статистика")
    print("=" * 40)
    
    if clients or transports or transport_companies:
        print(f"Клиенты: {len(clients)} | Транспорт: {len(transports)} | Компании: {len(transport_companies)}")
        print("-" * 40)
    
    print('1 - Создать транспортную компанию')
    print('2 - Вывести весь транспорт')
    print('3 - Вывести всех клиентов')
    print('4 - Создать клиента')
    print('5 - Добавить транспорт')
    print('6 - Загрузить определённый транспорт')
    print('7 - Распределить грузы клиентов по транспортным средствам')
    print('8 - Выйти из программы')
    print("=" * 40)
    
    choice = input("\nВыберите пункт меню (1-8): ")
    
    if choice.isdigit():
        choice = int(choice)
        if 1 <= choice <= 8:
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
        else:
            print("Ошибка: Введите число от 1 до 8!")
            menu()
    else:
        print("Ошибка: Введите число!")
        menu()

menu()