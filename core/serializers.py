from rest_framework.serializers import ModelSerializer
from .models import User,Book
from rest_framework import serializers
from rest_framework import serializers
from .models import Borrow,Review

class UserSerializer(serializers.ModelSerializer):
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES, required=False)

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'name', 'password',"user_type"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user_type = validated_data.pop('user_type', 'regular')
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.user_type = user_type
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr=="user_type":
                pass
            elif attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'quantity']

    def create(self, validated_data):
        #
        if 'published_date' not in validated_data:
            raise serializers.ValidationError({"published_date": "This field is required."})
        
        return Book.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():        
                setattr(instance, attr, value)
        instance.save()
        return instance
    


class BorrowSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    book = BookSerializer()
    class Meta:
        model = Borrow
        fields = ['id', 'user', 'book', 'start_date', 'end_date']

    def create(self, validated_data):
        return Borrow.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
                setattr(instance, attr, value)
        instance.save()
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    book = serializers.ReadOnlyField(source='book.title')

    class Meta:
        model = Review
        fields = ['id', 'user', 'book', 'rating', 'comment', 'created_at']

class AverageRatingSerializer(serializers.ModelSerializer):
    average_rating = serializers.FloatField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'average_rating']