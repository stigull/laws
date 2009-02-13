#coding: utf-8
from markdown2 import markdown

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext
from django.db.models.signals import pre_delete, post_delete

from utils.stringformatting import slugify




class NodeType(models.Model):
    name = models.CharField(_(u"Nafn tags"), max_length = 100, unique = True)
    treelevel = models.PositiveIntegerField(_(u"Dýpt í tré"), unique = True)

    class Meta:
        verbose_name = _(u"Tegund hnúts í lagatréi")
        verbose_name_plural = _(u"Tegundir hnúta í lagatréi")

    def __unicode__(self):
        return self.name

class LawNode(models.Model):
    """
    LawNode represents a node in a law tree. Each tree is of a certain form

        Node[type1]
            Node[type2]
            Node[type2]
                Node[type3]
                Node[type3]
                    ...
                    Node[typei]
                Node[type3]
            Node[type2]
                Node[type3]
            ...
        Node[type1]
            Node[type2]
        Node[type1]

        If a node has a type with treelevel i then there exists a path from a treelevel 1 element to the node consisting
        of exactly i nodes



    """
    node_type = models.ForeignKey(NodeType, verbose_name = _(u"Tag hnútsins"))
    number = models.IntegerField(_(u"Númer"))
    name = models.CharField(_(u"Nafn hnútsins"), max_length = 200, blank = True)
    content = models.TextField(_(u"Innihald hnútsins"), blank = True)
    content_html = models.TextField(blank = True)
    parent = models.ForeignKey("self", verbose_name = _(u"Foreldri hnútsins"), related_name = "children", null = True, blank = True)

    class Meta:
        ordering = ("number", "parent__number")
        verbose_name = _(u"Hnútur í lagatréi")
        verbose_name_plural = _(u"Hnútar í lagatréi")

    def __unicode__(self):
        if self.parent:
            return u"%s > %s %s: %s" % (self.parent, self.node_type, self.number, self.name)
        else:
            return u"%s %s: %s" % (self.node_type, self.number, self.name)

    def has_children(self):
        """
        Usage:  has_children = node.has_children()
        After:  has_children is True if and only if the node has a subtree
        """
        return self.children.all().count() > 0

    def get_positional_id(self):
        """
        Usage:  node_positional_id = node.get_positional_id()
        After:  node_positional_id is a unique string for this node that represents it's position in the law
        """
        if self.parent:
            return u"%s-%s-%s" % (self.parent.get_positional_id(), slugify(self.node_type.name), self.number)
        else:
            return u"%s-%s" % (slugify(self.node_type.name), self.number)

    def save(self):
        self.content_html = markdown(self.content)
        super(LawNode, self).save()

def delete_node_handler(sender, instance, **kwargs):
    """
    Renumbers the entire law tree when a node gets deleted
    """
    parent = instance.parent
    print instance
    print parent
    if parent is None:
        #We are at root level
        tree = instance.law_tree.all()[0]
        nodes = tree.root_nodes.all().order_by('number')
    else:
        nodes = parent.children.all().order_by('number')


    nodes = nodes.exclude(id = instance.id)
    for i, node in enumerate(nodes):
        node.number = i+1
        node.save()

pre_delete.connect(delete_node_handler, sender=LawNode)

class Laws(models.Model):
    schoolyear = models.ForeignKey("student.Schoolyear", verbose_name = _(u"Skólaár"), unique = True, related_name = 'laws')
    root_nodes = models.ManyToManyField(LawNode, verbose_name = _(u"Rætur trésins"),
                                            limit_choices_to = {'node_type__treelevel' : 1 },
                                            related_name = 'law_tree')

    class Meta:
        verbose_name = _(u"Lög félagsins")
        verbose_name_plural = _(u"Lög félagsins")

    def __unicode__(self):
        return gettext(u"Lög félagsins árið") + " %s" % self.schoolyear

    def get_absolute_url(self):
        return ("laws_show_schoolyear", (), {'schoolyear_starts': self.schoolyear.starts.year, 'schoolyear_ends': self.schoolyear.ends.year })
    get_absolute_url = models.permalink(get_absolute_url)

