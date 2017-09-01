from rest_framework import serializers;
from .models import Job;

class JobSerializer(serializers.ModelSerializer):
    expected_pledged = serializers.FloatField(min_value=0);
    expected_workers = serializers.IntegerField(min_value=0);

    class Meta:
        fields = ['name', 'creation_date', 'pledged', 'paid', 'workers', 'finished'];