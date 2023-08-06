from apex_client.objects import ApexObject


class Comment(ApexObject):
    valid_properties = ['id', 'text', 'parent', ]
    date_properties = ['date_created', 'date_modified', 'delete_date', ]
