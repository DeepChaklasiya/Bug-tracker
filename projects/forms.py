from django import forms
from projects.models import Project, Thread, Comment
from django.contrib.auth.models import User


class ProjectForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs.get('user') != None:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    class Meta:
        model = Project
        fields = ['name', 'description', 'tags', 'developers']
        widgets = {
            'description': forms.widgets.Textarea(attrs={'rows': 5}),
            'tags': forms.widgets.Textarea(attrs={'rows': 3}),
        }

    developers = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(
            is_active=True, is_staff=False, is_superuser=False).all(),
        widget=forms.widgets.SelectMultiple
    )

    def save(self, commit=True):
        project = super().save(commit=False)
        tags = [tag.strip() for tag in project.tags.split(',')]
        project.tags = ','.join(tags)
        if not hasattr(project, 'manager'):
            project.manager = self.user
        project.save()

        # To save many to many field, we have to call save_m2m
        self.save_m2m()
        return project

class ThreadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs.get('reporter') != None:
            self.reporter = kwargs.pop('reporter')
        self.project_id= kwargs.pop('projectId')
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = Thread
        fields = ['bug_type','title','description','bug_priority','closed']
        widgets = {
            'description': forms.widgets.Textarea(attrs={'rows': 5})
        }
    BUG_TYPE_CHOICES = (('bug', 'Bug'), ('query', 'Query'))
    closed = forms.BooleanField(initial=False,required=False)
    bug_type=forms.ChoiceField(choices=BUG_TYPE_CHOICES)
    BUG_PRIORITY_CHOICES = (
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
        ('NA', 'Not Applicable'),
        ('enhancement', 'Enhancement'),
    )
    bug_priority=forms.ChoiceField(choices=BUG_PRIORITY_CHOICES)
    def save(self, commit=True):
        thread = super().save(commit=False)
        if not hasattr(thread, 'reporter'):
            thread.reporter = self.reporter
        project = Project.objects.get(id=self.project_id)
        thread.project=project
        thread.save()

        # To save many to many field, we have to call save_m2m
        self.save_m2m()
        return thread

class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        if kwargs.get('author') != None:
            self.author = kwargs.pop('author')
        self.thread_id= kwargs.pop('threadId')
        super().__init__(*args, **kwargs)
    
    class Meta:
        model = Comment
        fields = ['body','author_role']
        widgets = {
            'body': forms.widgets.Textarea(attrs={'rows': 5})
        }
    ROLE_CHOICES = (
        ('contributor', 'Contributor'),
        ('developer', 'Developer'),
        ('project_manager', 'Project Manager'),
    )
    author_role=forms.ChoiceField(choices=ROLE_CHOICES)
    def save(self, commit=True):
        comment = super().save(commit=False)
        if not hasattr(comment, 'author'):
            comment.author = self.author
        thread = Thread.objects.get(id=self.thread_id)
        comment.thread=thread
        comment.save()

        # To save many to many field, we have to call save_m2m
        self.save_m2m()
        return comment