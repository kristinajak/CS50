-- Keep a log of any SQL queries you execute as you solve the mystery.
-- Investigating crime scene report
SELECT description
FROM crime_scene_reports
WHERE year = 2021 AND month = 7 AND day = 28
AND street = "Humphrey Street";

-- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
-- Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
-- Littering took place at 16:36. No known witnesses.

SELECT name, transcript
FROM interviews
WHERE transcript LIKE "%bakery%";
-- Answer:
-- | Ruth    | Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away. If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.                                                          |
-- | Eugene  | I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.                                                                                                 |
-- | Raymond | As the thief was leaving the bakery, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket. |
-- | Kiana   | I saw Richard take a bite out of his pastry at the bakery before his pastry was stolen from him.

-- Checking the license plate numbers
SELECT activity, license_plate, month, day, hour, minute
FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25;

-- | activity | license_plate | month | day | hour | minute |
-- | exit     | 5P2BI95       | 7     | 28  | 10   | 16     |
-- | exit     | 94KL13X       | 7     | 28  | 10   | 18     |
-- | exit     | 6P58WS2       | 7     | 28  | 10   | 18     |
-- | exit     | 4328GD8       | 7     | 28  | 10   | 19     |
-- | exit     | G412CB7       | 7     | 28  | 10   | 20     |
-- | exit     | L93JTIZ       | 7     | 28  | 10   | 21     |
-- | exit     | 322W7JE       | 7     | 28  | 10   | 23     |
-- | exit     | 0NTHK55       | 7     | 28  | 10   | 23     |

-- Checking IDs
SELECT license_plate, people.id
FROM people
WHERE license_plate IN
(SELECT license_plate
FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25);

-- license_plate |   id   |
-- | 5P2BI95       | 221103 |
-- | 6P58WS2       | 243696 |
-- | L93JTIZ       | 396669 |
-- | G412CB7       | 398010 |
-- | 4328GD8       | 467400 |
-- | 322W7JE       | 514354 |
-- | 0NTHK55       | 560886 |
-- | 94KL13X       | 686048

-- Checking ATM infromation
SELECT account_number
FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw";

--| account_number |
--| 28500762       |
--| 28296815       |
--| 76054385       |
--| 49610011       |
--| 16153065       |
--| 25506511       |
--| 81061156       |
--| 26013199       |

-- Checking to whom the accounts belong

SELECT person_id
FROM bank_accounts
WHERE account_number IN
(SELECT account_number
FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw");

--| person_id |
--| 686048    |
--| 514354    |
--| 458378    |
--| 395717    |
--| 396669    |
--| 467400    |
--| 449774    |
--| 438727    |

-- Comparing license plate vs. bank accounts
SELECT person_id
FROM bank_accounts
INNER JOIN people ON people.id = person_id
WHERE account_number IN
(SELECT account_number
FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw")
AND license_plate IN
(SELECT license_plate
FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25);
-- +-----------+
-- | person_id |
-- +-----------+
-- | 686048    |
-- | 514354    |
-- | 396669    |
-- | 467400    |
-- +-----------+

-- Checking for the phone numbers
SELECT people.id, phone_number
FROM people
WHERE people.id IN
(SELECT person_id
FROM bank_accounts
INNER JOIN people ON people.id = person_id
WHERE account_number IN
(SELECT account_number
FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw")
AND license_plate IN
(SELECT license_plate
FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25));
-- +--------+----------------+
-- |   id   |  phone_number  |
-- +--------+----------------+
-- | 396669 | (829) 555-5269 |
-- | 467400 | (389) 555-5198 |
-- | 514354 | (770) 555-1861 |
-- | 686048 | (367) 555-5533 |
-- +--------+----------------+

-- Checking who had a phone call as per witness transcript
SELECT caller, duration, receiver
FROM phone_calls
WHERE caller IN
(SELECT phone_number
FROM people
WHERE people.id IN
(SELECT person_id
FROM bank_accounts
INNER JOIN people ON people.id = person_id
WHERE account_number IN
(SELECT account_number
FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw")
AND license_plate IN
(SELECT license_plate
FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25)))
AND month = 7 AND day = 28 AND duration < 60;
-- +----------------+----------+----------------+
-- |     caller     | duration |    receiver    |
-- +----------------+----------+----------------+
-- | (367) 555-5533 | 45       | (375) 555-8161 |
-- | (770) 555-1861 | 49       | (725) 555-3243 |
-- +----------------+----------+----------------+

-- Checking flight ids on July 29 with the origin flight from Fiftyville
SELECT flights.id, hour, minute
FROM flights
WHERE origin_airport_id =
(SELECT airports.id FROM airports WHERE city = "Fiftyville")
AND month = 7 AND day = 29;
-- +----+------+--------+
-- | id | hour | minute |
-- +----+------+--------+
-- | 18 | 16   | 0      |
-- | 23 | 12   | 15     |
-- | 36 | 8    | 20     |
-- | 43 | 9    | 30     |
-- | 53 | 15   | 20     |
-- +----+------+--------+

-- Checking the passport number
SELECT id, name, passport_number
FROM people
WHERE phone_number IN
(SELECT caller
FROM phone_calls
WHERE caller IN
(SELECT phone_number
FROM people
WHERE people.id IN
(SELECT person_id
FROM bank_accounts
INNER JOIN people ON people.id = person_id
WHERE account_number IN
(SELECT account_number
FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw")
AND license_plate IN
(SELECT license_plate
FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25)))
AND month = 7 AND day = 28 AND duration < 60);
-- |   id   | name  | passport_number |
-- +--------+-------+-----------------+
-- | 514354 | Diana | 3592750733      |
-- | 686048 | Bruce | 5773159633      |
-- +--------+-------+-----------------+

-- Checking what flights (IDs) were taken by two suspects
SELECT passport_number, flight_id
FROM passengers
WHERE passport_number IN
(SELECT passport_number
FROM people
WHERE phone_number IN
(SELECT caller
FROM phone_calls
WHERE caller IN
(SELECT phone_number
FROM people
WHERE people.id IN
(SELECT person_id
FROM bank_accounts
INNER JOIN people ON people.id = person_id
WHERE account_number IN
(SELECT account_number
FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw")
AND license_plate IN
(SELECT license_plate
FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25)))
AND month = 7 AND day = 28 AND duration < 60));
-- +-----------------+-----------+
-- | passport_number | flight_id |
-- +-----------------+-----------+
-- | 3592750733      | 18        |
-- | 3592750733      | 24        |
-- | 5773159633      | 36        |
-- | 3592750733      | 54        |
-- +-----------------+-----------+

-- Checking the flight of a suspect
SELECT id, month, day, hour, minute
FROM flights
WHERE flights.id IN
(SELECT flight_id
FROM passengers
WHERE passport_number IN
(SELECT passport_number
FROM people
WHERE phone_number IN
(SELECT caller
FROM phone_calls
WHERE caller IN
(SELECT phone_number
FROM people
WHERE people.id IN
(SELECT person_id
FROM bank_accounts
INNER JOIN people ON people.id = person_id
WHERE account_number IN
(SELECT account_number
FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw")
AND license_plate IN
(SELECT license_plate
FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25)))
AND month = 7 AND day = 28 AND duration < 60)))
AND month = 7 AND day = 29;
-- +----+-------+-----+------+--------+
-- | id | month | day | hour | minute |
-- +----+-------+-----+------+--------+
-- | 18 | 7     | 29  | 16   | 0      |
-- | 36 | 7     | 29  | 8    | 20     |
-- +----+-------+-----+------+--------+
-- Answer: the suspect flight ID is 36.

SELECT destination_airport_id
FROM flights
WHERE id = 36;
--Answer 4

SELECT city
FROM airports WHERE id = 4;
--The city the thief ESCAPED TO: New York City

SELECT phone_number
FROM people
WHERE phone_number IN
(SELECT caller
FROM phone_calls
WHERE caller IN
(SELECT phone_number
FROM people
WHERE people.id IN
(SELECT person_id
FROM bank_accounts
INNER JOIN people ON people.id = person_id
WHERE account_number IN
(SELECT account_number
FROM atm_transactions
WHERE month = 7 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw")
AND license_plate IN
(SELECT license_plate
FROM bakery_security_logs
WHERE month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25)))
AND month = 7 AND day = 28 AND duration < 60);
-- +-------+----------------+
-- | name  |  phone_number  |
-- +-------+----------------+
-- | Diana | (770) 555-1861 |
-- | Bruce | (367) 555-5533 |
-- +-------+----------------+

SELECT name
FROM people
WHERE phone_number = "(375) 555-8161";
-- The ACCOMPLICE is: Robin