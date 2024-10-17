#!/bin/bash
echo "BUILD START"
# تثبيت المتطلبات
python -m pip install -r requirements.txt

# جمع الملفات الثابتة
python manage.py collectstatic --noinput --clear

echo "BUILD END"
