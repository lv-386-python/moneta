""" Module for handling images for using in current, income, expand."""
from core.db.db_helper import DbHelper


class StorageIcon(DbHelper):
    """
    Model for interacting with icons.
    """

    @staticmethod
    def get_icons(category):
        """
        Returns a list of icons, available for for a particular category.
        :params: category for which we need a list of icons
        :return: list of available icons
        """
        sql = f"""
            SELECT *
            FROM  image
            WHERE category='{category}';
            """
        query = StorageIcon._make_select(sql)
        icon_list = []
        for row in query:
            icon_list.append({
                'icon_id': row['id'],
                'css': row['css'],
                'category': row['category']
            })
        return icon_list

    @staticmethod
    def get_icon_choices_by_category(category):
        """
        Returns a choice list  of icons, available for for a particular category,
        for using in forms.
        :params: category for which we need a list of icons
        :return: choice list of available icons
        """
        icons = StorageIcon.get_icons(category)

        return tuple([(str(icon['icon_id']), icon['css']) for icon in icons])
