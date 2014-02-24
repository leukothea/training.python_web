from django.contrib import admin
from django.core.urlresolvers import reverse
from myblog.models import Post, Category

class CategoryInline(admin.TabularInline):
	model = Category.posts.through

class CategoryAdmin(admin.ModelAdmin):
	fields = ('name', 'description')
	exclude = ('posts', )

class PostAdmin(admin.ModelAdmin):
	inlines = [
		CategoryInline,
	]
#	exclude = ('post',)

	def get_formsets(self, request, obj=None):
		for inline in self.get_inline_instances(request, obj):
			yield inline.get_formset(request, obj)

	list_display = ('title', )

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
