from rest_framework import serializers
from rest_framework.reverse import reverse
from django.utils.html import strip_tags
from django.utils import timezone

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
        # return request.build_absolute_uri(post.pk)
        return reverse("blog:api-v1:post-detail", kwargs={'pk': post.pk}, request=request)
    
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
    

""" model serializer for Category"""
class CategorySerializer(serializers.ModelSerializer):
    """ add a field to show the posts of each category"""
    posts = serializers.SerializerMethodField()

    """ a read only field to get the url of category instance """
    absolute_url = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name','posts', 'absolute_url']

    def get_posts(self, obj):
        posts = Post.objects.filter(status='pub', published_date__lte=timezone.now(), category=obj)
        return [f'{post.title} (post-id = {post.id})' for post in posts]
    
    def get_absolute_url(self, category):
        request = self.context.get('request')
        return reverse("blog:api-v1:category-detail", kwargs={'pk': category.pk}, request=request)

    """ separate representation in list and detail """
    def to_representation(self, instance):
        request = self.context.get('request')

        rep = super().to_representation(instance)

        if request.parser_context.get('kwargs'):
            """ omit absolute_url in detail page """
            rep.pop('absolute_url', None)
        return rep