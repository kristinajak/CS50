SELECT people.name FROM people JOIN stars ON stars.person_id = people.id
WHERE
    people.name != "Kevin Bacon" AND
    movie_id IN (
    SELECT movie_id from stars JOIN people ON people.id = stars.person_id
    WHERE people.name = "Kevin Bacon" AND birth = "1958");