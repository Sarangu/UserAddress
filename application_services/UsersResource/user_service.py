from application_services.BaseApplicationResource import BaseRDBApplicationResource
import database_services.RDBService as d_service


class UserResource(BaseRDBApplicationResource):

    def __init__(self):
        super().__init__()

    @classmethod
    def get_by_template(cls, template):
        res = d_service.RDBService.find_by_template("UserAddress", "user",
                                                    template, None)
        return res

    @classmethod
    def get_by_primary_key(cls, key):
        template = {"user_no":key}
        res = d_service.RDBService.find_by_template("UserAddress", "user",
                                                    template, None)
        return res

    @classmethod
    def add_template_to_table(cls, template):
        res = d_service.RDBService.create("UserAddress", "user", template)
        return res

    @classmethod
    def delete_by_primary_key(cls, key):
        template = {"user_no":key}
        res = d_service.RDBService.delete_by_template("UserAddress", "user", template)
        return res

    @classmethod
    def update_by_primary_key(cls, key, template):
        pk = {"user_no":key}
        res = d_service.RDBService.update_by_primary_key("UserAddress", "user", pk, template)
        return res

    @classmethod
    def get_address_by_user_no(cls, key):
        template = {"user_number": key}
        res = d_service.RDBService.find_by_template("UserAddress", "address",
                                                    template, None)
        return res

    @classmethod
    def delete_address_by_user_no(cls, key):
        template = {"user_number":key}
        res = d_service.RDBService.delete_by_template("UserAddress", "address", template)
        return res

    @classmethod
    def update_address_by_user_no(cls, key, template):
        pk = {"user_number": key}
        res = d_service.RDBService.update_by_primary_key("UserAddress", "address", pk, template)
        return res

    @classmethod
    def add_address_for_user(cls, userid, template):
        template['user_number'] = userid
        res = d_service.RDBService.create("UserAddress", "address", template)
        return res

    @classmethod
    def get_links(cls, resource_data):
        pass

    @classmethod
    def get_data_resource_info(cls):
        return 'aaaaaF21E6156', 'users'
