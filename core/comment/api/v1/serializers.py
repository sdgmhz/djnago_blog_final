from rest_framework import serializers
from rest_framework.reverse import reverse
from django.utils import timezone

from ...models import Comment
from blog.models import Post
from accounts.models import Profile


class CommentSerializer(serializers.ModelSerializer):

    """ a read only field to get the url of comment instance """
    absolute_url = serializers.SerializerMethodField()

    """ a field to show a summary of content in list page """
    snippet = serializers.ReadOnlyField(source="get_snippet")

    post = serializers.SlugRelatedField(
        slug_field='title',
        queryset=Post.objects.filter(
            status='pub', published_date__lte=timezone.now())
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'post',
            'name',
            'email',
            'subject',
            'snippet',
            'absolute_url',
            'message',
            'recommend',
            'approved',
            'created_date',
            'updated_date',
        ]
        read_only_fields = ['email', 'approved']

    def __init__(self, *args, **kwargs):
        super(CommentSerializer, self).__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and request.method in ['PUT', 'PATCH']:
            self.fields['post'].read_only = True
            self.fields['email'].read_only = True

    def get_absolute_url(self, post):
        request = self.context.get('request')
        # return request.build_absolute_uri(post.pk)
        return reverse("comment:api-v1:comment-detail", kwargs={'pk': post.pk}, request=request)

    """ separate representation in list and detail """
    def to_representation(self, instance):
        request = self.context.get('request')

        rep = super().to_representation(instance)

        if request.parser_context.get('kwargs'):
            """ omit snippet, content and absolute_url in detail page """
            rep.pop('snippet', None)
            rep.pop('absolute_url', None)
        else:
            """ remove content and clean_content in list """
            rep.pop('message', None)
        return rep

    """ override create method in order to get the email from authentication data """
    def create(self, validated_data):
        validated_data['email'] = Profile.objects.get(
            user__id=self.context.get("request").user.id)
        return super().create(validated_data)

    """ override update method in order to set the approved to False !! Just admin in admin panel is able to set status to 'published' """
    def update(self, instance, validated_data):
        validated_data['approved'] = False
        return super().update(instance, validated_data)
