import tkinter as tk
from tkinter import ttk # библиотека для взаимодействия с таблицами в приложениях
import sqlite3


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        ''' Общее оформление приложения'''
        toolbar = tk.Frame(bg='#d7d8e0', bd=2) # настраиваем цвет и толщину полоски с кнопками
        toolbar.pack(side=tk.TOP, fill=tk.X) # указываем положение полоски с кнопками
        self.add_img = tk.PhotoImage(file='./img/add.png') # указываем путь к картинке для кнопок
        btn_open_dialog = tk.Button(toolbar, bg='#d7d8e0', bd=0, # создаем кнопку с картинкой
                                    image=self.add_img,
                                    command=self.open_dialog)
        btn_open_dialog.pack(side=tk.LEFT) # пакуем кнопку по левой стороне

        self.tree = ttk.Treeview(self, columns=['ID', 'name', 'tel', 'email', 'salary'],
                                heigh=45, show='headings') # указываем какие колонки содержит таблица, их высоту и способ отображения текста 

        self.tree.column('ID', width=30, anchor=tk.CENTER) # где названия колонок будут в таблице и их ширину
        self.tree.column('name', width=300, anchor=tk.CENTER)
        self.tree.column('tel', width=150, anchor=tk.CENTER)
        self.tree.column('email', width=150, anchor=tk.CENTER)
        self.tree.column('salary', width=90, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID') # указываем названия колонок, которые увидит пользователь
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='E-mail')
        self.tree.heading('salary', text='Зарплата')

        self.tree.pack(side=tk.LEFT) # пакуем таблицу по левой стороне, по верхней будет также

        self.update_img = tk.PhotoImage(file='img/update.png') # создаём кнопку редактирования
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0',
                                    bd = 0,image=self.update_img,
                                    command = self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file = 'img/delete.png') # создаём кнопку удаления
        btn_delete = tk.Button(toolbar, bg='#d7d8e0' , bd=0,
                               image=self.delete_img,
                               command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file = 'img/search.png') # создаём кнопку поиска
        btn_search = tk.Button(toolbar, bg='#d7d8e0' , bd=0,
                               image=self.search_img,
                               command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)
        
        self.refresh_img = tk.PhotoImage(file = 'img/refresh.png') # создаём кнопку обновления
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0' , bd=0,
                               image=self.refresh_img,
                               command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview) # ползунок справа
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def open_dialog(self):
        '''возможность открыть дочернее окно'''
        Child()
    
    def records(self, name, tel, email, salary):
        '''отображение записей'''
        self.db.insert_data(name, tel, email, salary)
        self.view_records()
        
    def view_records(self):
        '''моментальное обновление записей после изменений'''
        self.db.c.execute('''SELECT * FROM db''')
        [self.tree.delete(i) for i in self.tree.get_children()] # удаляем все записи из таблицы пользователя
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()] # вставляем заново все данные из бд в таблицу ползователя, включая новые
    
    def open_update_dialog(self): # вызов окна изменения
        Update()

    def update_record(self, name, tel, email, salary):
        '''запрос изменения'''
        self.db.conn.execute('''
        UPDATE db SET name=?, tel=?, email=?, salary=? WHERE ID=?''', (name, tel, email, salary,
        self.tree.set(self.tree.selection()[0], '#1'))) # взять из дерева первую строчку, а из неё первый элемент
        self.db.conn.commit()
        self.view_records()

    def delete_records(self):
        '''запрос удаления'''
        for selection_item in self.tree.selection():
            self.db.c.execute('''
            DELETE FROM db WHERE id=?''',(self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records() 

    def open_search_dialog(self):
        '''использование оформления и функционала окна поиска'''
        Search()

    def search_records(self, name):
        '''запрос поиска записи'''
        name = ('%' + name + '%')
        self.db.c.execute('''SELECT * FROM db WHERE name LIKE ?''', (name,))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

class Child(tk.Toplevel): # он наследует от Toplevel т.к он отвечает за создание дочернего окна
    def __init__(self):
        super().__init__()
        self.init_child()
        self.view = app

    def init_child(self):
        '''Оформление и функционал окна добавления'''
        self.title('Добавить')
        self.geometry('400x220')
        root.resizable(False, False)
        self.grab_set() # чтобы окно было на переднем плане
        self.focus_set() # чтобы нельзя было взаимодействовать с root в этот момент

        label_name = tk.Label(self, text='ФИО') # надписи, что именно ты вводишь
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='E-mail')
        label_sum.place(x=50, y=110)
        label_salary = tk.Label(self, text='Зарплата')
        label_salary.place(x=50, y=140)

        self.entry_name = ttk.Entry(self) # то куда ты вводишь
        self.entry_name.place(x=200, y=50)

        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x=200, y=140)

        self.button_cancel = ttk.Button(self, text='Закрыть', # кнопка закрыть
                                        command=self.destroy)
        self.button_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить') # кнопка подтвердить/добавить
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                       self.entry_email.get(),
                                                                       self.entry_tel.get(),
                                                                       self.entry_salary.get())) # связываем кнопку с добавлением данных в бд

class Update(Child): # нужно выделить запись для редактирования
    ''' Изменение данных '''
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()
    
    def init_edit(self):
        '''оформление кнопки редактирования'''
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event:
                    self.view.update_record(self.entry_name.get(),
                                            self.entry_email.get(),
                                            self.entry_tel.get(),
                                            self.entry_salary.get()))
        btn_edit.bind('<Button-1>', lambda event:
                      self.destroy(), add='+') # + даёт возможность использовать сразу несколько команд
        self.btn_ok.destroy() # убираем кнопку добавить
    
    def default_data(self):
        '''получение исходных данных для более удобного редактирования'''
        self.db.c.execute('''
        SELECT * FROM db WHERE id=?''', 
        (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row  = self.db.c.fetchone() # выделить ряд
        self.entry_name.insert(0, row[1])
        self.entry_tel.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])


class Search(tk.Toplevel):
    '''Создание поисковой системы'''
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app
    
    def init_search(self):
        ''' Оформление и функционал окна поиска'''
        self.title('Поиск') # настройка параметров окна
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск') # Создание надписи поиск
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self) # создание поля для ввода
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy) # создание кнопки закрыть
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск') # создание части кнопки подтверждения поиска
        btn_search.place(x=105, y=50) 
        btn_search.bind('<Button-1>', lambda event:
                         self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event:
                      self.destroy(), add='+')

class DB: 
    def __init__(self):
        self.conn = sqlite3.connect('db.db') # подключаемся к бд
        self.c = self.conn.cursor()
        self.c.execute(''' CREATE TABLE IF NOT EXISTS db (id integer primary key, name text, tel text, email text, salary int)''')
        self.conn.commit()
    
    def insert_data(self, name, tel, email, salary):
        '''Запрос на добавление данных в бд'''
        self.c.execute('''INSERT INTO db (name, tel, email, salary) VALUES (?, ?, ?, ?)''',(name, tel, email, salary)) 
        self.conn.commit()


'''создание корня приложения'''
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    root.geometry('750x450')
    root.resizable(False, False)
    root.mainloop()