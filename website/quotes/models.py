from django.core.validators import MinLengthValidator
from core.mixins import Timestamped
from django.db import models
from django.utils.text import slugify
from imagekit.models import ProcessedImageField
import uuid
from django.urls import reverse
from django_random_queryset import RandomManager
from imagekit.processors import ResizeToFit
from django.utils.html import format_html
from io import BytesIO
from .utils import create_image_from_text
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys
import re

class Author(Timestamped):
    name = models.CharField(max_length=120, unique=True, validators=[MinLengthValidator(3)])
    slug = models.SlugField(max_length=120, unique=True, editable=False)
    bio = models.TextField(null=True, blank=True)
    # Managers
    objects = models.Manager()  # The default manager.
    image = ProcessedImageField(blank=True, upload_to='images/bio/',
                                processors=[ResizeToFit(500, 500)],
                                format='JPEG',
                                options={'quality': 90})

    class Meta:
        ordering = ('-name',)

    def get_absolute_url(self):
        return reverse('quote_author_list', kwargs={'author_slug': self.slug})

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Author, self).save(*args, **kwargs)


class FileImage(Timestamped):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    file = ProcessedImageField(blank=True, upload_to='images/%Y/%m/%d/', processors=[ResizeToFit(2000, 2000)],
                               format='JPEG',
                               options={'quality': 90})
    # Managers
    objects = models.Manager()  # The default manager.

    class Meta:
        ordering = ('created_at',)

    @property
    def thumbnail_preview(self):
        return format_html(
            '<img src="{}">'.format(self.file_thumbnail_250.url))

    def __str__(self):
        return str(self.uuid)


class Tag(Timestamped):
    name = models.CharField(max_length=100, unique=True, validators=[MinLengthValidator(3)])
    slug = models.SlugField(max_length=100, unique=True, editable=False)

    # Managers
    objects = models.Manager()  # The default manager.

    class Meta:
        ordering = ('-name',)

    def get_absolute_url(self):
        return reverse('quote_tag_list', kwargs={'tag_slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class Blacklist(Timestamped):
    name = models.CharField(max_length=100, unique=True)
    original_name = models.CharField(max_length=100, unique=True)
    # Managers
    objects = models.Manager()  # The default manager.

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name


class Missed(Timestamped):
    name = models.CharField(max_length=100, unique=True)
    original_name = models.CharField(max_length=100, unique=True)
    # Managers
    objects = models.Manager()  # The default manager.

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name


class QuoteModelManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(file_image__isnull=False).prefetch_related('tags').select_related(
            'author').select_related('file_image')


class RandomModelManager(RandomManager):
    def get_queryset(self):
        return super().get_queryset().filter(file_image__isnull=False).prefetch_related('tags').select_related(
            'author').select_related('file_image')


class Quote(Timestamped):
    title = models.CharField(max_length=255, unique=True, validators=[MinLengthValidator(4)])
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    author = models.ForeignKey(Author, related_name='author_quote', on_delete=models.CASCADE, )
    file_image = models.ForeignKey(FileImage, related_name='file_image_quote', on_delete=models.CASCADE, blank=True,
                                   null=True)
    body = models.TextField()
    analyze = models.TextField(blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    tags = models.ManyToManyField(Tag)
    image_square = models.ImageField(blank=True, upload_to='images/generated/%Y/%m/%d/')
    image_vertical = models.ImageField(blank=True, upload_to='images/generated/%Y/%m/%d/')
    image_horizontal = models.ImageField(blank=True, upload_to='images/generated/%Y/%m/%d/')
    explicit_text = models.BooleanField(default=False)
    slider_selected = models.BooleanField(default=False)
    featured_selected = models.BooleanField(default=False)
    sub_slider_selected = models.BooleanField(default=False)
    # Managers
    objects = QuoteModelManager()
    random_objects = RandomModelManager()
    raw_objects = models.Manager()

    class Meta:
        ordering = ('-title',)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.body = re.sub(r'<.*?>', '', self.body)

        image_square = self.create_thumb(create_image_from_text(self, 1080, 1080, 48, self.uuid, 40, 350),'square')
        self.image_square = image_square

        image_vertical = self.create_thumb(create_image_from_text(self, 1080, 1920, 68, self.uuid, 52, 600), 'horizontal')
        self.image_vertical = image_vertical

        image_horizontal = self.create_thumb(create_image_from_text(self, 1224, 472, 40, self.uuid, 35, 250), 'vertical')
        self.image_horizontal = image_horizontal


        super(Quote, self).save(*args, **kwargs)

    def tag_names(self):
        return [str(tag) for tag in self.tags.all()]

    def author_name(self):
        return self.author.name

    def get_absolute_url(self):
        return reverse('quote_single', kwargs={'author_slug': self.author.slug, 'quote_slug': self.slug})

    def create_thumb(self, image, orientation):
        blob = BytesIO()
        image.save(blob, 'JPEG')
        blob.seek(0)  # Rewind the file pointer to the beginning of the file
        # Option 2: Wrap the BytesIO object in InMemoryUploadedFile
        image_file = InMemoryUploadedFile(blob, None, f"{str(self.uuid) + '-' + orientation}.jpg", 'image/jpeg', sys.getsizeof(blob), None)

        return image_file