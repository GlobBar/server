from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from apiusers.serializers import UserSerializer, GroupSerializer, UserDetailSerializer
from rest_framework import permissions
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from report.models import Report
from report.serializers import ReportSerializer
from report.models import ReportImageLike


class UserList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, format=None):
        users = None
        limit_from = str(request.GET.get('limit_from'))
        limit_count = str(request.GET.get('limit_count'))

        if limit_from == 'None':
            limit_from = '0'
        if limit_count == 'None':
            limit_count = '1000'

        one = int(limit_from)
        two = int(limit_count)
        li = [one, two]
        suuuu = sum(li)

        if 'search' in request.GET:
            search_str = request.GET.get('search')
            if len(search_str) > 0:
                users = User.objects.filter(username__icontains=search_str)[one:suuuu]
        if users is None:

            users = User.objects.all()[one:suuuu]

        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        if pk == 'me':
            user = request.user
        else:
            user = self.get_object(pk)

        serializer = UserDetailSerializer(user)

        # My Report likes
        my_like_report_pks = []
        my_likes_report = ReportImageLike.objects.filter(user=user)
        if my_likes_report.count() > 0:
            for l in my_likes_report:
                my_like_report_pks += [str(l.report.pk)]

        last_reports = Report.objects.filter(user_id=user.pk).order_by('-id')[0:3]
        res_reports_list = []
        for r in last_reports:
            last_reports_seriolaser = ReportSerializer(r, context={'is_hot': True, 'my_like_report_pks': my_like_report_pks}).data
            res_reports_list += [last_reports_seriolaser]

        return Response({'user': serializer.data, 'last_reports': res_reports_list})

    def put(self, request, pk, format=None):
        user = self.get_object(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user = self.get_object(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    # auth
    permission_classes = (permissions.IsAuthenticated,)
    
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
