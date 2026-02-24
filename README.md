# Flow - Personal Finance Tracker

Flow is a Django-based finance management application that is highly simplified version of a finance app I create and use myself. 
Decided this will be a nice and interesting project to try and reverse engineer the app to a more simple version. 
Built for the SoftUni Django Basics Regular Exam. Maybe will upgrade it to a more advanced version on the Advanced coure.

## 📋 Features

- **Dashboard Overview**: View financial summary, recent transactions, top spending categories, and active savings goals
- **Transaction Management**: Create, read, update, and delete income/expense entries
- **Category Management**: Organize transactions with customizable spending categories and budget limits
- **Savings Goals**: Set financial targets and track progress with visual indicators
- **Filtering & Sorting**: Filter transactions by type and sort by date or amount
- **Responsive Design**: Bootstrap 5 ensures mobile-friendly interface

## 📊 Sample Data Included

The project comes with **pre-loaded sample data** through migration seed files, so o manual data entry required to test the projet app. 
All amounts are AI generated as this was manual repetitive process that can be sped up by AI:

### Categories (10 pre-defined)
- Income categories: Salary, Freelance
- Expense categories: Groceries, Rent, Utilities, Transportation, Dining Out, Entertainment, Shopping, Healthcare
- Each category has color coding and budget limits

### Transactions (13 sample transactions)
- **Income examples**: Monthly salary, freelance projects, bonus payments
- **Expense examples**: Rent, utilities, groceries, dining out, shopping, transportation
- Transactions span the last 30 days with amounts and descriptions

### Savings Goals (5 active goals)
- **Summer Vacation Fund**: $2,000 target ($750 saved, 90 days remaining)
- **New Laptop**: $1,500 target ($450 saved, 60 days remaining)
- **Emergency Fund**: $5,000 target ($2,100 saved, 180 days remaining)
- **New Smartphone**: $800 target ($200 saved, 45 days remaining)
- **Christmas Gifts**: $600 target ($100 saved, 270 days remaining)

All sample data is created through migration files (`0002_seed_*.py` in each app). You can modify or delete this data through the application interface just like real user data.

## 📁 Project Structure

**Flow** (Project Root):
- **Flow** (Main Project Directory):
  - `__init__.py`
  - `settings.py`
  - `urls.py`
  - `views.py`
  - `wsgi.py`
- **categories** (App):
  - **migrations**:
    - `0001_initial.py`
    - `0002_seed_categories.py`
    - `__init__.py`
  - **templates**:
    - **categories**:
      - `category_list.html`
      - `category_detail.html`
      - `category_form.html`
      - `category_confirm_delete.html`
  - `__init__.py`
  - `admin.py`
  - `apps.py`
  - `forms.py` - CategoryForm
  - `models.py` - Category model
  - `urls.py` - Category URL routes
  - `views.py` - Category views
- **transactions** (App):
  - **migrations**:
    - `0001_initial.py`
    - `0002_seed_transactions.py`
    - `__init__.py`
  - **templatetags**:
    - `__init__.py`
    - `flow_extras.py` - Custom filters: currency, progress_percentage
  - **templates**:
    - **transactions**:
      - `dashboard.html`
      - `transaction_list.html`
      - `transaction_detail.html`
      - `transaction_form.html`
      - `transaction_filter.html`
      - `transaction_confirm_delete.html`
  - `__init__.py`
  - `admin.py`
  - `apps.py`
  - `forms.py` - TransactionForm
  - `models.py` - Transaction model
  - `urls.py` - Transaction URL routes
  - `views.py` - Transaction views
- **goals** (App):
  - **migrations**:
    - `0001_initial.py`
    - `0002_seed_goals.py`
    - `__init__.py`
  - **templates**:
    - **goals**:
      - `goal_list.html`
      - `goal_detail.html`
      - `goal_form.html`
      - `goal_confirm_delete.html`
  - `__init__.py`
  - `admin.py`
  - `apps.py`
  - `forms.py` - SavingsGoalForm
  - `models.py` - SavingsGoal model
  - `urls.py` - Goal URL routes
  - `views.py` - Goal views
- **templates** (Global Templates):
  - `base.html` - Base template with navigation and footer
  - `nav.html` - Navigation partial
  - `footer.html` - Footer partial
  - `404.html` - Custom error page
- `manage.py` - Django management script
- `requirements.txt` - Project dependencies
- `.gitignore` - Git ignore rules
- `README.md` - Project documentation
