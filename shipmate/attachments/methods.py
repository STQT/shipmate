def create_attachment(task_serializer, class_name, rel_data):
    """ Created QuoteAttachment, LeadsAttachment and OrderAttachment instances"""
    class_name.objects.create(
        title=task_serializer.text,
        user=task_serializer.user,
        marked=False,
        **rel_data
    )
    # TODO: Update title, second title for any attachment types
