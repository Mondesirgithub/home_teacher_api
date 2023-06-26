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
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response
from django.utils.html import strip_tags


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)        
            tuteur = Tuteur.objects.filter(username=attrs['username']).first()
            professeur = Professeur.objects.filter(username=attrs['username']).first() 

            if not professeur.estActif:
                return {'message':"Compte inactif,car vous n'avez pas encore passé l'entretien"}
            
            if tuteur and tuteur.check_password(attrs['password']):
                serializer = TuteurSerializerWithToken(tuteur).data
                for k, v in serializer.items():
                    data[k] = v
                return data
            

            if professeur and professeur.check_password(attrs['password']):
                serializer = ProfesseurSerializerWithToken(professeur).data
                for k, v in serializer.items():
                    data[k] = v
                return data

        except:
            return {'message':'username et/ou mot de passe incorrect'}
         
class MyTokenObtainPairViews(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    

@api_view(['GET'])
def tuteurExiste(request, username):
    try:
        tuteur = Tuteur.objects.get(username=username)
        return Response({'existe':1})
    except:
        return Response({'existe':0})

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
        if request.user.is_anonymous:
            tuteur = Tuteur.objects.get(pk=data['tuteur'])
        else:
            tuteur = Tuteur.objects.get(username=request.user.username,password=request.user.password)
    except:
        return Response({"message":"Veuillez vous connecter en tant que tuteur"})

    eleve = Eleve.objects.create(
        nom = data['nom'],
        prenom = data['prenom'],
        date_naissance = data['date_naissance'],
        classe = data['classe'],
        matieres=data['matieres'],
        periode_journee=data['periode_journee'],
        jours_disponibles=data['jours_disponibles'],
        ecole = data['ecole'],
        sexe = data['sexe'],
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
            telephone1=data['telephone1'],
            telephone2=data['telephone2'],
            email=data['email'],
            password= make_password(data['password']),
            profession=data['profession']
        )
        serializer = TuteurSerializerWithToken(tuteur, many=False)
        return Response(serializer.data)
    except:
        message = {'message' : 'Un utilisateur avec cet email ou ce numero de telephone existe déjà'}
        return Response(message)

@api_view(['POST'])
def registerProfesseur(request):
    data = request.data

    if Professeur.objects.filter(last_name=data['last_name']).exists() or Tuteur.objects.filter(last_name=data['last_name']).exists():
        message = {'message' : 'Un utilisateur avec ce nom existe déjà'}
        return Response(message)
    
    if Professeur.objects.filter(email=data['email']).exists():
        return Response({'message': 'Un utilisateur avec cette adresse e-mail existe déjà.'}, status=status.HTTP_400_BAD_REQUEST)

    # Vérifier si le numéro de téléphone existe déjà
    if Professeur.objects.filter(telephone1=data['telephone1']).exists() or Professeur.objects.filter(telephone2=data['telephone2']).exists():
        return Response({'message': 'Un utilisateur avec ce numéro de téléphone existe déjà.'}, status=status.HTTP_400_BAD_REQUEST)


    try:
        professeur = Professeur.objects.create(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['email'],
            email=data['email'],
            sexe = data['sexe'],
            telephone1=data['telephone1'],
            telephone2=data['telephone2'],
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
            periode_journee = data['periode_journee'],
            piece_jointe = data['piece_jointe']
        )
        serializer = ProfesseurSerializerWithToken(professeur, many=False)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        # Gérer toutes les autres exceptions génériques ici
        return Response({'message': f'Une erreur s\'est produite lors de la création du professeur : {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
def contact(request):
    nom = request.data['nom']
    sujet = request.data['sujet']
    email = request.data['email']
    message = request.data['message']
    subject = "Contact"
    template = 'comptes/contactEmail.html'
    context = {'nom': nom, 'sujet':sujet, 'email':email, 'message':message}
    html_message = render_to_string(template, context)
    plain_message = strip_tags(html_message)  # Version texte brut du message
    recipient_list = [settings.EMAIL_HOST_USER]
    try:
        send_mail(subject, plain_message, email, recipient_list, html_message=html_message)                
        message = {'message' : 'success'}
        return Response(message)    
    except:
        message = {'message' : 'erreur'}
        return Response(message)        