### Blogging App

A Django-based blogging platform integrated with Firebase Firestore for storage. Users can create, edit, delete, and search blog posts with authentication.

---

#### Features
- User authentication (login/logout).  
- Add, edit, and delete blog posts with optional image upload.  
- Search posts by title, content, or tags.  
- Display recent posts and tag statistics.

---

#### Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/SimpleCyber/Blogging-app.git
   cd Blogging-app
   ```
2. **Install Dependencies**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Configure Firebase**:
   - Set up Firebase Firestore.
   - Add credentials in a `.env` file:
     ```env
     FIREBASE_PROJECT_ID=your_project_id
     FIREBASE_PRIVATE_KEY=your_private_key
     # Add other keys here...
     ```
4. **Run the App**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

Contributions are welcome!