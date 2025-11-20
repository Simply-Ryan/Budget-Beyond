# Budget Beyond

### Currently being worked on:
Ryan - Sign Up / Log In Pages


# ChatGPT's Plan:

---

# 🧭 **Budget Beyond – Development Roadmap**

A full-stack personal management dashboard built with **Flask**, **Python**, **HTML/CSS/JS**, and **SQLite**.

---

## 🧱 **Phase 1: Project Setup**

✅ **Goal:** Get the environment, structure, and version control ready.

* [x] Initialize Git repo and GitHub remote
* [x] Clone on both systems (Windows & Mac)
* [x] Create Flask project structure
* [x] Add virtual environments (`venv`) for both devs
* [x] Install dependencies:

  ```bash
  pip install Flask Flask-WTF Flask-Login Flask-SQLAlchemy Flask-Migrate python-dotenv bcrypt email-validator pytest coverage flake8
  ```
* [x] Generate and test `requirements.txt`
* [x] Create working `run.py`, `app/__init__.py`, and `app/routes.py`
* [x] Add basic `home.html` page → ✅ Flask verified working

---

## 🧩 **Phase 2: Core Architecture**

✅ **Goal:** Build the foundation of the app.

* [ ] Create a `base.html` template (header, nav, footer)
* [ ] Make `home.html` extend `base.html`
* [ ] Add routes for:

  * `/` → Home
  * `/expenses` → Expense Tracker
  * `/bills` → Bill Reminder
  * `/tasks` → To-Do List
* [ ] Connect Jinja templates with route logic
* [ ] Add navigation bar linking all pages

---

## 💾 **Phase 3: Database Integration**

✅ **Goal:** Connect the app to SQLite.

* [ ] Configure SQLAlchemy in `app/__init__.py`
* [ ] Create models:

  * `User` (id, username, email, password_hash)
  * `Expense` (id, user_id, category, amount, date, notes)
  * `Bill` (id, user_id, name, due_date, amount, paid)
  * `Task` (id, user_id, title, due_date, completed)
* [ ] Set up `Flask-Migrate` for DB migrations

  ```bash
  flask db init
  flask db migrate -m "Initial migration"
  flask db upgrade
  ```
* [ ] Verify DB file in `instance/budgetbeyond.db`

---

## 🔐 **Phase 4: Authentication System**

✅ **Goal:** Add user login and registration.

* [ ] Use `Flask-Login` for session handling
* [ ] Create forms with `Flask-WTF`:

  * RegisterForm
  * LoginForm
* [ ] Add routes for `/register`, `/login`, `/logout`
* [ ] Protect dashboard routes (only accessible when logged in)
* [ ] Hash passwords with `bcrypt`

---

## 💰 **Phase 5: Expense Tracker**

✅ **Goal:** Let users track spending.

* [ ] Create Expense model (if not done)
* [ ] Add `/expenses` page to:

  * Display list of expenses
  * Add new expense (category, amount, date, note)
  * Edit / delete existing expenses
* [ ] Use Flask-WTF form for new expenses
* [ ] Add charts using Chart.js (`static/js/expenses.js`)

  * Monthly spending chart
  * Category distribution pie chart

---

## 🧾 **Phase 6: Bill Tracker & Reminders**

✅ **Goal:** Manage and visualize upcoming bills.

* [ ] Create `/bills` page
* [ ] Add form to input:

  * Bill name
  * Amount
  * Due date
  * Status (Paid/Unpaid)
* [ ] Automatically color-code overdue bills
* [ ] Optionally send (or simulate) reminders
* [ ] Show summary bar: “3 bills due soon”

---

## ✅ **Phase 7: To-Do List System**

✅ **Goal:** Manage personal or project tasks.

* [ ] Create `/tasks` page
* [ ] Add simple CRUD operations:

  * Add new task
  * Mark complete/incomplete
  * Delete task
* [ ] Add filters: “Today”, “This Week”, “Completed”
* [ ] Optional: add tags or categories

---

## 🎨 **Phase 8: Styling and Frontend Polish**

✅ **Goal:** Make it look great.

* [ ] Add consistent styling to `styles.css`
* [ ] Add a light/dark mode toggle
* [ ] Use a color palette that fits the theme
* [ ] Make pages mobile-friendly (CSS Flexbox/Grid)
* [ ] Add a favicon and logo to `static/images/`

---

## 🧠 **Phase 9: Quality and Testing**

✅ **Goal:** Ensure everything runs smoothly.

* [ ] Write unit tests with `pytest`
* [ ] Test routes, database models, and forms
* [ ] Use `coverage` to measure test completion
* [ ] Lint and format with `flake8`

---

## ☁️ **Phase 10: Final Touches & Deployment**

✅ **Goal:** Ship it!

* [ ] Update README with setup instructions
* [ ] Add screenshots / preview GIFs
* [ ] Prepare `.env` for environment variables
* [ ] Deploy on Render / Railway / FlaskAnywhere
* [ ] Add version tag: `v1.0.0` 🎉

---

## 🧑‍🤝‍🧑 **Collaboration Rules**

* **Always** `git pull origin main` before starting work
* **Commit frequently** with clear messages
* Work on **feature branches**:

  ```
  git add .
  git commit -m "Whatever message"
  git push origin main
  ```
* Open a **pull request** → review → merge to main

---

## 🗂️ **Optional Next Phases**

* [ ] Multi-currency support
* [ ] Export data to CSV/PDF
* [ ] Notifications & email reminders
* [ ] Shared/group budgeting
* [ ] Cloud sync
* [ ] AI-based financial insights (e.g., spending trends, saving tips)
* [ ] Integration with external APIs (e.g., Plaid for bank data)
* [ ] Budget planning templates
* [ ] Gamification (e.g., rewards for saving goals)

---

Would you like me to also include **a section with estimated time per phase** (e.g., “Phase 3: ~2 days”) so you can use it as a schedule?