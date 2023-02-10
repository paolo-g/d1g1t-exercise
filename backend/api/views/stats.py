""" Module stats providing stats endpoints"""
import statistics
from collections import Counter
from datetime import date
from rest_framework import status
from rest_framework.decorators import (
    api_view, permission_classes
)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from api.models import (
    Team, Happiness
)

@api_view(['GET'])
@permission_classes([IsAuthenticatedOrReadOnly])
def stats(request):
    """
    API GET endpoint that reports team statistics.

    Anonymous users see averages for all teams today.
    Authenticated users see their daily team report.
    """
    if not request.user.is_authenticated:
        # Get the happiness reports for each team today
        team_reports = {}
        teams = Team.objects.all()
        for team in teams:
            team_reports[team.name] = []
            reports = Happiness.objects.filter(owner__team=team,
                                               created_at__gte=date.today())
            for report in reports:
                team_reports[team.name].append(report.rating)


        # Build the anonymous report
        anonymous_report = {}
        for team_name, values in team_reports.items():
            if not values:
                continue
            anonymous_report[team_name] = statistics.mean(values)

        return Response(anonymous_report, status=status.HTTP_200_OK)



    # Authenticated user; get team happiness reports and compute stats
    reports = Happiness.objects.filter(owner__team=request.user.team,
                                       created_at__gte=date.today())
    team_reports = []
    for report in reports:
        team_reports.append(report.rating)

    if not team_reports:
        return Response({}, status=status.HTTP_200_OK)

    authenticated_report = {'average': statistics.mean(team_reports),
                            'levels': Counter(team_reports)}

    return Response(authenticated_report, status=status.HTTP_200_OK)
