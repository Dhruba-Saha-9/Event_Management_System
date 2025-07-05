from flask import Flask, render_template, redirect, url_for, flash, request, abort
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from config import Config
from models import db, Admin, Event, Student, Hall
from forms import EventForm, RegistrationForm, LoginForm, HallForm
import qrcode
import io
import base64
import PIL.Image
from datetime import datetime, date
from sqlalchemy.orm import joinedload
from sqlalchemy import desc

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

# Create database tables and admin user
with app.app_context():
    db.create_all()
    if not Admin.query.first():
        admin = Admin(username="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()

@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))

@app.context_processor
def inject_now():
    return {'now': datetime.now}

def generate_qr_code(data):
    """Generate QR code from data dictionary"""
    qr_string = (
        f"Name: {data['name']}\n"
        f"Email: {data['email']}\n"
        f"Event: {data['event']}\n"
        f"Venue: {data['venue']}\n"
        f"Date: {data['date']}"
    )
    
    qr = qrcode.make(qr_string)
    qr = qr.resize((app.config['QR_CODE_SIZE'], app.config['QR_CODE_SIZE']), PIL.Image.LANCZOS)
    buf = io.BytesIO()
    qr.save(buf, format="PNG")
    return base64.b64encode(buf.getvalue()).decode('utf-8')

@app.route('/')
def index():
    """Home page showing all events"""
    page = request.args.get('page', 1, type=int)
    events = Event.query.options(joinedload(Event.hall)).order_by(Event.date).paginate(
        page=page, per_page=app.config['EVENTS_PER_PAGE'], error_out=False
    )
    return render_template('index.html', events=events)

@app.route('/register/<int:event_id>', methods=['GET', 'POST'])
def register(event_id):
    """Register for an event"""
    event = Event.query.get_or_404(event_id)
    form = RegistrationForm()
    qr_code_base64 = None
    qr_data = None

    if event.is_full:
        flash('Sorry, this event is full.', 'warning')
        return redirect(url_for('index'))

    if form.validate_on_submit():
        # Check if email already registered for this event
        existing_registration = Student.query.filter_by(
            email=form.email.data, event_id=event.id
        ).first()
        
        if existing_registration:
            flash('You are already registered for this event.', 'warning')
            return render_template('register.html', form=form, event=event)

        student = Student(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            event_id=event.id
        )
        
        try:
            db.session.add(student)
            event.registered += 1
            db.session.commit()

            qr_data = {
                'name': student.name,
                'email': student.email,
                'event': event.title,
                'venue': event.hall.name if event.hall else 'N/A',
                'date': event.date.strftime('%B %d, %Y')
            }

            qr_code_base64 = generate_qr_code(qr_data)
            flash('Registration successful! Your QR code is ready.', 'success')
            
        except Exception as e:
            db.session.rollback()
            flash('Registration failed. Please try again.', 'danger')
            app.logger.error(f"Registration error: {e}")

    return render_template('register.html', form=form, event=event, 
                         qr_data=qr_data, qr_code=qr_code_base64)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Admin login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username=form.username.data).first()
        if admin and admin.check_password(form.password.data):
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        flash('Invalid username or password', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """Admin logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """Admin dashboard"""
    events = Event.query.options(joinedload(Event.hall)).order_by(desc(Event.created_at)).all()
    total_events = Event.query.count()
    total_registrations = Student.query.count()
    total_halls = Hall.query.count()
    
    stats = {
        'total_events': total_events,
        'total_registrations': total_registrations,
        'total_halls': total_halls,
        'upcoming_events': Event.query.filter(Event.date >= date.today()).count()
    }
    
    return render_template('dashboard.html', events=events, stats=stats)

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    """Create new event"""
    form = EventForm()
    halls = Hall.query.all()
    
    if not halls:
        flash('Please add at least one venue before creating events.', 'warning')
        return redirect(url_for('halls'))
    
    form.hall.choices = [(hall.id, f"{hall.name} ({hall.capacity} seats)") for hall in halls]

    if form.validate_on_submit():
        selected_hall = Hall.query.get(form.hall.data)
        event = Event(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            time=form.time.data,
            hall_id=form.hall.data,
            capacity=selected_hall.capacity
        )
        
        try:
            db.session.add(event)
            db.session.commit()
            flash('Event created successfully!', 'success')
            return redirect(url_for('dashboard'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to create event. Please try again.', 'danger')
            app.logger.error(f"Event creation error: {e}")
            
    return render_template('create_event.html', form=form)

@app.route('/delete_event/<int:event_id>', methods=['POST'])
@login_required
def delete_event(event_id):
    """Delete an event"""
    event = Event.query.get_or_404(event_id)
    
    try:
        db.session.delete(event)
        db.session.commit()
        flash('Event deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete event.', 'danger')
        app.logger.error(f"Event deletion error: {e}")
        
    return redirect(url_for('dashboard'))

@app.route('/halls', methods=['GET', 'POST'])
@login_required
def halls():
    """Manage venues"""
    form = HallForm()
    halls = Hall.query.order_by(Hall.name).all()
    
    if form.validate_on_submit():
        new_hall = Hall(
            name=form.name.data,
            capacity=form.capacity.data,
            latitude=float(form.latitude.data) if form.latitude.data else None,
            longitude=float(form.longitude.data) if form.longitude.data else None
        )
        
        try:
            db.session.add(new_hall)
            db.session.commit()
            flash('Venue added successfully!', 'success')
            return redirect(url_for('halls'))
        except Exception as e:
            db.session.rollback()
            flash('Failed to add venue. Please try again.', 'danger')
            app.logger.error(f"Hall creation error: {e}")
            
    return render_template('halls.html', form=form, halls=halls)

@app.route('/delete_hall/<int:hall_id>', methods=['POST'])
@login_required
def delete_hall(hall_id):
    """Delete a venue"""
    hall = Hall.query.get_or_404(hall_id)
    
    if hall.events:
        flash('Cannot delete venue with existing events.', 'warning')
        return redirect(url_for('halls'))
    
    try:
        db.session.delete(hall)
        db.session.commit()
        flash('Venue deleted successfully.', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Failed to delete venue.', 'danger')
        app.logger.error(f"Hall deletion error: {e}")
        
    return redirect(url_for('halls'))

@app.route('/view_registrations/<int:event_id>')
@login_required
def view_registrations(event_id):
    """View registrations for an event"""
    event = Event.query.get_or_404(event_id)
    students = Student.query.filter_by(event_id=event_id).order_by(Student.registered_at).all()
    return render_template('view_registrations.html', event=event, students=students)

@app.route('/track_event/<int:event_id>')
def track_event(event_id):
    """Track event location"""
    event = Event.query.get_or_404(event_id)
    if not event.hall or not event.hall.latitude or not event.hall.longitude:
        abort(404, description="Location not available for this event")
    
    return render_template('track_event.html', 
                         lat=event.hall.latitude, 
                         lng=event.hall.longitude,
                         event=event)

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)
