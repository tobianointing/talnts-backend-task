from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Suggestion
from .utils import (
    haversine,
    calculate_score,
    get_country_from_iso,
    get_suggestions,
)


def get_suggestion_dicts_objects():
    """
    Return list of custom dictionary suggestions that has
    name, latitute, longitute, distance_diff, score
    and also the list of suggestion objects without the score field
    """
    full_suggestions_list = [
        Suggestion(
            **{
                "name": "Londonderry, VT, United States",
                "latitute": 43.22646,
                "longitute": -72.80649,
                "distance_diff": 535.9064222347274,
                "score": 0.8,
            }
        ),
        Suggestion(
            **{
                "name": "London, CA, United States",
                "latitute": 36.47606,
                "longitute": -119.44318,
                "score": 0.3,
                "distance_diff": 3462.948799761196,
            }
        ),
        Suggestion(
            **{
                "name": "Londonderry County Borough, NIR, United Kingdom",
                "latitute": 54.99721,
                "longitute": -7.30917,
                "score": 0.0,
                "distance_diff": 5126.6964761758745,
            }
        ),
    ]

    suggestions_list_for_calculate_score = [
        Suggestion(s.name, s.longitute, s.latitute, s.distance_diff)
        for s in full_suggestions_list
    ]

    return full_suggestions_list, suggestions_list_for_calculate_score


# Create your tests here.
class SuggestionViewTest(APITestCase):
    def test_no_q_parameter_is_passed(self):
        """
        Ensure the q query params is passed to the url
        """
        url = reverse("suggestions")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data, {"message": "The query params `q` must be defined"}
        )

    def test_q_parameter_is_passed(self):
        url = reverse("suggestions")
        data = {"q": "Londo"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["suggestions"], [])

    def test_invalid_q_parameter(self):
        url = reverse("suggestions")
        data = {"q": "12swy781jhd"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["suggestions"], [])

    def test_no_longitute_latittute_params(self):
        url = reverse("suggestions")
        data = {"q": "Londo"}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["suggestions"][0]["score"], None)
        self.assertEqual(response.data["suggestions"][1]["score"], None)

    def test_longitute_latittute_params(self):
        url = reverse("suggestions")
        data = {"q": "Londo", "latitute": 43.70011, "longitute": -79.4931}
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(response.data["suggestions"][0]["score"], None)


class CustomFunctionsTest(APITestCase):
    def test_haversine(self):
        """Given two tubles of location cordinate
        return the distance between them
        """
        coord1 = (-79.3831843, 43.653226)
        coord2 = (-80.4771472, 43.4129238)

        distance = haversine(coord1, coord2)

        self.assertEqual(distance, 92.1467741859417)

    def test_calculate_score(self):
        """
        Given the list of suggestions and the max distance value.
        Return a list of suggestions object with a score between the
        range of 0 - 1.
        """
        (
            full_suggestions_list,
            suggestions_list_for_calculate_score,
        ) = get_suggestion_dicts_objects()
        max_distance = 5126.6964761758745
        result = calculate_score(max_distance, suggestions_list_for_calculate_score)

        self.assertEqual(result, full_suggestions_list)

    def test_get_country_from_iso(self):
        """
        Given the iso code of a country should return the full country name
        """
        iso_code = "US"
        country_name = get_country_from_iso(iso_code)

        self.assertEqual(country_name, "United States")

    def test_get_suggestions(self):
        """
        Given a search keyword and user coordinate as tuple
        should return a list objects of suggestions and a max distance != 0.0
        """
        q = "Londo"
        user_coord = (-79.4931, 43.70011)

        suggestions, max_distance = get_suggestions(q, user_coord)

        self.assertNotEqual(suggestions, [])
        self.assertNotEqual(max_distance, 0.0)

    def test_get_suggestions_no_user_coord(self):
        """
        Given a search keyword without user coordinate as tuple
        should return a list objects of suggestions and a max distance = 0.0
        """
        q = "Londo"

        suggestions, max_distance = get_suggestions(q)

        self.assertNotEqual(suggestions, [])
        self.assertEqual(max_distance, 0.0)
