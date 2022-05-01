
from flask import Flask, request, Response, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import datetime
from sqlalchemy import BigInteger, ForeignKey, PrimaryKeyConstraint
from .models import DB, Day, Appointment, Client


def create_app():

    APP = Flask(__name__)

    datelist = pd.date_range(start="2022-01-01",end="2022-12-31").to_pydatetime().tolist()

    APP.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mycrm.sqlite3'
    APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    DB.init_app(APP)
    @APP.before_first_request
    def create_tables():
        DB.create_all()

    @APP.route('/', methods=['GET','POST'])
    def root():
        # this route will present the user with choices for actions they can take next
    
        k = {'schedule': 'schedule_appointment', 'planner': 'planner', 'load': 'loaddb',
             'create client':'create_client', 'delete': 'delete_appointment',
             'remove': 'remove_client'}
        
        if request.method == 'POST':
            option = request.form.get('search')
            for key in k:
                if key in option.lower() or (option.lower() in key):
                    return redirect(url_for(k[key]))
                                                   
        return render_template('base1.html')



    @APP.route('/loaddb')
    def load_db():
        # this route will load 365 days into the empty database
        
        days = 'Sunday Monday Tuesday Wednesday Thursday Friday Saturday'.split()
        for i, x in enumerate(datelist):
            tmp = Day(id=i, date=str(x.month)+'/'+str(x.day), name=days[int(str(x.day))%7])
            # get a datetime and an int to create appointment for each day
            if not Day.query.get(tmp.id):
                DB.session.add(tmp)

        DB.session.commit()

        return 'datelist created'


    @APP.route('/create_client', methods=['GET', 'POST'])
    def create_client():
        """the create_client function will ask the user for an id, name, and age,
           so that a new client object may be created in the system"""

        if request.method == 'POST':
            
            # id is int
            id_x = request.form.get('search4')
            # name is str
            name_x = request.form.get('search5')
            # age is int
            age_x = request.form.get('search6')
            try:
                if not Client.query.get(int(id_x)):

                    new_client = Client(id=int(id_x), name=name_x, age=int(age_x))

                    DB.session.add(new_client)
                    
                    DB.session.commit()

                    return render_template('results3.html', answer=f'{new_client.name} added to database')
            except:
                return redirect(url_for('create_client'))

        return render_template('base3.html')

    @APP.route('/remove_client', methods=['GET', 'POST'])
    def remove_client():
        """this route will delete all appointments for a client before
           deleting the client profile"""

        if request.method == 'POST':

            old_client_id = request.form.get('search10')

            old_client = Client.query.get(int(old_client_id))

            if old_client:

                name = old_client.name
                for apt in old_client.appointments:
                    DB.session.delete(apt)

                DB.session.delete(old_client)

                DB.session.commit()

                return render_template('results5.html', answer=name)

        return render_template('base5.html')


    @APP.route('/check')
    def check():
        """this route allows one to check the occupancy of the Client and
           Appointment tables after loading, updating or clearing the database,
           and to ensure that the day objects have been created or deleted as
           expected"""
        
        
        end =  str([apt.id + ' ' + apt.day.date+' @ '+ str(apt.time)
        + (' with ' + apt.client.name or ' with Nobody') for apt in
        Appointment.query.all()]) + '  '+ str([d.date for d in Day.query.all()
        if d.date[-2:] == '13']) + '  |  Clients' + str([c.name for c in
        Client.query.all()])

        return end


    @APP.route('/delete_appointment', methods=['GET', 'POST'])
    def delete_appointment():
        # route to delete appointments by appointment id
 
        if request.method == 'POST':
            client_id = request.form.get('search7')

            apt_date = request.form.get('search8')

            apt_id = request.form.get('search9')

            appt = Appointment.query.get(apt_id)

            DB.session.delete(appt)

            DB.session.commit()

            return render_template('results4.html', answer='Appointment '+apt_id+' was removed')

        return render_template('base4.html')


    @APP.route('/schedule_appointment', methods=['GET', 'POST'])
    def schedule_appointment():
        """This route offers the ability to create new appointments for existing clients,
           currently the CRM accepts a day value for 1-365 to assign the date, an apt.
           time(int 9-6), and a client id(int)"""

        
        if request.method == 'POST':

            # enter day_id in mm/dd or mm-dd format
            day_id = request.form.get('search2')
            # apt_time will be entered as int 9-6 for now
            apt_time = request.form.get('search3')
            client_id_x = request.form.get('search35')
    
            # validate input
            if 5 > len(list(filter(lambda x: x.isdigit(), day_id))) >= 2:
                if any(b in day_id for b in '/- .'):
                    for x in '/- .':
                        if x in day_id:                                       
                            day_id = [int(j) for j in day_id.split(x)]

                            if 0 < day_id[0] < 13 or not 0 < day_id[1] <= 31:                              
                                m, d = day_id
                                value = 0

                                try:
                                    apt_time = int(apt_time)
                                    if not apt_time in [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]:
                                        raise Exception
                                    for ind, item in enumerate(datelist):
                                        
                                        if datetime.datetime(year=2022,month=m, day=d) == item:
                                            value = ind
                                            break
                                            
                                except Exception as ex_ception:
                                    print(str(ex_ception)+' was the exception')
                                    return redirect(url_for('schedule_appointment'))    
                                    
                            else:
                                return redirect(url_for('schedule_appointment'))
                else:                       
                    return redirect(url_for('schedule_appointment'))            
            else:
                return redirect(url_for('schedule_appointment'))

            if Day.query.get(value):
                my_day = Day.query.get(value)

                a_client = Client.query.get(int(client_id_x))

                if a_client:

                    # make sure an appointment is not already scheduled at that time on that day
                    
                    t = [a.time for a in my_day.appointments]
                    my = [a.time for a in a_client.appointments if a.day_id == my_day.id]
                    name = a_client.name
                    if not apt_time in t+my:

                        apt_id = ''.join(name[j] for j in range(len(name)) if not j % 2)[::-1] + ('$%'.join(
                                 list(str(client_id_x)[::-1]))) + str(len(Appointment.query.all()))

                        apt_x = Appointment(id=apt_id, day_id=my_day.id, time=apt_time, client_id=a_client.id)
                        my_day.appointments += [apt_x]
                        a_client.appointments += [apt_x]
                        DB.session.add(apt_x)
                        DB.session.commit()
                else:
                    print('Bad ID')
                    return redirect(url_for('schedule_appointment'))

                return render_template('results2.html', answer=str([i.id+': '+str(i.time)+' on '+i.day.date
                                                                    for i in a_client.appointments]))

                            
        return render_template('base.html')


    @APP.route('/refresh')
    def refresh():
        # wipe all data from Day, Client and Appointment tables
        
        DB.drop_all()
        DB.create_all()
        return 'Data has been refreshed.'


    @APP.route('/planner', methods=['GET', 'POST'])
    def planner():
        """this route asks the user for a range of dates entered in the form
           mm/dd - mm/dd, or optionally just one date mm/dd. returned is a 
           list of days matching the length of the data range, each date shows
           that it is free, or it will show its list of appointments"""

        if request.method == 'POST':
            day_range = request.form.get('search1')
            try:
                day_range = [c.split('/') for c in day_range.split('-')]
                a = lambda d: d.isdigit()
                day_range = [[int(''.join(filter(a, b))) for b in x] for x in day_range]
                values = []
                for day_id in day_range:
                    if 0 < day_id[0] < 13 or not 0 < day_id[1] <= 31:       
                        m, d = day_id
                    
                        for ind, item in enumerate(datelist):                                           
                            if datetime.datetime(year=2022,month=m, day=d) == item:                               
                                values += [ind]                                                                                                                             
                    else:
                        return redirect(url_for('planner'))
            except Exception as ex_ception:
                print(str(ex_ception)+' was the exception')

                return redirect(url_for('planner'))


                                    
            if len(values) == 2:
                r = list(range(values[0], values[1]+1))
            elif len(values) == 1:
                r = values

            else:
                return redirect(url_for('planner'))
            
            appts = []
            for day_id in r:
                if Day.query.get(day_id):
                    # primary keys for day are ints 1- 365
                    my_day = Day.query.get(day_id)
                    tmp = f'{my_day.name} {my_day.date}'
                    extra = []
                    print(my_day.name, my_day.date)
                    for apt in my_day.appointments:

                        extra += [str(apt.time)]
                    if extra:
                        appts += [tmp + ' @ ' + ', '.join(extra)]
                    else:
                        appts += [tmp+' - Free']
                

            return render_template('results.html', answer=' | '.join(appts))

        return render_template('base2.html')
        
            
    return APP



