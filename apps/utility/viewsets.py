"""
Basic building blocks for generic class based views.

We don't bind behaviour to http method handlers yet,
which allows mixin classes to be composed in interesting ways.
"""
from __future__ import unicode_literals

from rest_framework import status
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from apps.accounts.messages import ERROR_CODE
from apps.utility.common import CustomResponse
from apps.utility.custom_exception import ValidationError


class CreateModelMixin:
    """
    Create a model instance.
    """

    def create(self, request, *args, **kwargs):
        """
        mixin create method
        :param request: wsgi request
        :param args: argument list
        :param kwargs: keyword argument object
        :return: success message or error
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            serializer.save()
            headers = self.get_success_headers(serializer.data)
            return CustomResponse(
                status=status.HTTP_201_CREATED, detail=None
            ).success_response(data=serializer.data, headers=headers)
        return CustomResponse(
            status=status.HTTP_400_BAD_REQUEST, detail=serializer.errors
        ).error_response()

    @staticmethod
    def get_success_headers(data):
        try:
            return {"Location": str(data[api_settings.URL_FIELD_NAME])}
        except (TypeError, KeyError):
            return {}


class ListModelMixin:
    """
    List a queryset.
    """

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return CustomResponse(status=status.HTTP_200_OK, detail=None).success_response(
            data=serializer.data
        )


class RetrieveModelMixin:
    """
    Retrieve a model instance.
    """

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return CustomResponse(status=status.HTTP_200_OK, detail=None).success_response(
            data=serializer.data
        )


class UpdateModelMixin:
    """
    Update a model instance.
    """

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        if serializer.is_valid(raise_exception=False):
            self.perform_update(serializer)
            if getattr(instance, "_prefetched_objects_cache", None):
                instance._prefetched_objects_cache = {}
            return CustomResponse(
                status=status.HTTP_200_OK, detail=None
            ).success_response(data=serializer.data)
        return CustomResponse(
            status=status.HTTP_400_BAD_REQUEST, detail=serializer.errors
        ).error_response()

    @staticmethod
    def perform_update(serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin:
    """
    Destroy a model instance.
    """

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return CustomResponse(
            status=status.HTTP_204_NO_CONTENT, detail=None
        ).success_response(data=None)


class CustomModelViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    GenericViewSet,
):
    """
    A view-set that provides default `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions, and provide a unique response format .
    """

    pass


class CustomModelPostListViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    """
    A view-set that provides default `create()`, and `list()` actions, and provide a unique response format .
    """

    pass


class CustomModelListViewSet(ListModelMixin, GenericViewSet):
    """
    A view-set that provides default `list()` actions, and provide a unique response format .
    """

    pass


class CustomModelRetrieveViewSet(RetrieveModelMixin, GenericViewSet):
    """
    A view-set that provides default `list()` actions, and provide a unique response format .
    """

    pass


class CustomModelPostViewSet(CreateModelMixin, GenericViewSet):
    """
    A view-set that provides default `create()`, and `list()` actions, and provide a unique response format .
    """

    pass


def error_404(description):
    """function to return error with status code"""
    raise ValidationError(
        detail={
            "detail": {"message": description},
            "status_code": status.HTTP_404_NOT_FOUND,
        },
        status_code=status.HTTP_404_NOT_FOUND,
    )


def get_object_or_404(model, *args, **kwargs):
    """
    return record with(args=kwargs) if available in model
    else return validation error
    :param model:
    :param args:
    :param kwargs:
    :return:
    """
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        raise error_404(description=ERROR_CODE["4011"])


def error_400(description):
    """function to return error with status code"""
    raise ValidationError(
        detail={"data": {"message": description}},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def validation_error(description):
    """
    Raise validation error in formatted dictionary
    """
    return ValidationError(
        {
            "detail": {"message": description}
            if isinstance(description, str)
            else description,
            "status_code": int(status.HTTP_400_BAD_REQUEST),
        }
    )
