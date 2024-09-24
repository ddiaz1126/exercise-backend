from django.shortcuts import render
from rest_framework import generics
from .models import Exercise
from .serializers import ExerciseSerializer

class ExerciseListCreate(generics.ListCreateAPIView):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer
