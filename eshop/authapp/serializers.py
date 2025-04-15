from rest_framework import serializers
import boto3
from botocore.exceptions import ClientError
import os
import dotenv

dotenv.load_dotenv()

# AWS Credentials
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY_ID = os.environ.get("AWS_SECRET_ACCESS_KEY_ID")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")


# Helper to access DynamoDB table
def get_user_table(table_name: str):
    dynamodb = boto3.resource(
        "dynamodb",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY_ID,
        region_name=AWS_S3_REGION_NAME,
    )
    return dynamodb.Table(table_name)


class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        table = get_user_table("User")
        try:
            print(
                {
                    "email": validated_data["email"],
                    "password": validated_data[
                        "password"
                    ],  # Use hashed password in prod
                    "is_verified": False,
                }
            )
            table.put_item(
                Item={
                    "email": validated_data["email"],
                    "password": validated_data[
                        "password"
                    ],  # Use hashed password in prod
                    "is_verified": False,
                }
            )

        except ClientError as e:
            raise serializers.ValidationError("Could not save user.")
        return validated_data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        table = get_user_table("User")
        response = table.get_item(Key={"email": data["email"]})
        user = response.get("Item")
        if not user or user["password"] != data["password"]:
            raise serializers.ValidationError("Invalid credentials.")
        if not user.get("is_verified", False):
            raise serializers.ValidationError("Email not verified.")
        return data


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
