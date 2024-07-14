def sentiment_to_stars(sentiment):
    stars = (sentiment + 1) * 2.5
    return round(stars)


def display_stars(stars):
    full_stars = int(stars)
    half_star = 1 if stars - full_stars >= 0.5 else 0
    empty_stars = 5 - full_stars - half_star
    stars_str = '★' * full_stars + '☆' * empty_stars
    if half_star:
        stars_str = stars_str[:-1] + '⭒' + '☆' * (empty_stars - 1)
    return stars_str
