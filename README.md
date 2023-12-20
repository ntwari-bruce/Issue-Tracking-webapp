# Issue-Tracking-webapp
The Bug Tracker Web App is a Django-based application designed to help teams manage and track bugs, issues, and tasks related to their projects. It provides an efficient platform for project collaboration, where team members can create, update, and manage tickets with ease.

## Distinctiveness and Complexity
## Why our project satisfies the distinctiveness requirements:
1. Our Bug Tracker Web App stands out as a unique and valuable tool for project management and issue tracking. While there are existing bug tracking systems available, we have tailored our application to meet specific needs and provide a user-friendly experience. The distinctiveness of our project lies in the following aspects:

2. Custom User Model: We have customized the user model to include additional fields like phone_number, allowing us to capture more user-specific details. This customization enhances the user experience and provides project managers with valuable information about team members.

3. Real-time Notifications: Our application sends real-time notifications to users when they are assigned to a ticket, receive comments, or when a ticket's status changes. This feature fosters effective communication and collaboration within the team, leading to quicker issue resolution.

4. Data Visualization: The application incorporates data visualizations for ticket count by type, priority, and status. This visual representation of ticket data offers project managers and stakeholders valuable insights into the distribution of issues, enabling them to make data-driven decisions.

5. Custom Ticket Types and Priorities: We allow users to define custom ticket types and priorities, giving them the flexibility to adapt the system to their specific project requirements. This level of customization sets our Bug Tracker Web App apart from generic bug tracking solutions.

6. Collaborative Commenting System: Our commenting system enables team members to leave real-time comments on tickets, facilitating smooth communication and progress updates. Users can engage in discussions, share solutions, and collectively resolve issues within the system.

## Why our project satisfies the complexity requirements:
1. Our Bug Tracker Web App exhibits complexity in various aspects of its development and implementation. The complexity can be observed in the following areas:

2. Custom User Model Implementation: Customizing the user model required in-depth knowledge of Django's authentication system. Implementing the CustomUser model involved extending the AbstractUser class and handling various user-specific fields.

3. Advanced Querying and Data Filtering: Our application utilizes complex queries and filtering mechanisms to retrieve project-related data, manage ticket assignments, and display relevant information to users based on their permissions and project roles.

4. User Authentication and Authorization: The project implements a robust authentication and authorization system, ensuring that only authorized users can access specific project details and perform relevant actions, such as editing tickets or deleting projects.

5. Real-time Notifications and Email Integration: Implementing real-time notifications and integrating the email functionality required working with asynchronous tasks and handling user preferences for notification settings.

6. Data Visualization with Chart.js: The incorporation of data visualizations using Chart.js involved complex data processing, filtering, and rendering. We had to transform ticket data into the appropriate format for rendering interactive charts.

7. Custom Ticket Status and Priority Handling: The system allows users to define custom ticket statuses and priorities, requiring intricate database and form handling to accommodate dynamic options and user-defined choices.

8. Responsive Front-end Design: The project incorporates a responsive and user-friendly front-end design, optimizing the user experience on different devices and screen sizes.

9. Collaborative Commenting System: Implementing a commenting system that enables real-time discussions and updates required handling AJAX requests, managing comment creation, and displaying comments on ticket details pages.


# Features
_ User Authentication: Secure user registration and login functionalities are implemented using Django's built-in authentication system. Users can sign up, log in, and access the bug tracking functionalities specific to their roles.

_ Project Management: Users can create projects and add team members to collaborate on the project. Each project can have multiple tickets related to bugs, issues, or tasks.
Ticket Management: Users can create, edit, and delete tickets. Tickets can be assigned to team members, and their status, priority, and type can be updated.

_ Comment System: A comment system is provided for each ticket, enabling team members to discuss and provide updates on the ticket's progress.

_ Notifications: Users receive notifications about ticket updates and assignments, keeping them informed of project activities.

_ Dashboard and Analytics: The application offers visual representations of ticket data, such as ticket count by type, priority, and status, providing valuable insights into project progress.

## Custom User Model
The user model in this project has been customized to extend the default Django user model. The `CustomUser`model includes additional fields such as `phone_number` to capture user-specific information. The custom user model is implemented using the `AbstractUser` class provided by Django.
# models.py
`from django.contrib.auth.models import AbstractUser` 
 `class CustomUser(AbstractUser):` 
    ` phone_number = models.CharField(max_length=15)`

   `# Additional fields and methods can be added as needed.` 

## Requirements
Ensure you have Python 3.x installed, along with the required Python packages mentioned in the requirements.txt file. If you have not installed the required packages, run the following command in your virtual environment:
`pip install -r requirements.txt`

## Getting Started
1. Clone the project repository to your local machine.
   `git clone https://github.com/yourusername/bug_tracker.git`
   `cd bug_tracker`

2. Set up a virtual environment (recommended) and activate it. If you don't have virtualenv installed, install it using:
     `pip install virtualenv`
   Create and activate a virtual environment:
    `virtualenv env`
    `source env/bin/activate`   
  # On Windows, use `env\Scripts\activate``

3. Install the required Python packages using the __requirements.txt__ file:
   `pip install -r requirements.txt`

4. Migrate the database:
   `python manage.py migrate`
5. Create a superuser to access the admin panel and create projects:
   `python manage.py createsuperuser`
6. Run the development server:
   `python manage.py runserver`
7. Open your web browser and navigate to `http://127.0.0.1:8000/` to access the Bug Tracker Web App.

## Usage

_ `User Registration and Login:` Users can sign up for an account or log in if they already have one. Only logged-in users can create projects and tickets, as well as access the dashboard and notifications .

_ `Creating a Project:` Logged-in users with appropriate permissions can create new projects and add team members to collaborate on the project.

_ `Managing Tickets:` Project team members can create, edit, and delete tickets related to bugs, issues, or tasks. Tickets can be assigned to team members, and their status, priority, and type can be updated.

_ `Ticket Comments:` Team members can discuss and provide updates on tickets by leaving comments.

_ `Dashboard and Analytics:` The dashboard provides visual representations of ticket data, such as ticket count by type, priority, and status. Use these insights to track project progress and identify areas that require attention.

_ `Notifications:` Users receive notifications about ticket updates and assignments, keeping them informed about project activities.


Thank you for using the Bug Tracker Web App! We hope it helps streamline your project management and bug tracking process. Happy collaborating!



   


