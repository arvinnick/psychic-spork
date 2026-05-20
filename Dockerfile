FROM python:3.12-slim

# ۱. تعیین ورک‌دایرکتوری (خیلی مهمه)
WORKDIR /code

# ۲. کپی کردن فایل نیازمندی‌ها قبل از کپی کل کد (برای کش شدن بهتر در داکر)
COPY requirements.txt /code/requirements.txt

# ۳. نصب نیازمندی‌ها
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# ۴. کپی کردن کل سورس‌کد
COPY ./app /code/app
COPY seed_db.py /code/seed_db.py
COPY ./tests /code/tests
RUN pytest
# ۵. اجرای برنامه (بدون --reload)
# در محیط داکر بهتره از --host 0.0.0.0 استفاده کنی
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]