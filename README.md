# EventHub - Event Management System

A sophisticated, modern event management system built with Flask that allows users to register for events and administrators to manage events, venues, and registrations.

## Features

### For Users
- **Browse Events**: View all upcoming events with detailed information
- **Event Registration**: Register for events with a simple form
- **QR Code Generation**: Automatic QR code generation for event tickets
- **Location Tracking**: Track event locations on maps
- **Responsive Design**: Works seamlessly on desktop and mobile devices

### For Administrators
- **Dashboard**: Comprehensive overview with statistics
- **Event Management**: Create, edit, and delete events
- **Venue Management**: Add and manage event venues with location data
- **Registration Tracking**: View all registrations for each event
- **Secure Authentication**: Protected admin area with password hashing

## Technology Stack

- **Backend**: Flask 3.0.3
- **Database**: MySQL with SQLAlchemy ORM
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF with WTForms
- **Frontend**: Custom CSS framework with modern design
- **QR Codes**: qrcode library with Pillow
- **Validation**: Email validation and form validation

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd event-management-system
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database**
   - Create a MySQL database named `event_db`
   - Update the database connection in `config.py` if needed

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your browser and go to `http://localhost:5000`
   - Admin login: username: `admin`, password: `admin123`

## Project Structure

```
event-management-system/
├── app.py                 # Main Flask application
├── config.py             # Configuration settings
├── models.py             # Database models
├── forms.py              # Form definitions
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── static/
│   └── style.css        # Custom CSS framework
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Home page
    ├── dashboard.html    # Admin dashboard
    ├── login.html        # Admin login
    ├── create_event.html # Event creation form
    ├── register.html     # Event registration
    ├── halls.html        # Venue management
    ├── view_registrations.html # Registration list
    ├── track_event.html  # Location tracking
    └── errors/
        ├── 404.html      # 404 error page
        └── 500.html      # 500 error page
```

## Key Improvements Made

### Security Enhancements
- **Password Hashing**: Admin passwords are now securely hashed using Werkzeug
- **Input Validation**: Comprehensive form validation with proper error messages
- **SQL Injection Protection**: Using SQLAlchemy ORM for safe database operations

### Code Quality
- **Better Organization**: Separated concerns with proper model relationships
- **Error Handling**: Comprehensive error handling with user-friendly messages
- **Code Documentation**: Added docstrings and comments throughout
- **Removed Unnecessary Code**: Eliminated unused DummyForm and redundant code

### User Experience
- **Modern UI**: Custom CSS framework with professional design
- **Responsive Design**: Mobile-friendly interface
- **Better Navigation**: Improved navigation structure
- **Flash Messages**: User-friendly success/error notifications
- **Pagination**: Efficient event listing with pagination

### Database Improvements
- **Proper Relationships**: Better foreign key relationships
- **Cascade Deletes**: Automatic cleanup when events are deleted
- **Timestamps**: Added creation timestamps for all entities
- **Data Validation**: Model-level validation and constraints

### Features Added
- **Event Descriptions**: Optional event descriptions
- **Event Times**: Optional event time specification
- **Phone Numbers**: Optional phone number for registrations
- **Statistics Dashboard**: Overview of system statistics
- **Event Status**: Visual indicators for full/available events
- **Location Validation**: Proper handling of missing location data

## Configuration

The application can be configured through environment variables:

- `SECRET_KEY`: Flask secret key (auto-generated if not provided)
- `DATABASE_URL`: Database connection string
- `QR_CODE_SIZE`: Size of generated QR codes (default: 200)
- `EVENTS_PER_PAGE`: Number of events per page (default: 10)

## Usage

### For Administrators
1. Login with admin credentials
2. Add venues through the "Venues" section
3. Create events and assign them to venues
4. Monitor registrations through the dashboard
5. View detailed registration lists for each event

### For Users
1. Browse available events on the home page
2. Click "Register Now" on any available event
3. Fill out the registration form
4. Receive a QR code ticket for the event
5. Use the "Track Location" feature to find the venue

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support or questions, please open an issue in the repository. 