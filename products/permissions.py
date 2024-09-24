from rest_framework import permissions

class IsAdminOrSeller(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read permissions for any request
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the admin or the seller
        return request.user.role == 'admin' or obj.items.filter(product__seller=request.user).exists()