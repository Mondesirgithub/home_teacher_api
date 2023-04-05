from rest_framework import serializers
from .models import Tuteur, Eleve, Professeur, Encadrement


class EleveSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Eleve
        fields = '__all__'
    



class TuteurSerializer(serializers.ModelSerializer):
    eleves = serializers.SerializerMethodField()

    def get_eleves(self, obj):
        eleves = obj.eleve_set.all()
        serializer = EleveSerializer(eleves, many=True)
        return serializer.data

    class Meta:
        model = Tuteur
        fields = '__all__'


class ProfesseurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professeur
        fields = '__all__'