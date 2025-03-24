from rest_framework import serializers
from django.utils.html import strip_tags

from accounts.models import Profile
from ...models import Post, Category


""" model serializer for Post """
class PostSerializer(serializers.ModelSerializer):
    """ a read only field to get the url of duty instance """
    absolute_url = serializers.SerializerMethodField()

    """ a field to show a summary of content in list page """
    snippet = serializers.SerializerMethodField()

    """ a slug field to show category by name """
    category = serializers.SlugRelatedField(
        many=True,
        queryset=Category.objects.all(),
        slug_field='name',
    )

    author = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id',
            'author',
            'title',
            'image',
            'snippet',
            'absolute_url',
            'content',
            'status',
            'counted_views',
            'category',
            'created_date',
            'updated_date',
            'published_date',
            ]
        read_only_fields = ['author', 'status', 'counted_views',]

    
    def get_absolute_url(self, post):
        request = self.context.get('request')
        return request.build_absolute_uri(post.pk)
    
    def get_author(self, post):
        return post.author.user.email

    
    def get_snippet(self, obj):
        """ Remove HTML tags from snippet """
        return strip_tags(' '.join(obj.content.split()[:10]) + '...')
    
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
            rep.pop('content', None)

        return rep
    
    """ override create method in order to get the author from authentication data """
    def create(self, validated_data):
        validated_data['author'] = Profile.objects.get(user__id = self.context.get("request").user.id)
        return super().create(validated_data)
    
    """ override update method in order to set the status to 'draft' !! Just admin in admin panel is able to set status to 'published' """
    def update(self, instance, validated_data):
        validated_data['status'] = 'drf'
        return super().update(instance, validated_data)
    

