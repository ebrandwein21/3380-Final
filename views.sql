--Create a view named monthlyRentalSales that calculates monthly rental sales for all years of payments in the database. Order by year and month in ascending order. The columns of the view will the following
--year : displays the year for the payments
--month: displays the month name of the payments
--month_num: displays the month number of the payments
--TotalPayments: displays the total payments for that month of the year
Create VIEW monthlyRentalSales AS 
SELECT YEAR(r.rental_date) AS "YEAR", MONTH(r.rental_date) AS "MONTH", SUM(p.amount) AS "TotalPayments"
FROM rental r, payment p
WHERE r.rental_id = p.rental_id
GROUP BY YEAR(r.rental_date), MONTH(r.rental_date) 
ORDER BY YEAR(r.rental_date), MONTH(r.rental_date) ASC;

--Create a view named categoryTotals that calculates yearly rental sales for movie categories in the database. Order by year (ascending order) and name (descending order).  The columns of the view will the following
--year : displays the year for the payments
--name: displays the category name
--TotalPayments: displays the total rental payments for that category

CREATE VIEW categoryTotals AS 
SELECT YEAR(r.rental_date) AS "YEAR", c.name
FROM rental r, category c
WHERE c.last_update = r.last_update
ORDER BY YEAR(r.rental_date) ASC, c.name DESC;

--Create a view named storeCitySales that calculates yearly rental sales for cities each rental store is located in. Order by year  in descending order. The columns of the view will the following
--city: displays the city location of the store
--year : displays the year for the payments
--TotalPayments: displays the total rental payments for that city
CREATE VIEW storeCitySales AS 
SELECT YEAR(r.rental_date) AS "YEAR", c.city 
FROM rental r, city calculates
WHERE r.last_update = c.last_update
ORDER BY SELECT YEAR(r.rental_date) AS "YEAR" DESC;

--Create a view named customerRentalSales that calculates yearly rental sales for each customer. Order by year (ascending) and TotalPayments in descending order.  The columns of the view will the following
--year : displays the year for the payments
--name: displays the first and last name of the customer
--TotalPayments: displays the total rental payments for that customer
Create VIEW customerRentalSales AS 
SELECT YEAR(r.rental_date) AS "YEAR", SUM(p.amount) AS "TotalPayments"
FROM rental r, payment p
WHERE r.rental_id = p.rental_id
GROUP BY YEAR(r.rental_date), MONTH(r.rental_date) 
ORDER BY YEAR(r.rental_date), MONTH(r.rental_date) ASC;


--Create a view named customerMovieRentals that calculates yearly number of movies rented for each customer. Order by year (ascending) and TotalPayments in descending order.  The columns of the view will the following
--year : displays the year for the payments
--name: displays the first and last name of the customer
--NumRentals: displays the number of movies rented for that customer in that year
Create VIEW customerMovieRentals AS
