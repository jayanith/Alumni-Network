# Alumni Networking and Relationship Management System

A comprehensive Django-based web application for alumni networking, relationship management, event organization, and professional connections.

## Features

### Admin Features
- Dashboard with network statistics
- Complete CRUD operations for Alumni profiles
- Event management (create, edit, delete events)
- Job posting management
- View all connections and event registrations
- Monitor network activity

### Alumni Features
- **Alumni Directory**: Browse and search fellow alumni
- **Professional Networking**: Send and accept connection requests
- **Events & Reunions**: Discover and register for networking events, workshops, and reunions
- **Job Board**: Browse job opportunities posted by alumni and companies
- **Messaging**: Direct messaging with connected alumni
- **Profile Management**: Maintain professional profile with current position, company, LinkedIn, and bio
- **Connection Management**: View and manage your professional network

## Technology Stack

- **Backend:** Django 5.2.7
- **Database:** SQLite3 (can be configured for PostgreSQL)
- **Frontend:** HTML, CSS, JavaScript
- **Framework:** Django Templates

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Navigate to the project directory:**
   ```bash
   cd ocmsproject
   ```

2. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install django
   pip install Pillow  # For image handling
   ```

5. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser (for Django admin):**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

8. **Access the application:**
   - Main URL: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/

## Database Setup

The project uses SQLite3 by default. To use PostgreSQL:

1. Update the `DATABASES` configuration in `settings.py`
2. Uncomment the PostgreSQL configuration
3. Update database credentials

## Default Login Credentials

### Admin
- You need to create admin credentials using the Django shell or admin panel
- To create via shell:
  ```bash
  python manage.py shell
  ```
  Then run:
  ```python
  from adminapp.models import Admin
  Admin.objects.create(username='admin', password='admin123')
  ```

### Alumni
- Add alumni through the admin panel
- Default password: "Alumni123" (can be changed)
- Login with Alumni ID and password

## Usage Guide

### As Admin:
1. Login with admin credentials
2. Add alumni profiles with their information
3. Create and manage networking events
4. Post job opportunities
5. View network statistics and connections
6. Monitor event registrations

### As Alumni:
1. Login with Alumni ID and password
2. Browse the alumni directory to find connections
3. Send connection requests to fellow alumni
4. Accept or reject incoming connection requests
5. Browse and register for events
6. Explore job opportunities on the job board
7. Message connected alumni
8. Update your professional profile

## Project Structure

```
ocmsproject/
├── adminapp/          # Admin functionality
├── studentapp/        # Alumni functionality (networking features)
├── templates/         # HTML templates
│   ├── admin/        # Admin templates
│   ├── alumni/       # Alumni templates
│   └── ...
├── static/            # CSS, JS, Images
├── media/             # User uploaded files (profile pictures)
├── manage.py          # Django management script
└── ocmsproject/       # Main project settings
```

## Key Models

- **Alumni**: Alumni profile with professional information
- **Connection**: Connection requests and relationships between alumni
- **Event**: Networking events, workshops, and reunions
- **EventRegistration**: Alumni registrations for events
- **JobPosting**: Job opportunities posted by alumni
- **Message**: Direct messaging between alumni

## Security Notes

- This is a development version
- Passwords are stored in plain text (not for production)
- Use environment variables for sensitive data
- Enable DEBUG=False in production
- Use HTTPS in production
- Implement proper password hashing before production deployment

## Future Enhancements

- Password hashing and encryption
- Email notifications for connection requests and events
- Advanced search and filtering in alumni directory
- Groups and communities
- News feed and activity updates
- File sharing capabilities
- Advanced analytics and reporting
- REST API integration
- Mobile app support
- Social media integration
- Recommendation engine for connections

## Support

For issues or questions, please contact the development team.

## License

This project is for educational purposes.

## Credits

Developed as a Django-based academic project for Alumni Networking and Relationship Management.
