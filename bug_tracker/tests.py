from django.test import TestCase
from django.shortcuts import render, redirect
from .models import CustomUser, Project, Ticket, Comment, Notification
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CustomUser, Project
from django.contrib.messages import get_messages
from django.core import mail
from django.utils import timezone
import json



User = get_user_model()

# Creating the test cases for the databases
class ModelTestCase(TestCase):

    def setUp(self):
        # A test instances of CustomUser
        self.user1 = CustomUser.objects.create_user(username='user1', first_name='John', last_name='Doe', phone_number='123456789')
        self.user2 = CustomUser.objects.create_user(username='user2', first_name='Jane', last_name='Smith', phone_number='987654321')

        # A test instance of Project
        self.project = Project.objects.create(project_name='Test Project', project_description='This is a test project', project_creator=self.user1)

        # A test instance of Ticket
        self.ticket = Ticket.objects.create(project=self.project, title='Test Ticket', description='This is a test ticket', author=self.user1,
                                            status='New', priority='Low', ticket_type='Bug', estimated_time=5)

        # A test instance of Comment
        self.comment = Comment.objects.create(ticket=self.ticket, author=self.user1, content='This is a test comment')

        # A test instance of Notification
        self.notification = Notification.objects.create(user=self.user2, project=self.project, message='Test notification')

    def test_customuser_str_method(self):
        self.assertEqual(str(self.user1), 'user1')

    def test_project_str_method(self):
        self.assertEqual(str(self.project), 'Test Project')

    def test_ticket_str_method(self):
        self.assertEqual(str(self.ticket), 'Test Ticket')

    def test_comment_str_method(self):
        self.assertEqual(str(self.comment), 'Comment by user1 on Test Ticket')

    def test_notification_str_method(self):
        self.assertEqual(str(self.notification), 'user2 - Test notification')


# Testing the client side
class ViewsTestCase(TestCase):
    def setUp(self):
        # Create a test user for authentication
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com',password='testpassword')
        self.login_url = reverse('login_view')
        self.layout_url = reverse('layout')
        self.index_url = reverse('index')
        self.project_url = reverse('create_project')
        self.update_project_url = reverse('update_project')
        self.delete_project_url = reverse('delete_project', args=[1])
        self.logout_url = reverse('logout')
        self.user2 = CustomUser.objects.create_user(username='testuser2',email='user2@example.com', password='testpassword', first_name='Jane', last_name='Smith')
        self.user3 = CustomUser.objects.create_user(username='testuser3',email='user3@example.com', password='testpassword', first_name='Alice', last_name='Johnson')
        # Create a test project
        self.project = Project.objects.create(project_name='Test Project', project_description='This is a test project.', project_creator=self.user)
        # Add users to the project as team members
        self.project.team_members.add(self.user2, self.user3)
        # Create test tickets
        self.ticket = Ticket.objects.create(project=self.project, title='Test Ticket 1', description='This is a test ticket.', author=self.user, status='New', priority='High', ticket_type='Bug', estimated_time=3)
        self.ticket.assigned_devs.add(self.user2)
        self.ticket2 = Ticket.objects.create(project=self.project, title='Test Ticket 2', description='This is another test ticket.', author=self.user, status='New', priority='Medium', ticket_type='Feature', estimated_time=5)
        self.ticket2.assigned_devs.add(self.user3)
        # Create test comments
        self.comment = Comment.objects.create(ticket=self.ticket, author=self.user, content='This is a test comment.')
        self.comment2 = Comment.objects.create(ticket=self.ticket2, author=self.user2, content='This is another test comment.')
        # Create test notifications
        self.notification = Notification.objects.create(user=self.user, project=self.project, message='This is a test notification.', created_at=timezone.now())

    def test_create_project_view_post(self):
        # Test the create_project view with a POST request and valid project data
        data = {
            'project_name': 'Test Project',
            'project_description': 'This is a test project.',
            'sellist2a': [self.user2.id, self.user3.id],  # Assuming self.user2 and self.user3 are existing users
        }
        response = self.client.post('/create_project', data)
        # Assertions to check the response status code and redirection
        self.assertEqual(response.status_code, 302)  # Should redirect to the index page
        self.assertRedirects(response, reverse('index'))  # You can include this assertion if needed
        # Additional assertions as needed for the successful project creation


    def test_layout_view(self):
        # Test the layout view, should return a 200 status code
        response = self.client.get(reverse('layout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bug_tracker/layout.html')

    def test_index_view(self):
        # Test the index view, should return a 200 status code
        # Note: This view requires authentication, so we need to log in the user
        self.client.force_login(self.user)
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bug_tracker/index.html')

    def test_register_view_get(self):
        # Test the register view with a GET request, should return a 200 status code
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bug_tracker/register.html')

    def test_register_view_post_success(self):
        # Test the register view with a POST request and valid data
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'testpassword',
            'password_confirm': 'testpassword',
        }
        response = self.client.post(reverse('register'), data)
        self.assertRedirects(response, reverse('index'))  # Should redirect to the index page

        # Check if the user was created in the database
        user = CustomUser.objects.get(username='John')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.phone_number, '1234567890')
        self.assertEqual(user.email, 'john.doe@example.com')

    def test_register_view_post_password_mismatch(self):
        # Test the register view with a POST request and password mismatch
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone_number': '1234567890',
            'email': 'john.doe@example.com',
            'password': 'testpassword',
            'password_confirm': 'mismatchedpassword',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bug_tracker/register.html')
        self.assertContains(response, "Passwords must match.")

    def test_register_view_post_empty_fields(self):
        # Test the register view with a POST request and empty fields
        data = {
            'first_name': '',
            'last_name': '',
            'phone_number': '',
            'email': '',
            'password': '',
            'password_confirm': '',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bug_tracker/register.html')
        self.assertContains(response, "All fields are required")
    def test_login_view_get(self):
        # Test the login view with a GET request, should return a 200 status code
        response = self.client.get(reverse('layout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bug_tracker/layout.html')

    def test_login_view_post_invalid_credentials(self):
        # Prepare POST data for invalid credentials
        data = {
            'email': 'invalid@example.com',
            'password': 'invalidpassword',
        }

        # Perform login POST request with invalid credentials
        response = self.client.post(reverse('login_view'), data)

        # Assert that the response status code is 200 (OK) and the message is displayed in the template
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid email and/or password.")

    def test_forgot_password_view_post_user_not_found(self):
        # Prepare POST data for forgot password
        data = {
            'email': 'nonexistentuser@example.com',
        }

        # Perform forgot password POST request
        response = self.client.post(reverse('forgot_password'), data)

        # Assert that the response contains the warning message
        self.assertContains(response, 'User with this email does not exist.')

    def test_forgot_password_view_post_email_sent(self):
        # Test the forgot password view with a POST request and valid email
        data = {
            'email': 'testuser@example.com',
        }
        response = self.client.post(reverse('forgot_password'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'bug_tracker/forgot_password.html')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'An email with instructions to reset your password has been sent to your email address.')
        self.assertEqual(len(mail.outbox), 1)  # Email should be sent
        

    def test_reset_password_view_get_invalid_token(self):
        # Test the reset password view with a GET request and invalid token
        response = self.client.get(reverse('reset_password', kwargs={'uidb64': 'invaliduid', 'token': 'invalidtoken'}))
        self.assertRedirects(response, reverse('layout'))  # Should redirect to the layout page


    def test_update_password_view_post_password_match(self):
        # Test the update password view with a POST request and matching passwords
        new_password = 'newtestpassword'
        data = {
            'new_password': new_password,
            'new_password_confirm': new_password,
        }
        response = self.client.post(reverse('update_password', kwargs={'id': self.user.id}), data)
        self.assertRedirects(response, reverse('layout'))  # Should redirect to the layout page
        # Check if the password was updated in the database
        updated_user = CustomUser.objects.get(id=self.user.id)
        self.assertTrue(updated_user.check_password(new_password))

    def test_login_view_post_success(self):
        # Test the login view with a POST request and valid login credentials
        data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(self.login_url, data)
        self.assertRedirects(response, self.index_url)

    def test_login_view_post_invalid_credentials(self):
        # Test the login view with a POST request and invalid login credentials
        data = {
            'email': 'invaliduser@example.com',
            'password': 'invalidpassword',
        }
        response = self.client.post(self.login_url, data)
        self.assertContains(response, "Invalid email and/or password.")

    def test_create_project_view_post(self):
        # Test the create project view with a POST request
        self.client.login(email='testuser@example.com', password='testpassword')
        data = {
            'project_name': 'Test Project',
            'project_description': 'Test project description',
            'sellist2a': [self.user.id],
        }
        response = self.client.post(self.project_url, data)
        self.assertRedirects(response, self.index_url)

    def test_delete_comment(self):
        # Test deleting a comment for a ticket
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_comment', args=[self.comment.id]))
        self.assertEqual(response.status_code, 204)

    def test_tickets(self):
        # Test displaying all tickets created by the logged-in user
        self.client.force_login(self.user)
        response = self.client.get(reverse('tickets'))
        self.assertEqual(response.status_code, 200)

    def test_chart_data(self):
        # Test retrieving data for generating the first chart
        self.client.force_login(self.user)
        response = self.client.get(reverse('chart_data'))
        self.assertEqual(response.status_code, 200)

    def test_chart_data2(self):
        # Test retrieving data for generating the second chart
        self.client.force_login(self.user)
        response = self.client.get(reverse('chart_data2'))
        self.assertEqual(response.status_code, 200)

    def test_chart_data3(self):
        # Test retrieving data for generating the third chart
        self.client.force_login(self.user)
        response = self.client.get(reverse('chart_data3'))
        self.assertEqual(response.status_code, 200)

    def test_notifications(self):
        # Test displaying all notifications for the logged-in user
        self.client.force_login(self.user)
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)

    def test_delete_all_notifications(self):
        # Test deleting all notifications for the logged-in user
        self.client.force_login(self.user)
        response = self.client.post(reverse('delete_all_notifications'))
        self.assertEqual(response.status_code, 204)
        