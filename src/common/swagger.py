from drf_yasg.inspectors import SwaggerAutoSchema


class CustomSwaggerAutoSchema(SwaggerAutoSchema):
    def get_tags(self, operation_keys=None):
        operation_keys = operation_keys or self.operation_keys

        tags = self.overrides.get('tags')
        if not tags:
            tags = [f"{operation_keys[0]}-{operation_keys[1]}"]
        if hasattr(self.view, "swagger_tags"):
            tags = self.view.swagger_tags

        return tags
