# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import uuid

class Author(models.Model):
    """
    Model representing an author.
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('Died', null=True, blank=True)

    class Meta:
        ordering = ["last_name","first_name"]
    
    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance.
        """
        return reverse('author-detail', args=[str(self.id)])
    

    def __str__(self):
        """
        String for representing the Model object.
        """
        return '{0}, {1}'.format(self.last_name,self.first_name)

class Genre(models.Model):
	"""
	This class represent the genre a book can have.
	"""

	name = models.CharField(max_length=200,
		help_text="Enter a book genre (e.g. Science Fiction, French Poetry etc)")

	def __str__(self):
		"""
		String representation of the Genre object 
		"""
		return self.name

class Book(models.Model):
	"""
	This class is the representation of a Book in the library
	"""
	title = models.CharField(max_length = 200, 
		help_text = "Enter the book title")
	author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
	summary = models.TextField(max_length = 1000,
	 	help_text = "Please enter a brief book description.")
	isbn = models.CharField('isbn',\
		max_length = 200,\
		help_text = """Please enter the 13 char isbn number.
		<a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>""")
	genre = models.CharField('Genre',max_length= 200,help_text = "Select a genre for the book.")

	def __str__(self):		
		"""
		String for representing book model object.
		"""
		return self.title

	def get_absoulte_url(self):
		"""
		returns absolute url to access details of a book
		"""
		return reverse("book-details", args = [str(self.id)])



	def get_absolute_url(self):
		"""
		return absolute url to access genre
		"""
		return reverse(args=[str(self.name)])


class BookInstance(models.Model):
    """
    Model representing a specific copy of a book (i.e. that can be borrowed from the library).
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True) 
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability')

    class Meta:
        ordering = ["due_back"]
        

    def __str__(self):
        """
        String for representing the Model object
        """
        return '{0} ({1})'.format(self.id,self.book.title)
