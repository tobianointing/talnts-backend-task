import csv
from math import asin, cos, floor, radians, sin, sqrt
from .models import Suggestion


def haversine(coord1: tuple, coord2: tuple) -> float:
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    lon1, lat1 = coord1
    lon2, lat2 = coord2

    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    long_diff = lon2 - lon1
    lat_diff = lat2 - lat1
    a = sin(lat_diff / 2) ** 2 + cos(lat1) * cos(lat2) * sin(long_diff / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r


def calculate_score(
    max_distance: float, suggestions: list[Suggestion]
) -> list[Suggestion]:
    """
    Get the list of suggestions and the max distance value.
    Divide each suggestion distance with the max distance and
    substract 1 from it to assign the least distance to the user distance
    the highest score.
    """

    for suggestion in suggestions:
        score = 1 - (suggestion.distance_diff / max_distance)
        score = floor(score * 10) / 10
        suggestion.score = score

    return suggestions


def get_country_from_iso(iso: str) -> str:
    """
    Given an ISO code return the full country name
    """
    with open("countries.txt", "r", newline="") as f:
        reader = csv.reader(f, quoting=csv.QUOTE_NONE, delimiter="\t")

        headers = next(reader)

        for row in reader:
            country_index = headers.index("Country")
            search_index = headers.index("ISO")

            if iso == row[search_index]:
                return row[country_index]


HEADERS = [
    "geonameid",
    "name",
    "asciiname",
    "alternatenames",
    "latitude",
    "longitude",
    "feature class",
    "feature code",
    "country code",
    "cc2",
    "admin1 code",
    "admin2 code",
    "admin3 code",
    "admin4 code",
    "population",
    "elevation",
    "dem",
    "timezone",
    "modification date",
]


def get_suggestions(
    q: str, user_coordinate: tuple = None, file_name: str = "cities500.txt"
):
    """
    Function that return a dataclass object for cities
    gotten from the file cities500.txt with the value
    name, latitute, longitute, distance diff and score
    """
    suggestions: list[Suggestion] = []
    max_distance = 0.0

    with open(file_name, "r", encoding="utf-8", newline="") as file:
        cities_reader = csv.reader(file, delimiter="\t", quoting=csv.QUOTE_NONE)

        search_index = HEADERS.index("name")
        latitute_index = HEADERS.index("latitude")
        longitude_index = HEADERS.index("longitude")
        country_code_index = HEADERS.index("country code")
        admin1_code_index = HEADERS.index("admin1 code")

        for city in cities_reader:
            if city[search_index].lower().startswith(q.lower()):
                suggestion_coordinate = (
                    float(city[longitude_index]),
                    float(city[latitute_index]),
                )

                full_country_name = get_country_from_iso(city[country_code_index])

                if user_coordinate:
                    user_distance_diff = haversine(
                        user_coordinate, suggestion_coordinate
                    )
                    max_distance = max(max_distance, user_distance_diff)

                    suggestions.append(
                        Suggestion(
                            name=f"{city[search_index]}, {city[admin1_code_index]}, {full_country_name}",
                            latitute=city[latitute_index],
                            longitute=city[longitude_index],
                            distance_diff=user_distance_diff,
                        )
                    )
                else:
                    suggestions.append(
                        Suggestion(
                            name=f"{city[search_index]}, {city[admin1_code_index]}, {full_country_name}",
                            latitute=city[latitute_index],
                            longitute=city[longitude_index],
                        )
                    )

    return suggestions, max_distance
