# EventHub - Deployment Guide

This guide will help you deploy your Event Management System to various platforms.

## 🚀 Quick Deploy Options

### Option 1: Render (Recommended - Free)

1. **Fork/Clone this repository** to your GitHub account
2. **Go to [Render.com](https://render.com)** and sign up
3. **Click "New +"** and select "Web Service"
4. **Connect your GitHub repository**
5. **Configure the service:**
   - **Name:** `eventhub-ems` (or any name you prefer)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
6. **Add Environment Variables:**
   - `SECRET_KEY`: Generate a random string
   - `DATABASE_URL`: `sqlite:///event_db.sqlite` (for SQLite)
7. **Click "Create Web Service"**
8. **Wait for deployment** (usually 2-3 minutes)
9. **Your app will be live** at `https://your-app-name.onrender.com`

### Option 2: Heroku (Free tier discontinued)

1. **Install Heroku CLI**
2. **Login to Heroku:** `heroku login`
3. **Create app:** `heroku create your-app-name`
4. **Deploy:** `git push heroku master`
5. **Open app:** `heroku open`

### Option 3: Railway

1. **Go to [Railway.app](https://railway.app)**
2. **Connect your GitHub repository**
3. **Railway will auto-detect Python and deploy**
4. **Add environment variables if needed**
5. **Your app will be live automatically**

### Option 4: PythonAnywhere

1. **Sign up at [PythonAnywhere.com](https://www.pythonanywhere.com)**
2. **Upload your code** or clone from GitHub
3. **Set up a web app** in the Web tab
4. **Configure WSGI file** to point to your Flask app
5. **Install requirements:** `pip install -r requirements.txt`

## 🔧 Environment Variables

Set these environment variables in your deployment platform:

```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///event_db.sqlite
FLASK_ENV=production
```

## 📊 Database Setup

### For Production (Recommended):
- **PostgreSQL** (Render, Heroku, Railway)
- **MySQL** (PythonAnywhere)
- **SQLite** (for simple deployments)

### Database URL Examples:
```bash
# PostgreSQL
DATABASE_URL=postgresql://username:password@host:port/database

# MySQL
DATABASE_URL=mysql+pymysql://username:password@host:port/database

# SQLite
DATABASE_URL=sqlite:///event_db.sqlite
```

## 🛠️ Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/your-username/Event_Management_System.git
   cd Event_Management_System
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up database:**
   ```bash
   python reset_db.py
   ```

5. **Run the application:**
   ```bash
   python app.py
   ```

6. **Access at:** `http://localhost:5000`

## 🔐 Admin Access

After deployment, you can access the admin panel:
- **URL:** `https://your-app-url.com/login`
- **Username:** `admin`
- **Password:** `admin123`

**Important:** Change the default password after first login!

## 📱 Features Available After Deployment

✅ **Event Management** - Create, edit, delete events  
✅ **Venue Management** - Add and manage event venues  
✅ **User Registration** - Public event registration  
✅ **QR Code Generation** - Automatic ticket generation  
✅ **Location Tracking** - Map-based venue location  
✅ **Admin Dashboard** - Statistics and management  
✅ **Responsive Design** - Works on all devices  

## 🚨 Troubleshooting

### Common Issues:

1. **Build fails:**
   - Check Python version compatibility
   - Ensure all dependencies are in `requirements.txt`

2. **Database errors:**
   - Verify `DATABASE_URL` is correct
   - Check database permissions

3. **Static files not loading:**
   - Ensure `static/` folder is included
   - Check file permissions

4. **Location tracking not working:**
   - HTTPS is required for geolocation
   - Check browser permissions

### Support:
- Check the application logs in your deployment platform
- Review the README.md for detailed setup instructions
- Open an issue on GitHub for bugs or questions

## 🎉 Success!

Once deployed, your Event Management System will be accessible worldwide with:
- **Professional UI/UX**
- **Secure authentication**
- **Mobile-responsive design**
- **Real-time location tracking**
- **QR code ticket generation**
- **Comprehensive admin features**

Happy deploying! 🚀 