-- Keep a log of any SQL queries you execute as you solve the mystery.

-- SELECT *
-- FROM crime_scene_reports
-- WHERE street = "Humphrey Street" AND month = 7 AND year = 2021 AND day = 28

-- ** Check Transcipts (161: 10mins car left, 162: ATM before theft, 163: call about Flight after theft)
-- SELECT *
-- FROM interviews
-- WHERE month = 7 AND year = 2021 AND day = 28 AND transcript LIKE "%bakery%";

-- ** 161: Sometime within ten minutes of the theft, I saw the thief get into a car in
-- the bakery parking lot and drive away. If you have security footage from the bakery parking lot,
-- you might want to look for cars that left the parking lot in that time frame.

-- ** Cars activity within 10.15 - 10.25
-- SELECT name
-- FROM bakery_security_logs JOIN people ON people.license_plate = bakery_security_logs.license_plate
-- WHERE month = 7 AND year = 2021 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <=25 AND activity = "exit"

-- ****** Suspects Here: Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana, Kelsey ******

-- ** I don't know the thief's name, but it was someone I recognized.
-- ** Earlier this morning, before I arrived at Emma's bakery,
-- ** I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

-- ****** Suspects Here: Bruce, Iman, Diana, Brooke, Kenny, Luca, Taylor, Benista ******

-- SELECT name
-- FROM atm_transactions JOIN bank_accounts ON bank_accounts.account_number = atm_transactions.account_number JOIN people ON people.id = bank_accounts.person_id
-- WHERE month = 7 AND year = 2021 AND day = 28 AND atm_location = "Leggett Street" AND transaction_type = "withdraw"

-- ****** Reappeared Suspects Are: Bruce, Iman, Diana, Luca ******

-- ** As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
-- ** In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
-- ** The thief then asked the person on the other end of the phone to purchase the flight ticket.

-- People who fly on the ealiest flight on 29th (INFO: passport, phone num, name, license plate)
-- SELECT name
-- FROM passengers JOIN flights ON flight_id = flights.id JOIN people ON passengers.passport_number = people.passport_number
-- WHERE month = 7 AND year = 2021 AND day = 29 AND flight_id = (
--     SELECT id
--     FROM flights
--     WHERE month = 7 AND year = 2021 AND day = 29
--     ORDER BY hour,minute
-- )

-- ****** Reappeared Suspects Are: Bruce, Luca ******

-- ** Calls less than 60s
-- SELECT name
-- FROM phone_calls JOIN people ON people.phone_number = phone_calls.caller
-- WHERE month = 7 AND year = 2021 AND day = 28 AND duration < 60

-- ****** ONLY Reappeared Suspects: Bruce ******

-- ****** Bruce is the sneaky boi ******

-- ** Bruce fly to ....? (NYC)
-- SELECT city
-- FROM passengers JOIN flights ON flight_id = flights.id JOIN people ON passengers.passport_number = people.passport_number JOIN airports ON airports.id = flights.destination_airport_id
-- WHERE month = 7 AND year = 2021 AND day = 29 AND name = "Bruce" AND flight_id = (
--     SELECT id
--     FROM flights
--     WHERE month = 7 AND year = 2021 AND day = 29
--     ORDER BY hour,minute
-- )

-- ** Who Help Bruce ....?
-- SELECT *
-- FROM phone_calls JOIN people ON people.phone_number = phone_calls.caller
-- WHERE month = 7 AND year = 2021 AND day = 28 AND duration < 60 AND name = "Bruce"

-- SELECT name
-- FROM people
-- WHERE phone_number = "(375) 555-8161"