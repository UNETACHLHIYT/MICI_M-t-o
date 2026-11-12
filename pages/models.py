from django.db import models
from modelcluster.fields import ParentalKey

from wagtail import blocks
from wagtail.admin.panels import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
)
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.images.blocks import ImageChooserBlock
from wagtail.models import Page

from home.models import PhaseCardBlock


# ---------------------------------------------------------------
# Page 1 : Comprendre les MICI
# ---------------------------------------------------------------

# Une carte maladie (Crohn, RCH)
class MaladieBlock(blocks.StructBlock):
    titre = blocks.CharBlock(max_length=100, label="Nom de la maladie")
    texte = blocks.TextBlock(max_length=200, label="Petite phrase")

    class Meta:
        icon = "doc-full"
        label = "Maladie"


# Une colonne de texte (Symptômes digestifs, Au-delà de l'intestin)
class ColonneBlock(blocks.StructBlock):
    titre = blocks.CharBlock(max_length=100, label="Titre de la colonne")
    texte = blocks.RichTextBlock(
        features=["bold", "italic", "link", "ol", "ul"],
        label="Texte",
    )

    class Meta:
        icon = "list-ul"
        label = "Colonne"


class ComprendrePage(Page):
    template = "pages/mici.html"

    introduction = models.TextField(blank=True, verbose_name="Phrase d'introduction")

    maladies = StreamField(
        [("maladie", MaladieBlock())],
        blank=True,
        max_num=2,
        verbose_name="Les maladies (2 cartes)",
    )

    colonnes = StreamField(
        [("colonne", ColonneBlock())],
        blank=True,
        max_num=2,
        verbose_name="Les 2 colonnes",
    )

    remission = RichTextField(
        blank=True,
        features=["bold", "italic", "link", "ol", "ul"],
        verbose_name="Texte rémission et poussée",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("maladies"),
        FieldPanel("colonnes"),
        FieldPanel("remission"),
    ]


# ---------------------------------------------------------------
# Page 2 : Les phases météo (les 3 cartes)
# ---------------------------------------------------------------
class PhasesPage(Page):
    template = "pages/phase.html"

    etiquette = models.CharField(
        max_length=40,
        blank=True,
        default="Repères · 3 phases",
        verbose_name="Petite étiquette au-dessus du titre",
    )

    icone = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Icône ronde à côté du titre",
    )

    introduction = models.TextField(blank=True, verbose_name="Phrase d'introduction")

    titre_cartes = models.CharField(
        max_length=100,
        default="Choisir sa phase",
        verbose_name="Titre au-dessus des cartes",
    )

    cartes = StreamField(
        [("carte", PhaseCardBlock())],
        blank=True,
        max_num=3,
        verbose_name="Les 3 cartes phases",
    )

    page_precedente = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Bouton de gauche (page précédente)",
    )

    page_suivante = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Bouton de droite (page suivante)",
    )

    content_panels = Page.content_panels + [
        FieldPanel("etiquette"),
        FieldPanel("icone"),
        FieldPanel("introduction"),
        FieldPanel("titre_cartes"),
        FieldPanel("cartes"),
        FieldPanel("page_precedente"),
        FieldPanel("page_suivante"),
    ]

    class Meta:
        verbose_name = "Page des phases météo"


# ---------------------------------------------------------------
# Page 3 : la page d'UNE phase (Soleil, Nuages ou Tempête)
# ---------------------------------------------------------------

# Un conseil (Repos, Hydratation, Alimentation...)
class ConseilBlock(blocks.StructBlock):
    titre = blocks.CharBlock(max_length=80, label="Titre du conseil", help_text="Ex : Hydratation")
    texte = blocks.TextBlock(max_length=300, label="Texte du conseil")

    class Meta:
        icon = "tick"
        label = "Conseil"


class PhaseDetailPage(Page):
    template = "pages/phase_detail.html"

    phase = models.CharField(
        max_length=10,
        choices=[
            ("soleil", "Soleil – Rémission"),
            ("nuages", "Nuages – Vigilance"),
            ("tempete", "Tempête – Alerte"),
        ],
        default="soleil",
        verbose_name="Quelle phase ?",
        help_text="Choisit les couleurs de la page.",
    )

    etiquette = models.CharField(
        max_length=60,
        blank=True,
        verbose_name="Petite étiquette au-dessus du titre",
        help_text="Ex : Rémission · Tout va bien",
    )

    icone = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Icône ronde à côté du titre",
    )

    introduction = models.TextField(blank=True, verbose_name="Phrase d'introduction")

    # L'encadré d'alerte : on le laisse VIDE pour Soleil et Nuages
    alerte_titre = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Titre de l'alerte",
        help_text="Ex : Signes d'alerte : appelez votre équipe soignante ou le 15",
    )
    alerte_sous_titre = models.CharField(max_length=120, blank=True, verbose_name="Sous-titre de l'alerte")
    alerte_texte = models.TextField(blank=True, verbose_name="Texte de l'alerte")

    conseils_titre = models.CharField(
        max_length=100,
        default="Conseils au quotidien",
        verbose_name="Titre au-dessus des conseils",
    )

    conseils = StreamField(
        [("conseil", ConseilBlock())],
        blank=True,
        max_num=6,
        verbose_name="Les conseils",
    )

    page_precedente = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Bouton de gauche (page précédente)",
    )

    page_suivante = models.ForeignKey(
        "wagtailcore.Page",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
        verbose_name="Bouton de droite (page suivante)",
    )

    content_panels = Page.content_panels + [
        FieldPanel("phase"),
        FieldPanel("etiquette"),
        FieldPanel("icone"),
        FieldPanel("introduction"),
        MultiFieldPanel(
            [
                FieldPanel("alerte_titre"),
                FieldPanel("alerte_sous_titre"),
                FieldPanel("alerte_texte"),
            ],
            heading="Encadré d'alerte (seulement pour Tempête, laisser vide sinon)",
        ),
        FieldPanel("conseils_titre"),
        FieldPanel("conseils"),
        FieldPanel("page_precedente"),
        FieldPanel("page_suivante"),
    ]

    class Meta:
        verbose_name = "Page d'une phase (Soleil, Nuages, Tempête)"


# ---------------------------------------------------------------
# Page 4 : Ressources utiles
# ---------------------------------------------------------------

# Une ressource (AFA, Ameli...)
class RessourceBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False, label="Logo ou image")
    nom = blocks.CharBlock(max_length=100, label="Nom", help_text="Ex : AFA Crohn RCH France")
    description = blocks.TextBlock(
        required=False,
        max_length=250,
        label="Petite description (facultatif)",
    )
    url = blocks.URLBlock(label="Adresse du site", help_text="Ex : https://www.afa.asso.fr")
    texte_lien = blocks.CharBlock(max_length=40, default="Visiter le site", label="Texte du bouton")

    class Meta:
        icon = "site"
        label = "Ressource"


class RessourcesPage(Page):
    template = "pages/ressource.html"

    introduction = models.TextField(blank=True, verbose_name="Phrase d'introduction")

    ressources = StreamField(
        [("ressource", RessourceBlock())],
        blank=True,
        verbose_name="Les ressources",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("ressources"),
    ]

    class Meta:
        verbose_name = "Page des ressources utiles"


# ---------------------------------------------------------------
# Page 5 : Contact et recommandations (formulaire)
# ---------------------------------------------------------------

# Un champ du formulaire (Nom, E-mail, Message...), créé dans l'admin
class ContactFormField(AbstractFormField):
    page = ParentalKey("ContactPage", on_delete=models.CASCADE, related_name="form_fields")


class ContactPage(AbstractEmailForm):
    # Le même fichier sert pour le formulaire ET pour le message « Merci »
    template = "pages/contact.html"
    landing_page_template = "pages/contact.html"

    introduction = models.TextField(blank=True, verbose_name="Phrase d'introduction")

    avertissement_titre = models.CharField(
        max_length=150,
        default="Merci de ne transmettre aucune information médicale.",
        verbose_name="Titre de l'avertissement",
    )
    avertissement_texte = models.TextField(blank=True, verbose_name="Texte de l'avertissement")

    bouton_envoyer = models.CharField(max_length=40, default="Envoyer", verbose_name="Texte du bouton")

    merci_titre = models.CharField(
        max_length=100,
        default="Merci pour votre message",
        verbose_name="Titre après l'envoi",
    )
    merci_texte = models.TextField(blank=True, verbose_name="Texte après l'envoi")

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel("introduction"),
        MultiFieldPanel(
            [FieldPanel("avertissement_titre"), FieldPanel("avertissement_texte")],
            heading="Encadré d'avertissement",
        ),
        InlinePanel("form_fields", label="Champs du formulaire"),
        FieldPanel("bouton_envoyer"),
        MultiFieldPanel(
            [FieldPanel("merci_titre"), FieldPanel("merci_texte")],
            heading="Message affiché après l'envoi",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel([FieldPanel("from_address"), FieldPanel("to_address")]),
                FieldPanel("subject"),
            ],
            heading="Envoi par e-mail (facultatif, à laisser vide pour l'instant)",
        ),
    ]

    class Meta:
        verbose_name = "Page de contact"
    # ---------------------------------------------------------------
# Page 6 : Mentions légales et confidentialité
# ---------------------------------------------------------------

# Une rubrique (Éditeur, Hébergement, Données collectées...)
class SectionBlock(blocks.StructBlock):
    titre = blocks.CharBlock(max_length=100, label="Titre de la rubrique")
    texte = blocks.RichTextBlock(
        features=["bold", "italic", "link", "ol", "ul"],
        label="Texte",
    )

    class Meta:
        icon = "doc-full"
        label = "Rubrique"


class MentionsLegalesPage(Page):
    template = "pages/mentions.html"

    introduction = models.TextField(blank=True, verbose_name="Phrase d'introduction")

    sections = StreamField(
        [("section", SectionBlock())],
        blank=True,
        verbose_name="Les rubriques",
    )

    content_panels = Page.content_panels + [
        FieldPanel("introduction"),
        FieldPanel("sections"),
    ]

    class Meta:
        verbose_name = "Page des mentions légales"
