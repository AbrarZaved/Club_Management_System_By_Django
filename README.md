<!DOCTYPE html>
<html lang="en">
<body>

<h1>Club Management System</h1>
<p>A web application designed to manage and streamline club activities, events, and member interactions for any university.</p>

<h2>Project Overview</h2>
<p>The <strong>DIU Club Management System</strong> enables club members, admins, and university stakeholders to coordinate club activities efficiently. It provides features for handling join requests, event notifications, notices, and more.</p>

<h2>Features</h2>
<ul>
  <li>User Registration and Profile Management</li>
  <li>Admin and Member Roles with Access Control</li>
  <li>Join Request Management (Admins receive notifications)</li>
  <li>Event and Notice Notifications for Members</li>
  <li>Automatic Deletion of Read Notifications</li>
</ul>

<h2>Getting Started</h2>
<p>Follow these instructions to set up and run the DIU Club Management System locally.</p>

<h3>Prerequisites</h3>
<ul>
  <li><a href="https://www.python.org/">Python 3.x</a> installed on your machine</li>
  <li><a href="https://www.djangoproject.com/">Django</a> (Version: specify your version)</li>
  <li>Additional dependencies listed in <code>requirements.txt</code></li>
</ul>

<h3>Installation</h3>
<pre>
<code>
# Clone the repository
git clone https://github.com/AbrarZaved/Club_Management_System_By_Django.git

# Navigate into the project directory
cd Club_Management_System_By_Django

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser
python manage.py createsuperuser

# Run the development server
python manage.py runserver
</code>
</pre>

<h2>Usage</h2>
<p>After starting the server, you can access the application by going to <code>http://127.0.0.1:8000/</code> in your web browser.</p>

<h2>Project Structure</h2>
<ul>
  <li><strong>accounts/</strong> - Handles user registration, login, and profile management.</li>
  <li><strong>clubs/</strong> - Contains models, views, and templates related to club and event management.</li>
  <li><strong>notifications/</strong> - Manages notification functionalities for join requests, events, and notices.</li>
  <li><strong>static/</strong> - Contains static files such as CSS, JavaScript, and images.</li>
  <li><strong>templates/</strong> - Holds HTML templates for the application.</li>
</ul>

<h2>Technologies Used</h2>
<ul>
  <li>Django - Backend framework</li>
  <li>MySQL - Database</li>
  <li>JavaScript - Frontend interactions</li>
  <li>HTML & CSS - Markup and styling</li>
</ul>

<h2>Contributing</h2>
<p>Contributions are welcome! If you'd like to contribute, please fork the repository and make a pull request.</p>

<h2>License</h2>
<p>This project is licensed under the MIT License - see the <a href="LICENSE">LICENSE</a> file for details.</p>

<h2>Contact</h2>
<p>For questions or support, please contact <strong>Abrar Javed Sorafi</strong> at <a href="mailto:abrarzaved2002@gmail.com">AbrarZaved</a>.</p>

</body>
</html>
