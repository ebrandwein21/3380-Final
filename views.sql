--Create a view named monthlyRentalSales that calculates monthly rental sales for all years of payments in the database. Order by year and month in ascending order. The columns of the view will the following
--year : displays the year for the payments
--month: displays the month name of the payments
--month_num: displays the month number of the payments
--TotalPayments: displays the total payments for that month of the year
Create VIEW monthlyRentalSales AS 
SELECT YEAR(p.payment_date) AS "YEAR", MONTH(p.payment_date) AS "MONTH", SUM(p.amount) AS "TotalPayments"
FROM payment p
JOIN rental r ON r.rental_id = p.rental_id
GROUP BY YEAR(p.payment_date), MONTH(p.payment_date) 
ORDER BY YEAR(p.payment_date) ASC, MONTH(p.payment_date) ASC;

--Create a view named categoryTotals that calculates yearly rental sales for movie categories in the database. Order by year (ascending order) and name (descending order).  The columns of the view will the following
--year : displays the year for the payments
--name: displays the category name
--TotalPayments: displays the total rental payments for that category

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

--Create a view named storeCitySales that calculates yearly rental sales for cities each rental store is located in. Order by year  in descending order. The columns of the view will the following
--city: displays the city location of the store
--year : displays the year for the payments
--TotalPayments: displays the total rental payments for that city
--NUMS NOT COMPLETE 
CREATE VIEW storeCitySales AS 
SELECT YEAR(p.payment_date) AS "YEAR", ci.city, SUM(p.amount) AS "TotalPayments"
FROM payment p 
JOIN staff sta ON sta.staff_id = p.staff_id
JOIN store sto ON sto.store_id = sta.store_id
JOIN address a ON a.address_id = sto.address_id
JOIN city ci ON ci.city_id = a.city_id
GROUP BY Year(p.payment_date), ci.city
ORDER BY YEAR(p.payment_date) DESC;

--Create a view named customerRentalSales that calculates yearly rental sales for each customer. Order by year (ascending) and TotalPayments in descending order.  The columns of the view will the following
--year : displays the year for the payments
--name: displays the first and last name of the customer
--TotalPayments: displays the total rental payments for that customer
Create VIEW customerRentalSales AS 
SELECT YEAR(p.payment_date) AS "YEAR", CONCAT(c.first_name ,' ', c.last_name) AS "name", SUM(p.amount) AS "TotalPayments"   
FROM payment p
JOIN customer c ON c.customer_id = p.customer_id
GROUP BY YEAR(p.payment_date), name
ORDER BY YEAR(p.payment_date), TotalPayments DESC;


--Create a view named customerMovieRentals that calculates yearly number of movies rented for each customer. Order by year (ascending) and TotalPayments in descending order.  The columns of the view will the following
--year : displays the year for the payments
--name: displays the first and last name of the customer
--NumRentals: displays the number of movies rented for that customer in that year
Create VIEW customerMovieRentals AS 
SELECT YEAR(r.rental_date) AS "YEAR", CONCAT(c.first_name ,' ', c.last_name) AS "name", COUNT(r.rental_id) AS "NumRentals"
FROM rental r 
JOIN customer c ON c.customer_id = r.customer_id
GROUP BY YEAR(r.rental_date), name
ORDER BY YEAR(r.rental_date), NumRentals  DESC;

--Create a view named moviesPerCategory that calculates the number of movies in each category. Order by numMovies in descending order.  The columns of the view will the following
--name: displays the category name
--numMovies: displays the number of movies in that category
CREATE VIEW moviesPerCategory AS
SELECT c.name, COUNT(f.film_id) AS numMovies
FROM film f
JOIN film_category fc ON fc.film_id = f.film_id
JOIN category c ON c.category_id = fc.category_id
GROUP BY c.name 
ORDER BY NumMovies DESC;

--Create a view named moviesPerCategoryInStock that calculates the number of movies in each category currently in inventory. Order by then number of movies in stock in descending order.  The columns of the view will the following
--name: displays the category name
--inStock: displays the number of movies currently in stock in that category
CREATE VIEW moviesPerCategoryInStock AS
SELECT c.name, COUNT(i.film_id) AS inStock
FROM inventory i 
JOIN film f ON f.film_id = i.film_id
JOIN film_category fc ON fc.film_id = f.film_id
JOIN category c ON c.category_id = fc.category_id
GROUP BY c.name 
ORDER BY inStock DESC;
--sources 
--https://stackoverflow.com/questions/48576847/how-to-combine-first-name-middle-name-and-last-name-in-sql-server
