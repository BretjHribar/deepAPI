from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from DeepAPIproj.DeepAPIapp.serializers import UserSerializer, GroupSerializer, ImageClassifySerializer

from rest_framework.response import Response
from rest_framework import serializers, views

import numpy as np
import caffe
import os , sys
import urllib

import time

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ImageClassifyView(views.APIView):
    def get(self, request, format=None):
	t = time.time() 
        # Validate the incoming input (provided through query parameters)
	#authentication_classes = (authentication.TokenAuthentication,)
	#permission_classes = (permissions.IsAdminUser,)

        serializer = ImageClassifySerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)

        # Get the model input
        data = serializer.validated_data

	image_url = data["image_url"]
################################################################################
	CLASSIFY_MAP_FILE = os.path.join(os.getcwd(), "./DeepAPIproj/DeepAPIapp/deepModels/python/models/imagenet2012caffeClassMap.txt" )
    	MODEL_FILE = os.path.join(os.getcwd(), "./DeepAPIproj/DeepAPIapp/deepModels/python/models/deploy.prototxt" )
    	PRETRAINED = os.path.join(os.getcwd(), "./DeepAPIproj/DeepAPIapp/deepModels/python/models/bvlc_reference_caffenet.caffemodel" )
    	IMAGE_FILE = os.path.join(os.getcwd(), "./DeepAPIproj/DeepAPIapp/deepModels/python/images/cat.jpg" )
	IMAGE_MEAN = os.path.join(os.getcwd(), "./DeepAPIproj/DeepAPIapp/deepModels/python/models/ilsvrc_2012_mean.npy")
	IMAGE_FILE2 = os.path.join(os.getcwd(), "./DeepAPIproj/DeepAPIapp/deepModels/python/images/tiger4.jpg" )
	IMAGE_URL  = "http://store.storeimages.cdn-apple.com/4572/as-images.apple.com/is/image/AppleInc/aos/published/images/i/ph/iphone6/plus/iphone6-plus-box-space-gray-2014?wid=478&hei=595&fmt=jpeg&qlt=95&op_sharpen=0&resMode=bicub&op_usm=0.5,0.5,0,0&iccEmbed=0&layer=comp&.v=1411520743411"	

	print "image_url" + image_url
	image_filename, headers  = urllib.urlretrieve(image_url)

	#caffe.set_mode_cpu()
	caffe.set_mode_gpu()

	net = caffe.Classifier(MODEL_FILE, PRETRAINED,
		           mean=np.load(IMAGE_MEAN).mean(1).mean(1),
		           channel_swap=(2,1,0),
		           raw_scale=255,
		           image_dims=(256, 256))
	input_image = caffe.io.load_image(image_filename)

	model_time = time.time()
	prediction = net.predict([input_image])  # predict takes any number of images, and formats them for the Caffe net automatically
	model_execute_time = time.time() - model_time
	
	print 'prediction shape:', prediction[0].shape
	print 'predicted class:', prediction[0].argmax()

	image_class = prediction[0].argmax()
	#print "prediction: " + repr(prediction.size)
#####################################################################################

	imageClassMap = {}
	counter = 0
	with open(CLASSIFY_MAP_FILE) as f:
	    for line in f:
	    	val = line.split(None, 1)
		v = val[1].strip('\n')
	    	imageClassMap[int(counter)] = v
		counter += 1

#################################################################################
        return Response({
            "image_class": imageClassMap[image_class],
	    "time_to_execute" : time.time()  - t,
	    "model_execute_time" : model_execute_time
        }) 

