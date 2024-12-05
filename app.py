from flask import Flask, render_template, request, flash, url_for, redirect
import mysql.connector
from mysql.connector import errorcode

#refer to third midterm project to change variables
app = Flask(__name__)
app.config["DEBUG"] = True
app.config["SECRET_KEY"] = 'your secret key'
app.secret_key = 'your secret key'

def get_db_connection():
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user = "root",
            password = "root",
            port = "6603",
            database = "sakila_db"
        )
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your username or password.")
            exit()
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist.")
            exit()
        else:
            print(err)
            print("ERROR: Service not available")
            exit()
    return mydb

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

##root route
@app.route('/', methods=('GET',))
def home_navigation_get():
    return render_template('index.html')

@app.route('/', methods=('POST',))
def home_navigation_post():
    option = request.form.get('routes')

    if option == "home":
        return redirect(url_for('index'))
    elif option == 'rental':
        return redirect(url_for('rental-reports'))
    elif option == 'customers':
        return redirect(url_for('customer-reports'))
    elif option == 'inventory':
        return redirect(url_for('inventory-reports'))
    
@app.route('/rental_reports', methods=('GET',))
def rental_route():
    return render_template('rental.html')

@app.route('/rental_reports', methods=('POST',))
def rental_reports():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)

    option = request.form.get('rentals')

    if (option == "View Monthly Sales"):
        query_one = '''
        Create VIEW monthlyRentalSales AS 
        SELECT YEAR(p.payment_date) AS "YEAR", MONTH(p.payment_date) AS "MONTH", SUM(p.amount) AS "TotalPayments"
        FROM payment p
        JOIN rental r ON r.rental_id = p.rental_id
        GROUP BY YEAR(p.payment_date), MONTH(p.payment_date) 
        ORDER BY YEAR(p.payment_date) ASC, MONTH(p.payment_date) ASC;
    '''
    cursor.execute(query_one)
    query_one_result = cursor.fetchall()

    if (option == "View Sales by Category"):  
        query_two = '''
    CREATE VIEW categoryTotals AS 
    SELECT YEAR(p.payment_date) AS "YEAR", c.name, SUM(p.amount)
    FROM payment p
    JOIN rental r ON r.rental_id = p.rental_id
    JOIN inventory i ON i.inventory_id = r.inventory_id
    JOIN film f ON f.film_id = i.film_id
    JOIN film_category fc ON fc.film_id = f.film_id
    JOIN category c ON c.category_id = fc.category_id 
    GROUP BY YEAR(p.payment_date), c.name 
    ORDER BY YEAR(p.payment_date), c.name;
    '''
    cursor.execute(query_two)
    query_two_result = cursor.fetchall()

    if (option == "View Sales by City:"):  
        query_three = '''
        CREATE VIEW storeCitySales AS 
        SELECT YEAR(p.payment_date) AS "YEAR", ci.city, SUM(p.amount) AS "TotalPayments"
        FROM payment p 
        JOIN staff sta ON sta.staff_id = p.staff_id
        JOIN store sto ON sto.store_id = sta.store_id
        JOIN address a ON a.address_id = sto.address_id
        JOIN city ci ON ci.city_id = a.city_id
        GROUP BY Year(p.payment_date), ci.city
        ORDER BY YEAR(p.payment_date) DESC;
    '''
    cursor.execute(query_three)
    query_three_result = cursor.fetchone()
    return render_template('rental.html', query_one_result=query_one_result, query_two_result=query_two_result, query_three_result=query_three_result)

@app.route('/customer_reports', methods=('GET',))
def customer_route():
    return render_template('customers.html')

@app.route('/customer_reports', methods=('POST',))
def customer_reports():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)

    option = request.form.get('customers')

    if (option == "View Number of Movies Per Category"):
        query_four = '''
    Create VIEW customerRentalSales AS 
    SELECT YEAR(p.payment_date) AS "YEAR", CONCAT(c.first_name ,' ', c.last_name) AS "name", SUM(p.amount) AS "TotalPayments"   
    FROM payment p
    JOIN customer c ON c.customer_id = p.customer_id
    GROUP BY YEAR(p.payment_date), name
    ORDER BY YEAR(p.payment_date), TotalPayments DESC;

    '''
    cursor.execute(query_four)
    query_four_result = cursor.fetchall()

    if (option == "View Movies In-Stock Per Category"):  
        query_five = '''
    Create VIEW customerMovieRentals AS 
    SELECT YEAR(r.rental_date) AS "YEAR", CONCAT(c.first_name ,' ', c.last_name) AS "name", COUNT(r.rental_id) AS "NumRentals"
    FROM rental r 
    JOIN customer c ON c.customer_id = r.customer_id
    GROUP BY YEAR(r.rental_date), name
    ORDER BY YEAR(r.rental_date), NumRentals  DESC;
    '''
    cursor.execute(query_five)
    query_five_result = cursor.fetchall()

    return render_template('customers.html', query_four_result=query_four_result, query_five_result=query_five_result)

@app.route('/inventory-reports', methods=['GET'])
def inventory_route():
    return render_template('inventory.html')

@app.route('/inventory-reports', methods=['POST'])
def inventory_reports():
    mydb = get_db_connection()
    cursor = mydb.cursor(dictionary=True)

    option = request.form.get('movies')

    if (option == "View Number of Movies Per Category"):
        query_six = '''
        CREATE VIEW moviesPerCategory AS
        SELECT c.name, COUNT(f.film_id) AS numMovies
        FROM film f
        JOIN film_category fc ON fc.film_id = f.film_id
        JOIN category c ON c.category_id = fc.category_id
        GROUP BY c.name 
        ORDER BY NumMovies DESC;
    '''
    cursor.execute(query_six)
    query_six_result = cursor.fetchall()

    if (option == "View Movies In-Stock Per Category"):  
        query_seven = '''
    CREATE VIEW categoryTotals AS 
    SELECT YEAR(p.payment_date) AS "YEAR", c.name, SUM(p.amount)
    FROM payment p
    JOIN rental r ON r.rental_id = p.rental_id
    JOIN inventory i ON i.inventory_id = r.inventory_id
    JOIN film f ON f.film_id = i.film_id
    JOIN film_category fc ON fc.film_id = f.film_id
    JOIN category c ON c.category_id = fc.category_id 
    GROUP BY YEAR(p.payment_date), c.name 
    ORDER BY YEAR(p.payment_date), c.name;
    '''
    cursor.execute(query_seven)
    query_seven_result = cursor.fetchall()

    return render_template('inventory.html', query_six_result=query_six_result, query_seven_result=query_seven_result)

app.run(port=6603, debug=True)

##flask or mysql connector was not working -> https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/
##used chat for submit boxes