from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet


class CreateRetrieveUpdateListModelViewSet(
    mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
    mixins.ListModelMixin, GenericViewSet
):
    pass


class CreateModelViewSet(mixins.CreateModelMixin, GenericViewSet):
    pass


class RetrieveUpdateModelViewSet(mixins.RetrieveModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    pass


class CreateListModelViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, GenericViewSet):
    pass


class UpdateModelViewSet(mixins.UpdateModelMixin, GenericViewSet):
    pass


class ListModelViewSet(mixins.ListModelMixin, GenericViewSet):
    pass


class RetrieveListModelViewSet(mixins.RetrieveModelMixin, mixins.ListModelMixin, GenericViewSet):
    pass


class RetrieveUpdateListModelViewSet(
    mixins.RetrieveModelMixin, mixins.UpdateModelMixin, mixins.ListModelMixin, GenericViewSet
):
    pass


class CreateModelWithFixStatusViewSet(CreateModelViewSet):
    fix_status = None

    def create(self, request, *args, **kwargs):
        response = super().create(request=request, args=args, kwargs=kwargs)
        status = self.fix_status or response.status_code

        return Response(response.data, status=status, headers=response.headers)


class CreateUpdateModelWithFixStatusViewSet(mixins.CreateModelMixin, mixins.UpdateModelMixin, GenericViewSet):
    fix_status = None

    def create(self, request, *args, **kwargs):
        response = super().create(request=request, args=args, kwargs=kwargs)
        status = self.fix_status or response.status_code

        return Response(response.data, status=status, headers=response.headers)
