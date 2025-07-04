# 🔍 App Search & Review System

A full-stack Django web application that allows users to search for mobile apps, view app details, read community and Play Store reviews, and submit their own reviews.

Built with a clean UI, intelligent text matching, and user-authenticated review approval system.

---

## 🚀 Features

- 🔎 **Smart App Search**
  - Autocomplete suggestions after typing 3 characters
  - TF-IDF-based text similarity for relevant results

- 📱 **App Detail View**
  - Displays metadata, install count, and ratings
  - Separates main app and similar apps by category

- ⭐ **User Reviews**
  - Authenticated users can submit reviews with 1–5 star rating
  - Community reviews shown alongside Play Store reviews
  - Sentiment color-coded (optional auto-sentiment planned for future implementations)

- 👮 **Review Moderation**
  - User-submitted reviews require supervisor/admin approval

- 🎨 **Modern UI**
  - Responsive Bootstrap layout
  - Font Awesome icons
  - Light/dark theming options

---

## 🌐 Live Demo

**🔗 [Click here to try the app live](https://app-search-eh8o.onrender.com/)**  
(*Hosted on Render's free tier*)

---

## 🧪 Tech Stack

- **Backend:** Django 4.x, PostgreSQL
- **Frontend:** HTML, Bootstrap, Font Awesome
- **NLP Engine:** TF-IDF with `sklearn`
- **ORM:** Django Models
- **Hosting:** Render (512MB free tier), GitHub

---

## ⚙️ Local Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/shub1709/franklin_templeton.git
cd franklin_templeton
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows or create a conda env
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the root folder:

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
```

Or if using Postgres (e.g., Supabase):

```env
DATABASE_URL=postgres://username:password@host:port/dbname
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Run the Server

```bash
python manage.py runserver
```

Visit: [http://localhost:8000](http://localhost:8000)

---

## 🧑‍💻 Users & Roles

| Role       | Permissions                         |
|------------|-------------------------------------|
| Guest      | Search apps, read reviews           |
| User       | Submit reviews with rating          |
| Admin      | Approve/reject user-submitted reviews |

---

## 📂 Project Structure (Simplified)

```
├── apps/                  # Django app logic
│   ├── models.py          # App + Review models
│   ├── views.py           # Search, detail, review views
│   ├── templates/         # HTML templates
│   ├── static/            # CSS, JS
├── project/               # Django settings and URLs
├── manage.py
├── requirements.txt
├── README.md
└── .env                   # Local environment (not committed)
```

---

## 🧠 Future Value add-on features

- Integrate BERT-based sentiment analysis for detecting sentiments in user reviews
- Integrate the funtionality of app search based on user's requirement in addition to existing 'Keyword' search functionality
- Integration of a ChatBot (Frank) for additional assistance to the user
- Email verification for new users
- Pagination in review listings
- Sort/filter reviews by rating or sentiment

---

## 🙋‍♂️ Author

**Shubham Agarwal**  

---

## 🛡️ License


---