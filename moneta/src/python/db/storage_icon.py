""" Module for handling images for using in current, income, expand."""

from core.db.db_helper import DbHelper


class StorageIcon(DbHelper):
    """
    Model for interacting with icons.
    """
    @staticmethod
    def get_all_icons():
        """
        Returns a dict with id and css of all icons
        :return: list of available icons
        """

        sql = """
            SELECT id, css
            FROM  image;
            """
        args = ()
        query = StorageIcon._make_select(sql, args)
        return query

    @staticmethod
    def get_icon_by_id(image_id):
        """
        Getting icon from database by requested id
        :params: requested image id
        :returns: icon from database.
        """
        sql = """
            SELECT css
            FROM  image
            WHERE id = %s;
            """
        args = (image_id,)
        icon = StorageIcon._make_select(sql, args)
        return icon[0]['css']

    @staticmethod
    def get_icon_choices():
        """
        Returns a choice list  of icons, available for for a particular category,
        for using in forms.
        :params: category for which we need a list of icons
        :return: choice list of available icons
        """
        icons = StorageIcon.get_all_icons()
        if icons:
            return tuple([(str(icon['id']), icon['css']) for icon in icons])
        return (1, 'Sorry, but icons are currently not available.')

__all__ = ['StorageIcon']
