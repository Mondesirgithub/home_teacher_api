from rest_framework import serializers
from .models import Tuteur, Eleve, Professeur
from rest_framework_simplejwt.tokens import RefreshToken


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
        fields = ['id','first_name','last_name','username','email','profession','eleves']


class ProfesseurSerializer(serializers.ModelSerializer):

    class Meta:
        model = Professeur
        fields = ['id','first_name','last_name','username','email','date_naissance', 'adresse', 'statut', 'universite',
                  'filiere_etude','annee_etude','dernier_diplome',
                  'filiere_dernier_diplome','jours_disponibles','matieres_generales_enseignables',
                  'classes_generales_enseignables','classes_techniques_enseignables','matieres_techniques_enseignables',
                  'zones_travail','periode_journee','piece_jointe','ideleves'
                  ]
        

class TuteurSerializerWithToken(serializers.ModelSerializer):
    eleves = serializers.SerializerMethodField()
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    def get_eleves(self, obj):
        eleves = obj.eleve_set.all()
        serializer = EleveSerializer(eleves, many=True)
        return serializer.data

    class Meta:
        model = Tuteur
        fields = ['id','first_name','last_name','username','email','password','profession','eleves','token']


class ProfesseurSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField(read_only=True)

    def get_token(self, obj):
        token = RefreshToken.for_user(obj)
        return str(token.access_token)

    class Meta:
        model = Professeur
        fields = ['id','first_name','last_name','username','email','date_naissance', 'adresse', 'statut', 'universite',
                  'filiere_etude','annee_etude','dernier_diplome',
                  'filiere_dernier_diplome','jours_disponibles','matieres_generales_enseignables',
                  'classes_generales_enseignables','classes_techniques_enseignables','matieres_techniques_enseignables',
                  'zones_travail','periode_journee','piece_jointe','ideleves','password','token'
                  ]
