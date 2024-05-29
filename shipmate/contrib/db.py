from django.db import connection


def update_sequences(site_model, table_name):  # noqa
    max_obj = site_model.objects.order_by('-id').first()
    if max_obj:
        max_id = max_obj.id
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT last_value from {table_name}")
            (current_id,) = cursor.fetchone()
            if current_id <= max_id:
                cursor.execute(
                    f"alter sequence {table_name} restart with %s",
                    [max_id + 1],
                )
