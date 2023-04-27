import streamlit as st
import database as db
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "Your_api_uri"
mongo_client = MongoClient(uri)
mongo_db = mongo_client['ElectroStore']
devices_collection = mongo_db['devices']
conn = db.connect_db()


def login_user(login, password):
    client = db.select_client(conn, login, password)
    worker = db.select_worker(conn, login, password)
    if client:
        return 'client'
    elif worker:
        if worker[0][5] == 1:
            return 'admin'
        elif worker[0][5] == 2:
            return 'worker'
    else:
        return None


def main():
    db.create_tables(conn)
    st.sidebar.header('Вход в аккаунт')
    login = st.sidebar.text_input('Логин')
    password = st.sidebar.text_input('Пароль', type='password')
    entry_btn = st.sidebar.checkbox('Войти')
    if entry_btn:
        menu = login_user(login, password)
        if menu is None:
            st.error('Вы ввели неправильные данные')
        elif menu == 'client':
            current_client = db.select_client(conn, login, password)[0]
            client_id = current_client[0]
            st.subheader('Здравствуйте, ' + current_client[1])
            menu_choice = st.selectbox('Выберите меню', ['Каталог товаров', 'Список желаний', 'Корзина', 'Заказы'])
            if menu_choice == 'Каталог товаров':
                devices = db.select_devices(conn)
                selected_devices = pd.DataFrame(devices, columns=['id', 'device_name', 'device_type_id', 'company_id',
                                                                  'remainder'])
                companies = db.select_companies(conn)
                col1, col2 = st.columns(2)
                with col1:
                    device_type = st.selectbox('Тип устройства', ['Все', 'Телефон', 'Планшет', 'Ноутбук'])
                    if device_type == 'Телефон':
                        selected_devices = selected_devices[selected_devices['device_type_id'] == 1]
                    elif device_type == 'Планшет':
                        selected_devices = selected_devices[selected_devices['device_type_id'] == 2]
                    elif device_type == 'Ноутбук':
                        selected_devices = selected_devices[selected_devices['device_type_id'] == 3]
                with col2:
                    company = st.selectbox('Компания устройства', ['Все', 'Apple', 'Google', 'Samsung', 'Xiaomi'])
                    if company == 'Apple':
                        selected_devices = selected_devices[selected_devices['company_id'] == 1]
                    elif company == 'Google':
                        selected_devices = selected_devices[selected_devices['company_id'] == 2]
                    elif company == 'Samsung':
                        selected_devices = selected_devices[selected_devices['company_id'] == 3]
                    elif company == 'Xiaomi':
                        selected_devices = selected_devices[selected_devices['company_id'] == 4]
                for ind, device in selected_devices.iterrows():
                    with st.container():
                        device_id = device[0]
                        device_remainder = int(device[4])
                        st.text(f'Компания: {companies[device[3] - 1][1]}')
                        st.text(f'Название устройства: {device[1]}')
                        device_char = devices_collection.find_one({"model": device[1]})
                        st.text(f'Размер экрана: {device_char["screenSize"]}')
                        st.text(f'Разрешение экрана: {device_char["screenResolution"]}')
                        st.text(f'Тип экрана: {device_char["screenType"]}')
                        st.text(f'Вес: {device_char["weight"]}')
                        st.text(f'Процессор: {device_char["processor"]}')
                        st.text(f'Операционная система: {device_char["operatingSystem"]}')
                        st.text(f'Остаток на складе: {device_remainder}')
                        wish_btn, cart_btn = st.columns(2)
                        wish_btn_key = '1' + device[1]
                        cart_btn_key = '2' + device[1]
                        with wish_btn:
                            if st.button('В список желаний', key=wish_btn_key):
                                if db.select_wish_list_item(conn, client_id, device_id):
                                    st.error('Данное устройство уже есть в вашем списке желаний')
                                else:
                                    if db.insert_wish_list_item(conn, client_id, device_id):
                                        st.success('Устройство добавлено')
                                    else:
                                        st.error('Ошибка добавления')
                        with cart_btn:
                            if st.button('В корзину', key=cart_btn_key):
                                if db.select_cart_list_item(conn, client_id, device_id):
                                    st.error('Данное устройство уже есть в корзине')
                                else:
                                    if db.insert_cart_list_item(conn, client_id, device_id):
                                        st.success('Устройство добавлено в корзину')
                                    else:
                                        st.error('Ошибка добавления')
            elif menu_choice == 'Список желаний':
                wish_list_items = db.select_wish_list_items(conn, client_id)
                companies = db.select_companies(conn)
                for item in wish_list_items:
                    device_id = item[2]
                    device = db.select_device(conn, device_id)
                    device_remainder = int(device[0][4])
                    with st.container():
                        st.text(f'Компания: {companies[device[0][3] - 1][1]}')
                        st.text(f'Название устройства: {device[0][1]}')
                        device_char = devices_collection.find_one({"model": device[0][1]})
                        st.text(f'Размер экрана: {device_char["screenSize"]}')
                        st.text(f'Разрешение экрана: {device_char["screenResolution"]}')
                        st.text(f'Тип экрана: {device_char["screenType"]}')
                        st.text(f'Вес: {device_char["weight"]}')
                        st.text(f'Процессор: {device_char["processor"]}')
                        st.text(f'Операционная система: {device_char["operatingSystem"]}')
                        st.text(f'Остаток на складе: {device_remainder}')
                        wish_btn, cart_btn = st.columns(2)
                        wish_btn_key = '3' + device[0][1]
                        cart_btn_key = '4' + device[0][1]
                        with wish_btn:
                            if st.button('Удалить из списка желаний', key=wish_btn_key):
                                if db.delete_wish_list_item(conn, client_id, device_id):
                                    st._rerun()
                        with cart_btn:
                            if st.button('В корзину', key=cart_btn_key):
                                if db.select_cart_list_item(conn, client_id, device_id):
                                    st.error('Данное устройство уже есть в корзине')
                                else:
                                    if db.insert_cart_list_item(conn, client_id, device_id):
                                        st.success('Устройство добавлено в корзину')
                                    else:
                                        st.error('Ошибка добавления')
            elif menu_choice == 'Корзина':
                cart_list_items = db.select_cart_list_items(conn, str(client_id))
                companies = db.select_companies(conn)
                for item in cart_list_items:
                    device_id = item[2]
                    device = db.select_device(conn, str(device_id))[0]
                    device_remainder = int(device[4])
                    with st.container():
                        st.text(f'Компания: {companies[device[3] - 1][1]}')
                        st.text(f'Название устройства: {device[1]}')
                        st.text(f'Остаток на складе: {device_remainder}')
                        confirm_btn, del_btn = st.columns(2)
                        confirm_btn_key = '5' + device[1]
                        del_btn_key = '6' + device[1]
                        with confirm_btn:
                            if st.button('Подтвердить заказ', key=confirm_btn_key):
                                if device_remainder > 0:
                                    if db.insert_reservation(conn, client_id, device_id, 1) and \
                                            db.delete_cart_list_item(conn, client_id, device_id):
                                        db.set_device_remainder(conn, device_remainder - 1, device_id)
                                        st._rerun()
                                else:
                                    st.error('Недостаточно товара')
                        with del_btn:
                            if st.button('Удалить из корзины', key=del_btn_key):
                                if db.delete_cart_list_item(conn, client_id, device_id):
                                    st._rerun()
            elif menu_choice == 'Заказы':
                client_reservations = db.select_client_reservations(conn, str(client_id), 1)
                companies = db.select_companies(conn)
                for item in client_reservations:
                    device_id = item[2]
                    reservation_id = item[0]
                    device = db.select_device(conn, str(device_id))[0]
                    device_remainder = device[4]
                    with st.container():
                        st.text(f'Компания: {companies[device[3] - 1][1]}')
                        st.text(f'Название устройства: {device[1]}')
                        cancel_btn_key = '7' + device[1]
                        if st.button('Отменить заказ', key=cancel_btn_key):
                            db.set_reservation_status(conn, reservation_id, 4)
                            db.set_device_remainder(conn, device_remainder + 1, device_id)
                            st._rerun()
        elif menu == 'worker':
            current_worker = db.select_worker(conn, login, password)[0]
            worker_id = current_worker[0]
            status_choice = st.selectbox('Статус заказа', ['Новые', 'Собранные', 'Выданные', 'Отмененные'])
            reservations = db.select_reservations(conn)
            companies = db.select_companies(conn)
            df_reservations = pd.DataFrame(reservations, columns=['id', 'client_id', 'device_id', 'status_id',
                                                                  'worker_id'])
            common_btn_name = ''
            if status_choice == 'Новые':
                df_reservations = df_reservations[df_reservations['status_id'] == 1]
                common_btn_name = 'Собрать'
            elif status_choice == 'Собранные':
                df_reservations = df_reservations[df_reservations['status_id'] == 2]
                common_btn_name = 'Выдать'
            elif status_choice == 'Выданные':
                df_reservations = df_reservations[df_reservations['status_id'] == 3]
                common_btn_name = 'Удалить'
            elif status_choice == 'Отмененные':
                df_reservations = df_reservations[df_reservations['status_id'] == 4]
                common_btn_name = 'Удалить'
            for item in df_reservations.iterrows():
                reservation = item[1]
                reservation_client = db.select_client_by_id(conn, reservation[1])
                device_id = reservation[2]
                reservation_id = reservation[0]
                device = db.select_device(conn, str(device_id))[0]
                device_remainder = int(device[4])
                with st.container():
                    st.text(f'Компания: {companies[device[3] - 1][1]}')
                    st.text(f'Название устройства: {device[1]}')
                    st.text(f'Имя клиента: {reservation_client[1]}')
                    st.text(f'Телефон клиента: {reservation_client[4]}')
                    common_btn_key = '8' + device[1]
                    cancel_btn_key = '9' + device[1]
                    common_btn, cancel_btn = st.columns(2)
                    with common_btn:
                        if st.button(common_btn_name, key=common_btn_key):
                            if common_btn_name == 'Собрать':
                                db.set_reservation_worker(conn, reservation_id, worker_id)
                                db.set_reservation_status(conn, reservation_id, 2)
                                st._rerun()
                            elif common_btn_name == 'Выдать':
                                db.set_reservation_status(conn, reservation_id, 3)
                                st._rerun()
                            elif common_btn_name == 'Удалить':
                                db.delete_reservation(conn, reservation_id)
                                st._rerun()
                    with cancel_btn:
                        if st.button('Отменить заказ', key=cancel_btn_key):
                            db.set_reservation_status(conn, reservation_id, 4)
                            db.set_device_remainder(conn, device_remainder + 1, device_id)
                            st._rerun()
        elif menu == 'admin':
            st.title('Меню Админа')
            admin_choice = st.selectbox('Выберите меню', ['Товары', 'Работники'])
            if admin_choice == 'Товары':
                devices = db.select_devices(conn)
                selected_devices = pd.DataFrame(devices, columns=['id', 'device_name', 'device_type_id', 'company_id',
                                                                  'remainder'])
                companies = db.select_companies(conn)
                col1, col2 = st.columns(2)
                with col1:
                    device_type = st.selectbox('Тип устройства', ['Все', 'Телефон', 'Планшет', 'Ноутбук'])
                    if device_type == 'Телефон':
                        selected_devices = selected_devices[selected_devices['device_type_id'] == 1]
                    elif device_type == 'Планшет':
                        selected_devices = selected_devices[selected_devices['device_type_id'] == 2]
                    elif device_type == 'Ноутбук':
                        selected_devices = selected_devices[selected_devices['device_type_id'] == 3]
                with col2:
                    company = st.selectbox('Компания устройства', ['Все', 'Apple', 'Google', 'Samsung', 'Xiaomi'])
                    if company == 'Apple':
                        selected_devices = selected_devices[selected_devices['company_id'] == 1]
                    elif company == 'Google':
                        selected_devices = selected_devices[selected_devices['company_id'] == 2]
                    elif company == 'Samsung':
                        selected_devices = selected_devices[selected_devices['company_id'] == 3]
                    elif company == 'Xiaomi':
                        selected_devices = selected_devices[selected_devices['company_id'] == 4]
                for ind, device in selected_devices.iterrows():
                    with st.container():
                        device_id = device[0]
                        device_remainder = int(device[4])
                        st.text(f'Компания: {companies[device[3] - 1][1]}')
                        st.text(f'Название устройства: {device[1]}')
                        device_char = devices_collection.find_one({"model": device[1]})
                        st.text(f'Размер экрана: {device_char["screenSize"]}')
                        st.text(f'Разрешение экрана: {device_char["screenResolution"]}')
                        st.text(f'Тип экрана: {device_char["screenType"]}')
                        st.text(f'Вес: {device_char["weight"]}')
                        st.text(f'Процессор: {device_char["processor"]}')
                        st.text(f'Операционная система: {device_char["operatingSystem"]}')
                        st.text(f'Остаток на складе: {device_remainder}')
                        add_dev_btn, rem_dev_btn, del_dev_btn = st.columns(3)
                        add_dev_btn_key = '1' + device[1]
                        rem_dev_btn_key = '2' + device[1]
                        del_dev_btn_key = '3' + device[1]
                        with add_dev_btn:
                            if st.button('Добавить', key=add_dev_btn_key):
                                db.set_device_remainder(conn, device_remainder + 1, device_id)
                                st._rerun()
                        with rem_dev_btn:
                            if st.button('Убавить', key=rem_dev_btn_key):
                                if device_remainder > 0:
                                    db.set_device_remainder(conn, device_remainder - 1, device_id)
                                    st._rerun()
                                else:
                                    st.error('Устройства уже нет на складе')
                        with del_dev_btn:
                            if st.button('Удалить устройство', key=del_dev_btn_key):
                                db.delete_device(conn, device_id)
            elif admin_choice == 'Работники':
                with st.form(key='new_worker', clear_on_submit=True):
                    st.subheader('Создание нового аккаунта работника')
                    worker_name = st.text_input("Имя")
                    worker_login = st.text_input('Логин')
                    worker_password = st.text_input('Пароль')
                    worker_phone = st.text_input('Телефон')
                    role_id = 2
                    signup_btn = st.form_submit_button('Создать нового работника')
                    if signup_btn:
                        db.insert_worker(conn, worker_name, worker_login, worker_password, worker_phone, role_id)
    else:
        st.title('Магазин электротехники')
        st.markdown('Добро пожаловать в наш магазин!')
        st.markdown('Для пользования приложением вам необходимо авторизоваться в систему. '
                    'Если вы еще не имеете аккаунт, то вам необходимо зарегистрироваться в контекстном меню, '
                    'расположенном в нижней часте меню.')
        st.subheader('Регистрация')
        st.text('Введите ваши данные')
        with st.form(key='signup', clear_on_submit=True):
            client_name = st.text_input("Имя")
            client_phone = st.text_input('Телефон')
            client_login = st.text_input('Логин')
            client_password = st.text_input('Пароль')
            signup_btn = st.form_submit_button('Зарегистрироваться')
            if signup_btn:
                if db.insert_client(conn, client_name, client_phone, client_login, client_password):
                    st.success('Аккаунт успешно создан')
                else:
                    st.error('Не удалось создать аккаунт')
        st.markdown('Данные для связи:')
        st.markdown('Email: electro_store@mail.ru')
        st.markdown('Телефон: 8-800-555-3535')


if __name__ == '__main__':
    main()
