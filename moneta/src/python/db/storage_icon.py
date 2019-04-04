""" Module for handling images for using in current, income, expand."""

from src.python.core.db import db_helper as db


class StorageIcon:
    """
    Model for interacting with icons.
    """

    def __init__(self, icon_id, css, category):
        self.icon_id = icon_id
        self.css = css
        self.category = category

    def __repr__(self):
        return f"<icon - {self.icon_id}>"

    def __str__(self):
        return f"icon - id:{self.icon_id}"

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
        query = db.select_sql(sql)
        icon_list = []
        for row in query:
            icon = StorageIcon(*row)
            icon_list.append(icon)
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

        return tuple([(str(icon.icon_id), icon.css) for icon in icons])
