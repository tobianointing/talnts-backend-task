from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import SuggestionSerializer
from .utils import calculate_score, get_suggestions

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes


class SuggestionsView(APIView):
    @extend_schema(
        # extra parameters added to the schema
        parameters=[
            OpenApiParameter(
                name="q",
                description="The partial or complete search term",
                required=True,
                examples=[
                    OpenApiExample(
                        "Example",
                        value="Londo",
                    ),
                ],
            ),
            OpenApiParameter(
                name="latitute",
                description="caller's latitute",
                type=OpenApiTypes.FLOAT,
                examples=[
                    OpenApiExample(
                        "Example",
                        value="43.70011",
                    ),
                ],
            ),
            OpenApiParameter(
                name="longitute",
                description="caller's longitute",
                type=OpenApiTypes.FLOAT,
                examples=[
                    OpenApiExample(
                        "Example",
                        value="-79.4931",
                    ),
                ],
            ),
        ],
    )
    def get(self, request, format=None):
        """
        View that return a response of suggestions
        for large cities based on the user query
        with there, name, latitue, longitute and proximity score
        to the user coordinate
        """

        q = request.query_params.get("q", None)

        if not q:
            return Response(
                {"message": "The query params `q` must be defined"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        latitute = request.query_params.get("latitute", None)
        longitute = request.query_params.get("longitute", None)

        if latitute and longitute:
            latitute, longitute = map(float, [latitute, longitute])

            user_coordinate = (longitute, latitute)
            suggestions, max_distance = get_suggestions(q, user_coordinate)
            suggestions = calculate_score(max_distance, suggestions)
            suggestions = sorted(suggestions, key=lambda s: s.score, reverse=True)
            serializer = SuggestionSerializer(suggestions, many=True)

        else:
            suggestions, max_distance = get_suggestions(q)
            serializer = SuggestionSerializer(suggestions, many=True)

        return Response({"suggestions": serializer.data})
