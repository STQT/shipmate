def create_attachment(task_serializer, class_name, rel_data):
    task_attachment_instance = task_serializer.save()
    class_name.objects.create(
        title=task_attachment_instance.text,
        user=task_attachment_instance.user,
        marked=False,
        **rel_data
    )
