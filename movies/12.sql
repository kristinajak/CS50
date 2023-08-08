SELECT title FROM movies JOIN stars ON stars.movie_id = movies.id WHERE person_id = (SELECT people.id FROM people WHERE name = "Helena Bonham Carter") OR person_id = (SELECT people.id FROM people WHERE name = "Johnny Depp") GROUP BY title HAVING COUNT(title) = 2;