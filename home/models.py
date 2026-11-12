from django.db import models

from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page
from wagtail.snippets.models import register_snippet


# ---------------------------------------------------------------
# Bloc 1 : présentation (texte à gauche, image à droite)
# ---------------------------------------------------------------
class PresentationBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=False, max_length=150, label="Titre")
    text = blocks.RichTextBlock(
        features=["bold", "italic", "link", "ol", "ul"],
        label="Texte",
    )
    image = ImageChooserBlock(label="Image")
    alt_text = blocks.CharBlock(
        required=False,
        max_length=200,
        label="Description de l'image",
        help_text="Une phrase qui décrit l'image. Vide si elle est décorative.",
    )

    class Meta:
        icon = "image"
        label = "Présentation (texte + image)"



# ---------------------------------------------------------------
# Bloc 2 : une carte de phase
# ---------------------------------------------------------------
class PhaseCardBlock(blocks.StructBlock):
    phase = blocks.ChoiceBlock(
        choices=[
            ("soleil", "Soleil – Rémission"),
            ("nuages", "Nuages – Vigilance"),
            ("tempete", "Tempête – Alerte"),
        ],
        label="Phase",
    )
    image = ImageChooserBlock(label="Image de la phase")
    badge = blocks.CharBlock(max_length=30, label="Étiquette", help_text="Ex : Rémission")
    title = blocks.CharBlock(max_length=60, label="Titre", help_text="Ex : Soleil")
    text = blocks.TextBlock(max_length=200, label="Texte court")
    page = blocks.PageChooserBlock(required=False, label="Page liée")
    link_text = blocks.CharBlock(max_length=40, default="Voir les conseils", label="Texte du lien")

    class Meta:
        icon = "pick"
        label = "Carte phase"


# ---------------------------------------------------------------
# Bloc 3 : la section des phases (titre, intro, 3 cartes)
# ---------------------------------------------------------------
class PhasesBlock(blocks.StructBlock):
    title = blocks.CharBlock(
        max_length=150,
        default="Quelle météo souhaitez-vous consulter aujourd'hui ?",
        label="Titre",

    )
    intro = blocks.TextBlock(
        required=False,
        default="Choisissez les informations qui vous intéressent. "
                "Vous pouvez consulter les trois phases librement, à tout moment.",
        label="Introduction",
    )
    cards = blocks.ListBlock(PhaseCardBlock(), min_num=3, max_num=3, label="Cartes")

    class Meta:
        icon = "pick"
        label = "Phases météo"


# ---------------------------------------------------------------
# Bloc 4 : une carte "lien rapide"
# ---------------------------------------------------------------
class LienRapideBlock(blocks.StructBlock):
    title = blocks.CharBlock(max_length=60, label="Titre", help_text="Ex : Comprendre les MICI")
    text = blocks.TextBlock(required=False, max_length=160, label="Petite phrase (facultatif)")
    page = blocks.PageChooserBlock(required=False, label="Page liée")
    link_text = blocks.CharBlock(max_length=40, default="Lire", label="Texte du lien")

    class Meta:
        icon = "link"
        label = "Lien rapide"


# ---------------------------------------------------------------
# Bloc 5 : la rangée de liens rapides (jusqu'à 3 cartes)
# ---------------------------------------------------------------
class LiensRapidesBlock(blocks.StructBlock):

    title = blocks.CharBlock(max_length=100, default="Pour aller plus loin", label="Titre de la section")
    links = blocks.ListBlock(LienRapideBlock(), min_num=1, max_num=3, label="Liens")

    class Meta:
        icon = "link"
        label = "Liens rapides"


# ---------------------------------------------------------------
# La page d'accueil
# ---------------------------------------------------------------
class HomePage(Page):
    body = StreamField(
        [
            ("presentation", PresentationBlock()),
            ("phases", PhasesBlock()),
            ("liens", LiensRapidesBlock()),
        ],
        blank=True,
        verbose_name="Contenu de la page",
    )

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


# ---------------------------------------------------------------
# Snippet : les numéros d'urgence du header
# (ils se modifient dans l'admin, menu Snippets)
# ---------------------------------------------------------------
@register_snippet

class NumeroUrgence(models.Model):
    numero = models.CharField(max_length=20, verbose_name="Numéro")
    nom = models.CharField(max_length=60, verbose_name="Texte à côté du numéro")
    sms = models.BooleanField(default=False, verbose_name="Contact par SMS (et pas par appel)")
    ordre = models.PositiveSmallIntegerField(default=0, verbose_name="Ordre d'affichage")

    panels = [
        FieldPanel("numero"),
        FieldPanel("nom"),
        FieldPanel("sms"),
        FieldPanel("ordre"),
    ]

    class Meta:
        ordering = ["ordre"]
        verbose_name = "Numéro d'urgence"
        verbose_name_plural = "Numéros d'urgence"

    def __str__(self):
        return f"{self.numero} {self.nom}"