from django.urls import reverse
from django.db import models
from django.conf import settings
from kitchensink.utils.gootenberg import gootenberg, GootenbergException
from jsonschema import validate


from .base import BaseSink


class Sheet(BaseSink):
    title = models.CharField(
        "Project title", max_length=250, help_text="A title for this sheet"
    )

    project = models.ForeignKey(
        "Project",
        on_delete=models.PROTECT,
        blank=True,
        null=True,
        related_name="sheets",
    )

    favorites = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def serialize(self):
        return {
            "id": self.google_id,
            "title": self.title,
            "publish": reverse("kitchensink-publish-sheet", args=[self.id]),
            "type": "sheet",
            "project": self.project.title if self.project else None,
        }

    def get_data(self):
        try:
            resp = gootenberg('/parse/table/', {"id": self.google_id})
            content = resp.json()
        except GootenbergException:
            content = {}

        if(self.validation_schema):
            validate(content, self.validation_schema)

        return {
            "meta": {
                "source": "kitchensink",
                "version": self.version,
                "lastModified": self.get_last_content_modified(),
                "lastPublished": (
                    self.last_published.isoformat()
                    if self.last_published else None
                ),
                "project": (
                    self.project.title
                    if self.project
                    else None
                )
            },
            "content": content
        }

    def __str__(self):
        return self.title
