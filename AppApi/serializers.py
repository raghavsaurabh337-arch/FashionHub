from .models import Register, Product,Cart
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Register
        fields = '__all__' 
    def validate_email(self, value):
        if not value.lower().endswith("@gmail.com"):
            raise serializers.ValidationError(
                "Email must end with @gmail.com"
            )
        return value

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

# class CartSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Cart
#         fields = '__all__'