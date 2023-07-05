from rest_framework import serializers
from proposal.models import Proposal

from user_profile.models import UserProfile
from user_profile.serializers import UserProfileSerializer

from .models import Petition


class PetitionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField('getImage')
    user = serializers.SerializerMethodField('getUser')
    proposals = serializers.SerializerMethodField('getProposals')
    date = serializers.SerializerMethodField('getDate')

    class Meta:
        model = Petition
        fields = (
            "id",
            "user",
            "image",
            "dimension",
            "text",
            "font",
            "color",
            "date",
            "proposals"
        )
        
    def getDate(self,obj):
        return obj.date.strftime("%y%m%d%H%M%S")

    def getImage(self,obj):
        return obj.getImage()

    def getUser(self,obj):       
        user_profile = UserProfile.objects.get(user=obj.user)
        user_profile = UserProfileSerializer(user_profile).data
        return user_profile
        
    def getProposals(self,obj):
        proposals = Proposal.objects.filter(petition = obj)
        return len(proposals)
        
