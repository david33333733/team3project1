# reviews/permissions.py
from rest_framework import permissions

class IsReviewAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTIONS 요청은 모두 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        # 작성자거나 관리자면 수정/삭제 허용
        return obj.user == request.user or request.user.is_staff
