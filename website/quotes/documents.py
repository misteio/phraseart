from django_opensearch_dsl import Document, TextField, fields
from django_opensearch_dsl.registries import registry
from elasticsearch_dsl import analyzer, tokenizer
from .models import Quote


french_analyzer = analyzer('french_analyzer',
                           tokenizer=tokenizer('trigram', 'ngram', min_gram=3, max_gram=3),
                           filter=['lowercase']
                           )

@registry.register_document
class QuoteDocument(Document):
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
        settings = {
            'number_of_shards': 2,
            'number_of_replicas': 1,
            'analysis': {
                'analyzer': {
                    'french_analyzer': {
                        'type': 'custom',
                        'tokenizer': 'trigram',
                        'filter': ['lowercase']
                    }
                },
                'tokenizer': {
                    'trigram': {
                        'type': 'ngram',
                        'min_gram': 3,
                        'max_gram': 3
                    }
                }
            }
        }

    class Django:
        model = Quote # The model associated with this Document

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'created_at',
            'updated_at',
            'slug',
            'id',
            'body'
        ]

    def prepare_author(self, instance):
        return instance.author.name

    def prepare_author_slug(self, instance):
        return instance.author.slug

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