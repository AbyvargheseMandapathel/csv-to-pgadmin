from main import CSVXLToPostgres

loader = CSVXLToPostgres(
    file='sss3.csv', 
    table='ap_employee',     
    host='localhost',   
    database='employee', 
    username='postgres',  
    password='1234',
    port = "5433",  
)

loader.load_to_db()
