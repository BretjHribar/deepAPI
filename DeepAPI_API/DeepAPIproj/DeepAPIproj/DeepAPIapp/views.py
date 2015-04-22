from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from DeepAPIproj.DeepAPIapp.serializers import UserSerializer, GroupSerializer, ImageClassifySerializer

from rest_framework.response import Response
from rest_framework import serializers, views

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ImageClassifyView(views.APIView):
    print "IN GET!"
    def get(self, request, format=None):
        # Validate the incoming input (provided through query parameters)
	print "IN GET2!"
	#authentication_classes = (authentication.TokenAuthentication,)
	#permission_classes = (permissions.IsAdminUser,)

        serializer = ImageClassifySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # Get the model input
        data = serializer.validated_data
        model_input = data["model_input"]

        # Perform the complex calculations
        complex_result = 10 #model_input + "abc"

        # Return it in your custom format
        return Response({
            "complex_result": complex_result,
        }) 
