from django_elasticsearch_dsl import Document, TextField, fields, IntegerField
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, tokenizer

from .models import Quote


@registry.register_document
class QuoteDocument(Document):
    french_analyzer = analyzer('french_analyzer',
                               tokenizer=tokenizer('trigram', 'ngram', min_gram=3, max_gram=3),
                               filter=['lowercase']
                               )
    author = TextField()
    author_slug = TextField()
    all_fields = fields.TextField(
        analyzer=french_analyzer
    )
    all_fields_suggest = fields.TextField()

    class Index:
        # Name of the Elasticsearch index
        name = 'quotes'
        # See Elasticsearch Indices API reference for available settings
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}

    class Django:
        model = Quote # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'created_at',
            'updated_at',
            'slug',
            'id',
            'body',
            'lang'
        ]

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(file_image__isnull=False)

    def prepare_author(self, instance):
        return instance.author.name

    def prepare_author_slug(self, instance):
        return instance.author.slug

    def prepare_file_image_thumbnail_250(self, instance):
        return instance.file_image.file_thumbnail_250.file.name

    def prepare_all_fields(self, instance):
        all = instance.author.name + " " + instance.body
        for tag in instance.tags.all():
            all = all + " " + tag.name
        return  all

    def prepare_all_fields_suggest(self, instance):
        all = instance.author.name + " " + instance.body
        for tag in instance.tags.all():
            all = all + " " + tag.name
        return  all