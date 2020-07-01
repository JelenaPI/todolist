from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()

class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='NULL')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

class ToDoList():

    def menu(self):
        user_input = ''
        while user_input != '0':
            print('''1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit''')
            user_input = input()
            if user_input == '6':
                self.delete_task()

            if user_input == '4':
                self.missed_tasks()

            if user_input == '5':
                self.add_task()

            if user_input == '3':
                self.all_tasks()

            if user_input == '2':
                self.week_s_tasks()

            if user_input == '1':
                self.today_s_tasks()
        print('')
        print('Bye!')

    def add_task(self):
        new_task=Table(task=input('\nEnter task\n'), deadline=datetime.strptime(input('Enter deadline\n'), '%Y-%m-%d'))
        session.add(new_task)
        session.commit()
        print('The task has been added!\n')

    def today_s_tasks(self):
        today=datetime.today().strftime('%Y-%m-%d')
        rows = session.query(Table).filter(Table.deadline == today).all()
        print('\nToday '+datetime.today().strftime('%d %b')+':')
        if len(rows) == 0:
            print('Nothing to do!\n')
        else:
            for i in range(len(rows)):
                if i == len(rows)-1:
                    print(str(i+1)+'. '+rows[i].task+'\n')
                else:
                    print(str(i+1)+'. '+rows[i].task)

    def week_s_tasks(self):
        for k in range (7):
            rows = session.query(Table).filter(Table.deadline == (datetime.today()+timedelta(days=k)).date()).all()
            print('\n'+str((datetime.today()+timedelta(days=k)).strftime('%A %d %b')) +':')
            if len(rows) == 0:
                print('Nothing to do!')
            else:
                for order, row in enumerate(rows):
                    print(order + 1, row.task, sep='. ')
        print('')

    def all_tasks(self):
        print('All tasks:')
        rows = session.query(Table).order_by(Table.deadline).all()
        if len(rows) == 0:
            print('Nothing to do!\n')
        else:
            for i in range(len(rows)):
                print(str(i+1)+'. '+rows[i].task+'. '+rows[i].deadline.strftime('%d %b'))
            print('')

    def delete_task(self):
        print('\nChose the number of the task you want to delete:')
        rows = session.query(Table).all()
        if len(rows) == 0:
            print('Nothing to do!\n')
        else:
            for i in range(len(rows)):
                print(str(i+1)+'. '+rows[i].task+'. '+rows[i].deadline.strftime('%d %b'))
        session.delete(rows[int(input())-1])
        session.commit()
        print('The task has been deleted!\n')

    def missed_tasks(self):
        print('\nMissed tasks:')
        rows = session.query(Table).filter(Table.deadline < datetime.today()-timedelta(hours=23)).all()
        if len(rows) == 0:
            print('Nothing is missed!')
        else:
            for order, row in enumerate(rows):
                print(order + 1, row.task,row.deadline.strftime('%d %b'), sep='. ')
        print('')

program = ToDoList()
program.menu()
