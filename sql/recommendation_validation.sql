-- SQLite practice queries for MovieLens 100K recommendation-data validation.
-- `ratings` fields: user_id, movie_id, rating, timestamp.

-- Filtering and valid-value check
SELECT COUNT(*) AS invalid_rating_count
FROM ratings
WHERE rating NOT BETWEEN 1 AND 5;

-- Aggregation: interactions per user
SELECT user_id, COUNT(*) AS interaction_count
FROM ratings
GROUP BY user_id
ORDER BY interaction_count DESC, user_id
LIMIT 10;

-- HAVING: users with at least 100 interactions
SELECT user_id, COUNT(*) AS interaction_count
FROM ratings
GROUP BY user_id
HAVING COUNT(*) >= 100
ORDER BY interaction_count DESC, user_id;

-- NULL validation (identifiers, target, and event time)
SELECT
  SUM(user_id IS NULL) AS null_user_ids,
  SUM(movie_id IS NULL) AS null_movie_ids,
  SUM(rating IS NULL) AS null_ratings,
  SUM(timestamp IS NULL) AS null_timestamps
FROM ratings;

-- Exact duplicate records
SELECT user_id, movie_id, rating, timestamp, COUNT(*) AS duplicate_count
FROM ratings
GROUP BY user_id, movie_id, rating, timestamp
HAVING COUNT(*) > 1;

-- Repeated user-item interactions (not automatically invalid)
SELECT user_id, movie_id, COUNT(*) AS interaction_count
FROM ratings
GROUP BY user_id, movie_id
HAVING COUNT(*) > 1
ORDER BY interaction_count DESC, user_id, movie_id;

-- Join practice: attach a computed popularity table to interactions.
WITH item_popularity AS (
  SELECT movie_id, COUNT(*) AS interaction_count
  FROM ratings
  GROUP BY movie_id
)
SELECT r.user_id, r.movie_id, r.rating, p.interaction_count
FROM ratings AS r
JOIN item_popularity AS p ON p.movie_id = r.movie_id
ORDER BY p.interaction_count DESC, r.user_id
LIMIT 10;
