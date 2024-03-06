import os
import pandas as pd
import django
import psycopg2
from django.db import transaction
from datetime import datetime
import logging
import traceback

# Set up logging
logging.basicConfig(filename='upload_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "modal.settings")
django.setup()

from ap.models import Employee1

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'employee',
        'USER': 'postgres',
        'PASSWORD': '1234',
        'HOST': 'localhost',
        'PORT': '5433', 
    }
}

def upload_excel_to_database(file_path): 
    try: 
        df = pd.read_csv(file_path) 

        df['dob'] = df['dob'].astype(str) 
        df['date_joined'] = df['date_joined'].astype(str)
        df['created_at'] = df['created_at'].astype(str) 
        df['updated_at'] = df['updated_at'].astype(str) 
        # if not df['deleted_at'].isnull().all():
        #     df['deleted_at'] = df['deleted_at'].astype(str)

        data = df.to_dict(orient='records') 
        conn = psycopg2.connect( 
            dbname=DATABASES['default']['NAME'], 
            user=DATABASES['default']['USER'], 
            password=DATABASES['default']['PASSWORD'], 
            host=DATABASES['default']['HOST'], 
            port=DATABASES['default']['PORT']
        ) 

        logging.info("Connection established successfully.")

        with transaction.atomic(): 
            for row in data: 
                logging.info("entered loop")
                try:
                    if '/' in row['dob']:
                        row['dob'] = datetime.strptime(row['dob'], '%Y/%m/%d').date() 
                    else:
                        row['dob'] = datetime.strptime(row['dob'], '%Y-%m-%d').date()
                    logging.debug("Parsed dob: %s", row['dob'])

                    if '/' in row['date_joined']:
                        try: 
                            row['date_joined'] = datetime.strptime(row['date_joined'], '%Y/%m/%d %H:%M:%S')
                        except ValueError: 
                            row['date_joined'] = datetime.strptime(row['date_joined'], '%Y/%m/%d')
                    else:
                        row['date_joined'] = datetime.strptime(row['date_joined'], '%Y-%m-%d %H:%M:%S')
                    logging.debug("Parsed date_joined: %s", row['date_joined'])

                    if row['created_at'] and not pd.isnull(row['created_at']):
                        created_at_value = row['created_at'].split('.')[0]  
                        created_at_value = created_at_value.split('+')[0]  
                        row['created_at'] = datetime.strptime(created_at_value, '%Y-%m-%d %H:%M:%S')
                    logging.debug("Parsed created_at: %s", row['created_at'])

                    if row['updated_at'] and not pd.isnull(row['updated_at']):
                        updated_at_value = row['updated_at'].split('.')[0]  
                        updated_at_value = updated_at_value.split('+')[0]  
                        row['updated_at'] = datetime.strptime(updated_at_value, '%Y-%m-%d %H:%M:%S')
                    logging.debug("Parsed updated_at: %s", row['updated_at'])
                        
                    # if row['deleted_at'] and row['deleted_at'] != 'nan':
                    #     deleted_at_value = row['deleted_at'].split('.')[0]
                    #     deleted_at_value = deleted_at_value.split('+')[0]
                    #     row['deleted_at'] = datetime.strptime(deleted_at_value, '%Y-%m-%d %H:%M:%S')
                    # else:
                    #     row['deleted_at'] = None
                    # logging.debug("Parsed deleted_at: %s", row['deleted_at'])

                    # Use create method to create a new entry
                    obj = Employee1.objects.create(
                        id=row['id'],
                        password=row['password'],
                        last_login=row['last_login'],
                        is_superuser=row['is_superuser'],
                        email=row['email'],
                        username=row['username'],
                        first_name=row['first_name'],
                        last_name=row['last_name'],
                        EMP_code=row['EMP_code'],
                        is_active=row['is_active'],
                        is_staff=row['is_staff'],
                        branch_id=row['branch_id'],
                        dob=row['dob'],
                        date_joined=row['date_joined'],
                        father_name=row['father_name'],
                        mother_name=row['mother_name'],
                        gender=row['gender'],
                        address=row['address'],
                        phone=row['phone'],
                        mobile=row['mobile'],
                        hod=row['hod'],
                        created_at=row['created_at'],
                        updated_at=row['updated_at'],
                        city_id=row['city_id'],
                        country_id=row['country_id'],
                        department_id=row['department_id'],
                        designation_id=row['designation_id'],
                        state_id=row['state_id'],
                        user_role_id=row['user_role_id'],
                        user_type_id=row['user_type_id'],
                        pro_pic=row['pro_pic'],
                        dispatcher=row['dispatcher'],
                        status_id=row['status_id'],
                        fcm_token=row['fcm_token'],
                        middle_name=row['middle_name'],
                        secondary_mob_nos=row['secondary_mob_nos'],
                        ar_name=row['ar_name'],
                    )
                except ValueError as ve:
                    logging.error(f"Error parsing date: {ve} in row: {row}")
                except Exception as e:
                    logging.error(f"An error occurred: {e}")
                    logging.error(traceback.format_exc())
         
        conn.close() 

        return True, None   
    except Exception as e: 
        logging.error(f"Exception occurred: {e}")
        return False, str(e)   
   

if __name__ == "__main__": 
    excel_file_path = r'sss3.csv' 
     
    if os.path.exists(excel_file_path): 
        success, error_message = upload_excel_to_database(excel_file_path) 
        if success: 
            print("Excel data uploaded successfully!") 
        else:
            print(f"Failed to upload Excel data: {error_message}") 
    else: 
        print("Excel file not found.")
