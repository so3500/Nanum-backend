from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F
from logging import warning

from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.views import APIView

import logging

from study.models import *
from study.serializer import *
from accounts.serializer import *
#from study.models import *

"""
    The @api_view decorator for working with function based views.
    The APIView class for working with class-based views.
"""
"""
    ModelViewSet - list, create, retrieve, update, destroy 기능을 자동으로 지원
"""


@permission_classes((AllowAny,))
class StudyViewSet(viewsets.ModelViewSet):

    queryset = Study.objects.all()
    serializer_class = StudySerializer


@permission_classes((AllowAny,))
class StudyMemberViewSet(viewsets.ModelViewSet):
    queryset = StudyMember.objects.all()
    serializer_class = StudyMemberGetSerializer

    def _get_serializer(self, *args, **kwargs):
        serializer_class = StudyMemberSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        # request POST 요청에 포함된 data얻는 법
        # study 멤버 수 +1
        study_id = request.POST.__getitem__('study')
        study = get_object_or_404(Study, pk=study_id)
        study.joined_user_count += 1
        study.save()

        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

# override
    def destroy(self, request, *args, **kwargs):
        # study 멤버 수 -1
        study_id = request.POST.__getitem__('study')
        study = get_object_or_404(Study, pk=study_id)
        study.joined_user_count -= 1
        study.save()
        return super(StudyMemberViewSet, self).destroy(request, *args, **kwargs)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = StudyLike.objects.all()
    serializer_class = StudyLikeSerializer


# ===================================================
# ============== Board ==============
# ===================================================
@permission_classes((AllowAny,))
class BoardViewSet(viewsets.ModelViewSet):
    queryset = Board.objects.all()
    serializer_class = BoardGetSerializer

    def _get_serializer(self, *args, **kwargs):
        serializer_class = BoardSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# ===================================================
# ============== type 0 : BasicBoard ==============
# ===================================================
@permission_classes((AllowAny,))
class BasicBoardViewSet(viewsets.ModelViewSet):
    queryset = BasicBoard.objects.all()
    # get 시리얼라이저
    serializer_class = BasicBoardGetSerializer

    # override GenericAPIView.get_serializer
    def _get_serializer(self, *args, **kwargs):
        # create, update 시리얼라이저
        serializer_class = BasicBoardSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  #
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class BasicBoardCommentViewSet(viewsets.ModelViewSet):
    queryset = BasicBoardComment.objects.all()
    serializer_class = BasicBoardGetCommentGetSerializer

    # override GenericAPIView.get_serializer
    def _get_serializer(self, *args, **kwargs):
        serializer_class = BasicBoardCommentSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  #
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class BasicBoardFileViewSet(viewsets.ModelViewSet):
    queryset = BasicBoardFile.objects.all()
    serializer_class = BasicBoardFileGetSerializer

    # override
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 다운로드 수 증가 및 적용
        instance.download_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # override
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()     # file 관련 인스턴스 개체 삭제
        instance.attached_file.delete()  # 실제 file 삭제
        return super(BasicBoardFileViewSet, self).destroy(request, *args, **kwargs)


# ===================================================
# ============== type 1 : Reference ==============
# ===================================================
@permission_classes((AllowAny,))
class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceGetSerializer

    """
    get_serializer 함수만 오버라이딩 할 경우 GET할때도 create전용 serializer가 반영되서
    연관된 달력의 세부정보, 사용자, 스터디 정보에 대한 세부정보를 알 수 없다.
    따라서 create, get_serializer 함수를 같이 오버라이딩 해줘야 한다.
    """
    def _get_serializer(self, *args, **kwargs):
        # serializer_class = self.get_serializer_class()
        serializer_class = ReferenceSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        # warning("Reference create : " + str(request.data))
        # warning("ReferenceSerializer : " + str(self.serializer_class.Meta.fields))
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # warning("serializer ReferenceCreateSerializercreate : " + str(serializer.validated_data))
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        # return super(ReferenceViewSet, self).create(request, *args, **kwargs)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class ReferenceFileViewSet(viewsets.ModelViewSet):
    queryset = ReferenceFile.objects.all()
    serializer_class = ReferenceFileGetSerializer

    def _get_serializer(self, *args, **kwargs):
        # serializer_class = self.get_serializer_class()
        serializer_class = ReferenceFileSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 다운로드 수 증가 및 적용
        instance.download_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        instance.attached_file.delete()  # 실제 file 삭제
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    # override
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()    # file 관련 객체 삭제(super에서)
        instance.attached_file.delete() # 실제 file 삭제
        return super(ReferenceFileViewSet, self).destroy(request, *args, **kwargs)

    # issue?! : 오버라이딩은 어떻게 하는게 효율적이고 가독성 좋은 코드가 나올까?
    # def destroy(self, request, *args, **kwargs):
    #     instance = self.get_object()
    #     self.perform_destroy(instance)
    #     return Response(status=status.HTTP_204_NO_CONTENT)
    #
    # def perform_destroy(self, instance):
    #     instance.attached_file.delete() # file 삭제 코드
    #     instance.delete()

# ===================================================
# ============== type 3 : Verificaiton ==============
# ===================================================
@permission_classes((AllowAny,))
class VerificationViewSet(viewsets.ModelViewSet):
    queryset = Verification.objects.all()
    serializer_class = VerificationGetSerializer

    # override GenericAPIView.get_serializer
    def _get_serializer(self, *args, **kwargs):
        serializer_class = VerificationSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)  #
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class VerificationFileViewSet(viewsets.ModelViewSet):
    queryset = VerificationFile.objects.all()
    serializers_class = VerificationFileGetSerializer

    # override
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # 다운로드 수 증가 및 적용
        instance.download_count += 1
        instance.save()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    # override
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()     # file 관련 인스턴스 개체 삭제
        instance.attached_file.delete()  # 실제 file 삭제
        return super(VerificationFileViewSet, self).destroy(request, *args, **kwargs)


# ===================================================
# ============== type 4 : Calendar ==============
# ===================================================
@permission_classes((AllowAny,))
class CalendarViewSet(viewsets.ModelViewSet):
    queryset = Calendar.objects.all()
    serializer_class = CalendarGetSerializer

    # GenericAPIView 에 똑같은 이름의 함수가 있다.
    def _get_serializer(self, *args, **kwargs):
        serializer_class = CalendarSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) #
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


@permission_classes((AllowAny,))
class CalendarTagViewSet(viewsets.ModelViewSet):
    queryset = CalendarTag.objects.all()
    serializer_class = CalendarTagGetSerializer

    def _get_serializer(self, *args, **kwargs):
        serializer_class = CalendarTagSerializer
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    # override ModelViewSet.CreateModelMixin.create
    def create(self, request, *args, **kwargs):
        # 인스턴스 생성 시 사용되는 시리얼라이저를 바꾼다.
        serializer = self._get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    # override ModelViewSet.UpdateModelMixin.update
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False) #
        instance = self.get_object()
        serializer = self._get_serializer(instance, data=request.data, partial=partial) #
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


# ===================================================
# ============== StudyLike ==============
# ===================================================
# 스터디 좋아요 생성
@api_view(['POST'])
@permission_classes((AllowAny,))
def study_like_create(request, study_pk=None, format=None):
    if request.method == 'POST':
        logging.warning("request.data : " + str(request.data), )
        #logging.warning("request.data.__getitem__ :" + str(request.POST.__getitem__),)

        # issue?! : 스터디 좋아요는 한명의 사용자에 대해서 하나만 생성 - 프론트에서
        # issue?! : 스터디 '가'에 대해 좋아요를 누른 사용자A가 스터디 '가' 페이지를 띄울때, 좋아요 정보를 GET해서 뿌려줘야 하나?

        # Like instance 생성할 때 인자로 받은 study_pk 값을 request.POST 에 추가
        # request.POST.__setitem__('study', study_pk)
        # study 좋아요  수 증가 및 적용
        study = get_object_or_404(Study, pk=study_pk)
        study.like_count += 1
        study.save()
        # logging.warning("study_like : " + str(study.like_count), )
        serializer = StudyLikeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # logging.warning(request.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer@permission_classes((AllowAny,)).errors, status=status.HTTP_400_BAD_REQUEST)


# 스터디 좋아요 삭제
@api_view(['DELETE'])
@permission_classes((AllowAny,))
def study_like_delete(request, study_pk=None, like_pk=None, format=None):
    if request.method == 'DELETE':
        # study 좋아요 수 감소 및 적용
        study = get_object_or_404(Study, pk=study_pk)
        study.like_count -= 1
        study.save()

        # 해당 like 인스턴스 삭제
        like = get_object_or_404(StudyLike, pk=like_pk)
        like.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ===================================================
# ============== BasicBoardLike ==============
# ===================================================
# 게시글 좋아요 수 증가
# @api_view(['PUT', 'PATCH'])
# @permission_classes((AllowAny,))
# def basic_board_like_create(request, basic_board_pk=None, format=None):
#     if request.method == 'PUT' or 'PATCH':
#         # Like instance 생성할 때 인자로 받은 basic_board_pk 값을 request.POST 에 추가
#         request.POST.__setitem__('basic_board', basic_board_pk)
#         # study 좋아요  수 증가 및 적용
#         basic_board = get_object_or_404(BasicBoard, pk=basic_board_pk)
#         basic_board.like_count += 1
#         basic_board.save()


# # 게시글 좋아요 수 감소
# @api_view(['PUT'])
# @permission_classes((AllowAny,))
# def basic_board_like_delete(request, basic_board_pk=None, like_pk=None, format=None):
#     if request.method == 'PUT' or 'PATCH':
#         # basic_board 좋아요 수 감소 및 적용
#         basic_board = get_object_or_404(BasicBoard, pk=basic_board_pk)
#         basic_board.like_count -= 1
#         basic_board.save()
#
#         # 해당 basic_board like 인스턴스 삭제
#         like = get_object_or_404(StudyLike, pk=like_pk)
#         like.delete()
#         return Response(status=status.HTTP_20)



# 최근 게시물 조회
# 나중에
# @api_view(['GET'])
# def lastest(request, study_pk=None):
#     pass