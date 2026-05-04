-- 1.1 List the customers who are subscribed to the 'Kobiye Destek' tariff.
-- First, we join the CUSTOMERS table with the TARIFFS table to find the tariff name.
-- We filter the results where the tariff name is 'Kobiye Destek'.
-- This gives us all customers currently subscribed to this specific tariff.
SELECT C.CUSTOMER_ID, C.NAME, C.CITY, C.SIGNUP_DATE
FROM CUSTOMERS C
JOIN TARIFFS T ON C.TARIFF_ID = T.TARIFF_ID
WHERE T.NAME = 'Kobiye Destek';
-- 1.2 Find the newest customer who subscribed to the 'Kobiye Destek' tariff.
-- We use the same join as above but this time we order by SIGNUP_DATE descending.
-- By using ROWNUM = 1, we get only the most recently signed up customer.
-- This helps identify the latest addition to the 'Kobiye Destek' tariff.
SELECT C.CUSTOMER_ID, C.NAME, C.CITY, C.SIGNUP_DATE
FROM CUSTOMERS C
JOIN TARIFFS T ON C.TARIFF_ID = T.TARIFF_ID
WHERE T.NAME = 'Kobiye Destek'
AND ROWNUM = 1
ORDER BY C.SIGNUP_DATE DESC;
-- 1.2 Find the newest customer who subscribed to the 'Kobiye Destek' tariff.
-- We use a subquery to first order customers by SIGNUP_DATE in descending order.
-- Then we apply ROWNUM = 1 on the outer query to get only the top result.
-- This correctly identifies the most recently signed up customer for this tariff.
SELECT * FROM (
    SELECT C.CUSTOMER_ID, C.NAME, C.CITY, C.SIGNUP_DATE
    FROM CUSTOMERS C
    JOIN TARIFFS T ON C.TARIFF_ID = T.TARIFF_ID
    WHERE T.NAME = 'Kobiye Destek'
    ORDER BY C.SIGNUP_DATE DESC
) WHERE ROWNUM = 1;
-- 2.1 Find the distribution of tariffs among the customers.
-- We join CUSTOMERS with TARIFFS to get the tariff names.
-- We group by tariff name and count the number of customers in each group.
-- This gives us a clear picture of how customers are distributed across tariffs.
SELECT T.NAME, COUNT(C.CUSTOMER_ID) AS CUSTOMER_COUNT
FROM CUSTOMERS C
JOIN TARIFFS T ON C.TARIFF_ID = T.TARIFF_ID
GROUP BY T.NAME
ORDER BY CUSTOMER_COUNT DESC;
-- 3.1 Identify the earliest customers to sign up.
-- We use a subquery to find the minimum SIGNUP_DATE in the entire table.
-- Then we select all customers whose SIGNUP_DATE matches that minimum date.
-- Note that the earliest customers might not have the lowest CUSTOMER_IDs.
SELECT CUSTOMER_ID, NAME, CITY, SIGNUP_DATE
FROM CUSTOMERS
WHERE SIGNUP_DATE = (SELECT MIN(SIGNUP_DATE) FROM CUSTOMERS);
-- 3.2 Find the distribution of earliest customers across different cities.
-- We reuse the minimum SIGNUP_DATE condition from the previous query.
-- We group the results by city and count customers in each city.
-- This reveals which cities had the most early adopters of the service.
SELECT CITY, COUNT(CUSTOMER_ID) AS CUSTOMER_COUNT
FROM CUSTOMERS
WHERE SIGNUP_DATE = (SELECT MIN(SIGNUP_DATE) FROM CUSTOMERS)
GROUP BY CITY
ORDER BY CUSTOMER_COUNT DESC;
-- 4.1 Identify the IDs of customers whose monthly records are missing.
-- We compare the CUSTOMERS table with MONTHLY_STATS using a LEFT JOIN.
-- Customers with no matching record in MONTHLY_STATS will have NULL values.
-- This reveals the customers affected by the insertion error.
SELECT C.CUSTOMER_ID
FROM CUSTOMERS C
LEFT JOIN MONTHLY_STATS M ON C.CUSTOMER_ID = M.CUSTOMER_ID
WHERE M.CUSTOMER_ID IS NULL;
-- 4.2 Find the distribution of missing customers across different cities.
-- We use the same LEFT JOIN approach to identify customers with missing records.
-- Then we group by city to see how many missing customers are in each city.
-- This helps identify if the insertion error affected specific regions more.
SELECT C.CITY, COUNT(C.CUSTOMER_ID) AS MISSING_COUNT
FROM CUSTOMERS C
LEFT JOIN MONTHLY_STATS M ON C.CUSTOMER_ID = M.CUSTOMER_ID
WHERE M.CUSTOMER_ID IS NULL
GROUP BY C.CITY
ORDER BY MISSING_COUNT DESC;
-- 5.1 Find customers who have used at least 75% of their data limit.
-- We join MONTHLY_STATS with CUSTOMERS and TARIFFS to get data limits.
-- We calculate the usage percentage by dividing DATA_USAGE by DATA_LIMIT.
-- Customers with 75% or more data usage are filtered and returned.
SELECT C.CUSTOMER_ID, C.NAME, T.NAME AS TARIFF, 
       M.DATA_USAGE, T.DATA_LIMIT,
       ROUND((M.DATA_USAGE / T.DATA_LIMIT) * 100, 2) AS USAGE_PERCENT
FROM MONTHLY_STATS M
JOIN CUSTOMERS C ON M.CUSTOMER_ID = C.CUSTOMER_ID
JOIN TARIFFS T ON C.TARIFF_ID = T.TARIFF_ID
WHERE T.DATA_LIMIT > 0
AND (M.DATA_USAGE / T.DATA_LIMIT) >= 0.75
ORDER BY USAGE_PERCENT DESC;
-- 5.2 Identify customers who have exhausted all of their package limits.
-- We join MONTHLY_STATS with CUSTOMERS and TARIFFS to compare usage vs limits.
-- We check if DATA_USAGE, MINUTE_USAGE and SMS_USAGE all meet or exceed their limits.
-- Only customers who have completely used up all three resources are returned.
SELECT C.CUSTOMER_ID, C.NAME, T.NAME AS TARIFF,
       M.DATA_USAGE, T.DATA_LIMIT,
       M.MINUTE_USAGE, T.MINUTE_LIMIT,
       M.SMS_USAGE, T.SMS_LIMIT
FROM MONTHLY_STATS M
JOIN CUSTOMERS C ON M.CUSTOMER_ID = C.CUSTOMER_ID
JOIN TARIFFS T ON C.TARIFF_ID = T.TARIFF_ID
WHERE M.DATA_USAGE >= T.DATA_LIMIT
AND M.MINUTE_USAGE >= T.MINUTE_LIMIT
AND M.SMS_USAGE >= T.SMS_LIMIT;
-- 6.1 Find the customers who have unpaid fees.
-- We join MONTHLY_STATS with CUSTOMERS to get customer details.
-- We filter records where PAYMENT_STATUS is 'UNPAID'.
-- This identifies all customers who have not yet paid their monthly fees.
SELECT C.CUSTOMER_ID, C.NAME, C.CITY, M.PAYMENT_STATUS
FROM MONTHLY_STATS M
JOIN CUSTOMERS C ON M.CUSTOMER_ID = C.CUSTOMER_ID
WHERE M.PAYMENT_STATUS = 'UNPAID';
-- 6.2 Find the distribution of all payment statuses across different tariffs.
-- We join all three tables to get tariff names and payment statuses together.
-- We group by tariff name and payment status to see the distribution.
-- This gives a complete overview of payment behavior across all tariffs.
SELECT T.NAME AS TARIFF, M.PAYMENT_STATUS, COUNT(*) AS COUNT
FROM MONTHLY_STATS M
JOIN CUSTOMERS C ON M.CUSTOMER_ID = C.CUSTOMER_ID
JOIN TARIFFS T ON C.TARIFF_ID = T.TARIFF_ID
GROUP BY T.NAME, M.PAYMENT_STATUS
ORDER BY T.NAME, M.PAYMENT_STATUS;