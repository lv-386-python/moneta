""" Module for handling images for using in current, income, expand."""
from core.db.db_helper import Expend


class StorageIcon(Expend):
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
            WHERE category=%s;
            """
        args = (category,)
        query = StorageIcon._make_select(sql, args)
        return query

    @staticmethod
    def get_icon_choices_by_category(category):
        """
        Returns a choice list  of icons, available for for a particular category,
        for using in forms.
        :params: category for which we need a list of icons
        :return: choice list of available icons
        """
        icons = StorageIcon.get_icons(category)
        return tuple([(str(icon['id']), icon['css']) for icon in icons])
