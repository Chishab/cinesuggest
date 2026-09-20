import math
import re
from collections import Counter


def _tokens(movie):
    text = f"{movie.genre} {movie.description}".lower()
    return re.findall(r"[a-z0-9]+", text)


def _cosine(left, right):
    common = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in common)
    left_size = math.sqrt(sum(value * value for value in left.values()))
    right_size = math.sqrt(sum(value * value for value in right.values()))
    if not left_size or not right_size:
        return 0.0
    return numerator / (left_size * right_size)


def recommend_movies(selected_movie, movies, limit=6):
    selected_vector = Counter(_tokens(selected_movie))
    recommendations = []
    for movie in movies:
        if movie.id == selected_movie.id:
            continue
        score = _cosine(selected_vector, Counter(_tokens(movie)))
        recommendations.append((score, movie))
    recommendations.sort(key=lambda item: (item[0], item[1].rating), reverse=True)
    return recommendations[:limit]
