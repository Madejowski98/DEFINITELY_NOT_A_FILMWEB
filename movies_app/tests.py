from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from .models import Movie, Review, Article, Genre

User = get_user_model()


class MovieAppTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.staff_user = User.objects.create_user(
            username="staffuser", password="password", is_staff=True
        )
        self.genre = Genre.objects.create(name="Action")
        self.movie = Movie.objects.create(
            title="Test Movie",
            genre=self.genre,
            release_year=2020,
            director="John Doe",
            description="Test Description",
            added_by=self.user,
            approved=True,  # Updated to be approved by default for list views
        )
        self.article = Article.objects.create(
            title="Test Article",
            description="Test Description",
            added_by=self.user,
            approved=True,  # Updated to be approved by default for list views
        )

    def test_movie_list(self):
        response = self.client.get(reverse("movie_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.movie.title)

    def test_movie_detail(self):
        response = self.client.get(reverse("movie_detail", args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.movie.title)

    def test_add_movie_authenticated(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("add_movie"),
            {
                "title": "New Movie",
                "genre": self.genre.id,
                "release_year": 2021,
                "director": "Jane Doe",
                "description": "New Description",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Movie.objects.count(), 2)

    def test_add_movie_unauthenticated(self):
        response = self.client.post(
            reverse("add_movie"),
            {
                "title": "New Movie",
                "genre": self.genre.id,
                "release_year": 2021,
                "director": "Jane Doe",
                "description": "New Description",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Movie.objects.count(), 1)

    def test_approve_movie_as_staff(self):
        self.client.login(username="staffuser", password="password")
        response = self.client.post(reverse("approve_movie", args=[self.movie.id]))
        self.assertEqual(response.status_code, 302)
        self.movie.refresh_from_db()
        self.assertTrue(self.movie.approved)

    def test_pending_movies_as_staff(self):
        self.client.login(username="staffuser", password="password")
        response = self.client.get(reverse("pending_movies"))
        self.assertEqual(response.status_code, 200)
        # Create another unapproved movie to test pending movies list
        unapproved_movie = Movie.objects.create(
            title="Pending Movie",
            genre=self.genre,
            release_year=2021,
            director="Jane Doe",
            description="Pending Description",
            added_by=self.user,
            approved=False,
        )
        response = self.client.get(reverse("pending_movies"))
        self.assertContains(response, unapproved_movie.title)

    def test_pending_movies_non_staff(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("pending_movies"))
        self.assertEqual(response.status_code, 302)

    def test_add_review_authenticated(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("add_review", args=[self.movie.id]),
            {"rating": 8, "review": "Great movie!"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 1)

    def test_add_review_unauthenticated(self):
        response = self.client.post(
            reverse("add_review", args=[self.movie.id]),
            {"rating": 8, "review": "Great movie!"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Review.objects.count(), 0)

    def test_article_list(self):
        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)

    def test_article_detail(self):
        response = self.client.get(reverse("article_detail", args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article.title)

    def test_add_article_authenticated(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("add_article"),
            {"title": "New Article", "description": "New Description"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Article.objects.count(), 2)

    def test_add_article_unauthenticated(self):
        response = self.client.post(
            reverse("add_article"),
            {"title": "New Article", "description": "New Description"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Article.objects.count(), 1)

    def test_approve_article_as_staff(self):
        self.client.login(username="staffuser", password="password")
        response = self.client.post(reverse("approve_article", args=[self.article.id]))
        self.assertEqual(response.status_code, 302)
        self.article.refresh_from_db()
        self.assertTrue(self.article.approved)

    def test_pending_articles_as_staff(self):
        self.client.login(username="staffuser", password="password")
        response = self.client.get(reverse("pending_articles"))
        self.assertEqual(response.status_code, 200)
        # Create another unapproved article to test pending articles list
        unapproved_article = Article.objects.create(
            title="Pending Article",
            description="Pending Description",
            added_by=self.user,
            approved=False,
        )
        response = self.client.get(reverse("pending_articles"))
        self.assertContains(response, unapproved_article.title)

    def test_pending_articles_non_staff(self):
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse("pending_articles"))
        self.assertEqual(response.status_code, 302)

    def test_average_rating(self):
        # Create reviews
        Review.objects.create(
            user=self.user, movie=self.movie, rating=5, review="Review 1"
        )
        Review.objects.create(
            user=self.user, movie=self.movie, rating=7, review="Review 2"
        )
        Review.objects.create(
            user=self.user, movie=self.movie, rating=9, review="Review 3"
        )

        # Check average rating
        self.assertAlmostEqual(self.movie.user_rating, 7, places=1)

        # Check if average rating is correctly displayed in the detail view
        response = self.client.get(reverse("movie_detail", args=[self.movie.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Average Rating: 7.0")
