from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.request import Request
from .filters import ProductFilter
from .models import Product, ProductImage
from rest_framework.decorators import api_view
from .serializer import ProductImageSerialize, ProductSerialize
from rest_framework.pagination import PageNumberPagination
import boto3
from rest_framework import status

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


# Create your views here.


@api_view(http_method_names=["GET"])
def get_products(request):

    filterset = ProductFilter(
        data=request.GET, queryset=Product.objects.all().order_by("id")
    )

    count = filterset.qs.count()

    # pagination
    resPerPage = 1

    paginator = PageNumberPagination()
    paginator.page_size = resPerPage

    queryset = paginator.paginate_queryset(filterset.qs, request=request)

    serializer = ProductSerialize(queryset, many=True)
    return Response(
        {"count": count, "resPerpage": resPerPage, "Products": serializer.data}
    )


@api_view(http_method_names=["GET"])
def get_product(request, pk):
    product = get_object_or_404(Product, id=pk)
    serializer = ProductSerialize(product, many=False)
    return Response({"Product": serializer.data})


@api_view(http_method_names=["POST"])
def upload_product_image(request):

    data = request.data
    files = request.FILES.getlist("image")

    images = []
    for f in files:
        image = ProductImage.objects.create(product=Product(data["product"]), image=f)
        images.append(image)

    serializer = ProductImageSerialize(images, many=True)

    return Response(serializer.data)


@api_view(http_method_names=["GET", "POST"])
def Radhas(request: Request) -> Response:

    table = get_user_table("Radha")

    if request.method == "GET":
        radha = table.scan()
        return Response({"Items": radha.get("Items")})
    elif request.method == "POST":
        try:
            table.put_item(Item=request.data)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(
                data={"error", "Failed to insert"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(http_method_names=["GET", "PUT", "DELETE"])
def radha(request, name):

    table = get_user_table("Radha")

    if request.method == "GET":
        radha = table.get_item(Key={"name": name})
        if radha.get("Item") is not None:
            return Response(data={"Item": radha.get("Item")})
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

    elif request.method == "PUT":
        try:
            table.put_item(Item=request.data)
            return Response(status=status.HTTP_201_CREATED)
        except:
            return Response(
                data={"error", "Failed to Update"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
