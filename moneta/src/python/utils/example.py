# example of usage
import pool_manager as db

@db.re_request()
def request_example():
	query = '''select * from user'''
	with db.pool_manage().manage() as connect:
		cursor = connect.cursor()
		cursor.execute(query)
		return cursor.fetchall()

if __name__ == "__main__":
    print(request_example())


