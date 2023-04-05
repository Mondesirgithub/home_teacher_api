from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from comptes.models import Tuteur, Professeur, Eleve
from comptes.serializers import TuteurSerializer, ProfesseurSerializer, EleveSerializer, TuteurSerializerWithToken, ProfesseurSerializerWithToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        tuteur = Tuteur.objects.filter(username=attrs['username']).first()
        professeur = Professeur.objects.filter(username=attrs['username']).first()
        
        if tuteur:
            if tuteur.check_password(attrs['password']):
                serializer = TuteurSerializerWithToken(tuteur).data
                for k, v in serializer.items():
                    data[k] = v
                return data
            else:
                return {"message" : "username et/ou mot de passe incorrect"}


        if professeur:
            if professeur.check_password(attrs['password']):
                serializer = ProfesseurSerializerWithToken(professeur).data
                for k, v in serializer.items():
                    data[k] = v
                return data
            else:
                return {"message" : "username et/ou mot de passe incorrect"}

        
        return {"message" : "username et/ou mot de passe incorrect"} 
         
@method_decorator(csrf_exempt, name='dispatch')
class MyTokenObtainPairViews(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def tuteurs(request, pk=None):
    if pk is None:
        tuteurs = Tuteur.objects.all()
        serializer = TuteurSerializer(tuteurs, many=True)
        return Response(serializer.data)
    else:
        try:
            tuteur = Tuteur.objects.get(pk=pk)
            serializer = TuteurSerializer(tuteur, many=False)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            message = {'message' : 'tuteur inexistant'}
            return Response(message, status=status.HTTP_404_NOT_FOUND) 
        except:
            message = {'message' : 'Un problème est survenu !, veuillez réessayer'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)      



@api_view(['GET'])
def professeurs(request, pk=None):
    if pk is None:
        professeurs = Professeur.objects.all()
        serializer = ProfesseurSerializer(professeurs, many=True)
        return Response(serializer.data)
    else:
        try:
            professeur = Professeur.objects.get(pk=pk)
            serializer = ProfesseurSerializer(professeur, many=False)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            message = {'message' : 'professeur inexistant'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)    
        except:
            message = {'message' : 'Un problème est survenu !, veuillez réessayer'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def eleves(request, pk=None):
    if pk is None:
        eleves = Eleve.objects.all()
        serializer = EleveSerializer(eleves, many=True)
        return Response(serializer.data)
    else:
        try:
            eleve = Eleve.objects.get(pk=pk)
            serializer = EleveSerializer(eleve, many=False)
            return Response(serializer.data)
        except ObjectDoesNotExist:
            message = {'message' : 'eleve inexistant'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)  
        except:
            message = {'message' : 'Un problème est survenu !, veuillez réessayer'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)    
        

@api_view(['POST'])
def registerEleve(request):
    data = request.data
    try:
        tuteur = Tuteur.objects.get(username=request.user.username,password=request.user.password)
    except:
        return Response({"message":"Veuillez vous connecter en tant que tuteur"})

    eleve = Eleve.objects.create(
        nom = data['nom'],
        prenom = data['prenom'],
        date_naissance = data['date_naissance'],
        classe = data['classe'],
        ecole = data['ecole'],
        difficulte = data['difficulte'],
        lieu_travail = data['lieu_travail'],
        idtuteur = tuteur
    )
    serializer = EleveSerializer(eleve, many=False)
    return Response(serializer.data)

@api_view(['POST'])
def registerTuteur(request):
    data = request.data
    try:
        tuteur = Tuteur.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['email'],
            email=data['email'],
            password= make_password(data['password']),
            profession=data['profession']
        )
        serializer = TuteurSerializerWithToken(tuteur, many=False)
        return Response(serializer.data)
    except:
        message = {'message' : 'Un utilisateur avec cet email existe déjà'}
        return Response(message)


@api_view(['POST'])
def registerProfesseur(request):
    data = request.data 
    professeur = Professeur.objects.create(
        first_name=data['first_name'],
        last_name=data['last_name'],
        username=data['email'],
        email=data['email'],
        password= make_password(data['password']),
        date_naissance = data['date_naissance'],
        adresse = data['adresse'],
        statut = data['statut'],
        universite = data['universite'],
        filiere_etude = data['filiere_etude'],
        annee_etude = data['annee_etude'],
        dernier_diplome = data['dernier_diplome'],
        filiere_dernier_diplome = data['filiere_dernier_diplome'],
        jours_disponibles = data['jours_disponibles'],
        matieres_generales_enseignables = data['matieres_generales_enseignables'],
        classes_generales_enseignables = data['classes_generales_enseignables'],
        classes_techniques_enseignables = data['classes_techniques_enseignables'],
        matieres_techniques_enseignables = data['matieres_techniques_enseignables'],
        zones_travail = data['zones_travail'],
        periode_journee = data['periode_journee'],
        piece_jointe = data['piece_jointe']
    )
    serializer = ProfesseurSerializerWithToken(professeur, many=False)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

