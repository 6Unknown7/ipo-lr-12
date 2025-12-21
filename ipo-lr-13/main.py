from transport import Client, Truck, Train, TransportCompany


def console_main():
    # Существующий консольный интерфейс (не изменён, используется как fallback)
    company = TransportCompany("Быстрая Доставка")
    while True:
        print("\n" + "=" * 50)
        print("МЕНЮ ТРАНСПОРТНОЙ КОМПАНИИ")
        print("=" * 50)
        print("1. Добавить транспортное средство")
        print("2. Добавить клиента")
        print("3. Показать все транспортные средства")
        print("4. Показать всех клиентов")
        print("5. Распределить грузы оптимально")
        print("6. Показать отчет о распределении")
        print("0. Выход")
        choice = input("\nВыберите действие: ")
        if choice == "0":
            print("До свидания!")
            break
        print("Выбран пункт консольного меню. Запустите GUI для удобства.")


if __name__ == "__main__":
    # Попытка запустить GUI (PyQt6). При отсутствии — откат на консольный режим.
    try:
        from gui import run_app
        run_app()
    except Exception as e:
        print(f"Не удалось запустить GUI (PyQt6). Ошибка: {e}\nЗапускается консольный интерфейс...")
        console_main()
