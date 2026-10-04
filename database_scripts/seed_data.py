import os
import sys
import re
from datetime import datetime
from sqlalchemy.orm import Session
from backend.database.session import engine, init_db, SessionLocal
from backend.database.models import User, Department, Club, Staff, Event, StudentResult
from backend.auth.security import get_password_hash

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

def seed_database():
    print("[*] Initializing database tables in XAMPP MySQL (database: sacas)...")
    init_db()
    db: Session = SessionLocal()

    try:
        # 1. Departments
        if db.query(Department).count() == 0:
            print("[+] Seeding Departments...")
            departments_data = [
                Department(department_id=1, name='B.Sc. Computer Science with Data Science', url='https://sacas.ac.in/departments/bsc-computer-science-data-science'),
                Department(department_id=2, name='B.Sc. Computer Science with Artificial Intelligence', url='https://sacas.ac.in/departments/bsc-computer-science-ai'),
                Department(department_id=3, name='B.Sc. Computer Science', url='https://sacas.ac.in/departments/bsc-computer-science'),
            ]
            db.add_all(departments_data)
            db.commit()

        # 2. Clubs
        if db.query(Club).count() == 0:
            print("[+] Seeding Clubs...")
            clubs_data = [
                Club(club_id=1, name='Exnora Club', parent_body='Environmental Extension Cell / Student Affairs'),
                Club(club_id=2, name='Rotaract Club', parent_body='Rotaract Club / General College Extension Cell'),
            ]
            db.add_all(clubs_data)
            db.commit()

        # 3. Staff
        if db.query(Staff).count() == 0:
            print("[+] Seeding Staff...")
            staff_data = [
                Staff(department_id=1, name='Mr. Krishnan. R', role='Head of the Department', email='bscdshod@sacas.ac.in', phone='9444578024', qualification='M. Sc., M. Phil., NET, SET'),
                Staff(department_id=1, name='Mrs. Anuradha P', role='Assistant Professor', email='anuradhap@sacas.ac.in', phone='9940297135', qualification='M. Sc., M. Phil., NET'),
                Staff(department_id=1, name='Mrs.C. Ranjani', role='Assistant Professor', email='ranjanic@sacas.ac.in', phone='8098370004', qualification='M. Sc.(IT), M. Phil., NET, SET'),
                Staff(department_id=1, name='Mr.S.Mahendran', role='Assistant Professor', email=None, phone=None, qualification='M.C.A., M.Phil., SET, NET'),
                Staff(department_id=2, name='Mr. Krishnan. R', role='Head of the Department', email='bscaihod@sacas.ac.in', phone='9444578024', qualification='M. Sc., M. Phil., NET, SET'),
                Staff(department_id=2, name='Mrs. Anuradha P', role='Assistant Professor', email='anuradhap@sacas.ac.in', phone='9940297135', qualification='M. Sc., M. Phil., NET'),
                Staff(department_id=2, name='Mrs.C. Ranjani', role='Assistant Professor', email='ranjanic@sacas.ac.in', phone='8098370004', qualification='M. Sc.(IT), M. Phil., NET, SET'),
                Staff(department_id=2, name='Mr.S.Mahendran', role='Assistant Professor', email=None, phone=None, qualification='M.C.A., M.Phil., SET, NET'),
                Staff(department_id=3, name='Dr. M. Thirunavukkarasu', role='Head of the Department', email='bsccshod@sacas.ac.in', phone='9941046922', qualification='M.Sc., M. Phil., Ph. D'),
                Staff(department_id=3, name='Mr. P. Chandrasekar', role='Assistant Professor', email='chandrasekarp@sacas.ac.in', phone='9841450690', qualification='M.C.A., M. Phil., (Ph. D) NET.'),
                Staff(department_id=3, name='Mrs. T. Shunmugavadivoo', role='Assistant Professor', email='shunmugavadivoot@sacas.ac.in', phone='9894027638', qualification='M.C.A., M. Phil., (Ph. D) NET.'),
                Staff(department_id=3, name='Mrs. C. Sangeetha', role='Assistant Professor', email='sangeethac@sacas.ac.in', phone='8778443561', qualification='MCA, M.Phil., (Ph.D.,)'),
                Staff(department_id=3, name='Mr.Gunaseelan C', role='Assistant Professor', email='gunaseelanc@sacas.ac.in', phone='9940111214', qualification='MCA, NET,(Ph.D.,)'),
                Staff(department_id=3, name='Ms. Saranya A', role='Assistant Professor', email='saranyaa@sacas.ac.in', phone='9361955814', qualification='M.C.A.'),
                Staff(department_id=3, name='Mrs.N.Nandhini', role='Assistant Professor', email=None, phone=None, qualification='M.Sc., M.Phil., NET., M. Tech'),
                Staff(department_id=3, name='Dr.K.Jamberi', role='Associate Professor & Head', email=None, phone=None, qualification='MCA., M.Phil, SET, M.Sc (Psy), B.Ed., Ph.D.Post Doc'),
                Staff(department_id=3, name='Mrs.C.Sathia Jeya', role='Associate Professor', email=None, phone=None, qualification='MCA., M.Phil., (Ph.D)'),
                Staff(department_id=3, name='Mrs.M.Vijayarani', role='Associate Professor', email=None, phone=None, qualification='MCA., M.Phil., (Ph.D)'),
                Staff(department_id=3, name='Mr.Bursu Madhu', role='Assistant Professor', email=None, phone=None, qualification='M.C.A.'),
            ]
            db.add_all(staff_data)
            db.commit()

        # 4. Events
        if db.query(Event).count() == 0:
            print("[+] Seeding Events...")
            events_data = [
                Event(department_id=1, club_id=None, title='SYNAPSE 2026', event_date=datetime.strptime('2026-07-24', '%Y-%m-%d').date(), venue='SACAS Preview Theatre', description='Guest lecture on The Synapse between Data and Intelligence, freshers welcome, and Council Inauguration.', url='https://sacas.ac.in/events/department-of-computer-science-with-artificial-intelligence-data-science-in-association-with-iqac-s-a-college-of-arts-science-successfully-organized-synapse-2026-on-24-07-2026'),
                Event(department_id=2, club_id=None, title='NOVAZEN’26 Inter-Collegiate Technical Symposium', event_date=datetime.strptime('2026-03-05', '%Y-%m-%d').date(), venue='Campus Premises', description='Symposium featuring five technical competitions and two non-technical events with 280 participants.', url='https://sacas.ac.in/events/department-of-computer-science-with-artificial-intelligence-of-s-a-college-of-arts-science-organized-novazen26-an-inter-collegiate-technical-symposium-on-05-03-2026'),
                Event(department_id=3, club_id=None, title='Farewell 2026', event_date=datetime.strptime('2026-04-10', '%Y-%m-%d').date(), venue='SACAS Canteen', description='Heartfelt farewell programme to bid adieu to the outgoing batch of B.Sc. Computer Science.', url='https://sacas.ac.in/events/department-of-computer-science-at-s-a-college-of-arts-science-organized-a-heartfelt-farewell-programme-farewell-2026-on-10-04-2026'),
                Event(department_id=None, club_id=1, title='Rocket Formation – World Records Union', event_date=datetime.strptime('2022-11-25', '%Y-%m-%d').date(), venue='Campus Ground', description='Largest human image of rocket with 1000 student participants, recognized by World Records Union.', url='https://sacas.ac.in/events/rocket-formation-world-records-union'),
                Event(department_id=None, club_id=1, title='Mass Cleaning Activity In Avadi Paruthipattu Lake', event_date=datetime.strptime('2022-07-23', '%Y-%m-%d').date(), venue='Avadi Paruthipattu Lake', description='Mass cleaning activity in Avadi Lake under guidance of Minister S.M. Nasar.', url='https://sacas.ac.in/events/mass-cleaning-activity-in-avadi-paruthipattu-lake'),
                Event(department_id=None, club_id=2, title='Happiness Sharing Programme at Carmel Centre', event_date=datetime.strptime('2026-06-09', '%Y-%m-%d').date(), venue='Carmel Centre', description='Spreading joy and distributing toys to differently abled special children.', url='https://sacas.ac.in/events/the-rotaract-club-and-unnat-bharat-abhiyan-uba-of-s-a-college-of-arts-science-organized-a-happiness-sharing-programme-at-carmel-centre-for-the-differently-abled-on-09-06-2026'),
                Event(department_id=None, club_id=2, title='Large-Scale Cleanup Drive at Pulicat Islands', event_date=datetime.strptime('2026-06-06', '%Y-%m-%d').date(), venue='Pulicat Islands', description='World Environment Day cleanup collecting plastic waste in collaboration with Bisleri.', url='https://sacas.ac.in/events/sacass-large-scale-cleanup-drive-held-in-pulicat-islands-for-world-environment-day-on-06-06-2026'),
                Event(department_id=3, club_id=2, title='Madras Day Celebration with Spectacular Human Formation', event_date=datetime.strptime('2023-08-22', '%Y-%m-%d').date(), venue='College Ground', description='Intricate human formation forming "Happy Madras Day" by Rotaract and Computer Science students.', url='https://sacas.ac.in/events/madras-day-celebration-with-spectacular-human-formation-on-22-08-2023'),
            ]
            db.add_all(events_data)
            db.commit()

        # 5. Student Results
        if db.query(StudentResult).count() == 0:
            print("[+] Seeding Student Results from init.sql...")
            init_sql_path = os.path.join(os.path.dirname(__file__), "init.sql")
            with open(init_sql_path, "r", encoding="utf-8") as f:
                content = f.read()

            values_match = re.search(r"INSERT INTO student_result\s*\([^)]+\)\s*VALUES\s*(.+);", content, re.DOTALL | re.IGNORECASE)
            if values_match:
                raw_values = values_match.group(1).strip()
                row_pattern = re.findall(r"\(([^)]+)\)", raw_values)
                for row in row_pattern:
                    parts = [p.strip().strip("'") for p in row.split(",")]
                    s_no = int(parts[0])
                    reg_no = int(parts[1])
                    dept_id = int(parts[2])
                    name = parts[3]
                    dob_str = parts[4]
                    dob_val = datetime.strptime(dob_str, "%Y-%m-%d").date()
                    p_prac = int(parts[5])
                    tam = int(parts[6])
                    eng = int(parts[7])
                    py = int(parts[8])
                    off = int(parts[9])
                    naan = int(parts[10])
                    tot = int(parts[11])
                    pct = float(parts[12])
                    rnk = int(parts[13])

                    sr = StudentResult(
                        s_no=s_no,
                        register_number=reg_no,
                        department_id=dept_id,
                        name=name,
                        dob=dob_val,
                        python_practical=p_prac,
                        tamil=tam,
                        english=eng,
                        python=py,
                        office_automation=off,
                        naan_mudhalvan=naan,
                        main_total=tot,
                        percentage=pct,
                        rank=rnk
                    )
                    db.add(sr)
                db.commit()
                print(f"[+] Loaded {len(row_pattern)} student academic records.")

        # 6. User Accounts (Default password 123456)
        if db.query(User).count() == 0:
            print("[+] Generating User Accounts from Student Results (Default Password: '123456')...")
            students = db.query(StudentResult).all()
            student_hash = get_password_hash("123456")
            for s in students:
                user = User(
                    username=str(s.register_number),
                    hashed_password=student_hash,
                    role="student",
                    register_number=s.register_number,
                    full_name=s.name,
                    email=f"{s.register_number}@student.sacas.ac.in"
                )
                db.add(user)

            admin_user = User(
                username="admin",
                hashed_password=get_password_hash("admin123"),
                role="admin",
                register_number=None,
                full_name="College Administrator",
                email="admin@sacas.ac.in"
            )
            db.add(admin_user)
            db.commit()
            print(f"[+] Created {len(students)} Student Accounts and Administrator Account.")

        print("\n[SUCCESS] XAMPP MySQL database 'sacas' is fully seeded and ready!")
    except Exception as e:
        db.rollback()
        print(f"[ERROR] Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
