"""
    This is a helper class and should only be used
    by single mysql db projects.
"""
import re
from sqlalchemy.ext.declarative.api import (
    declared_attr,
    has_inherited_table,
    declarative_base,
)


class _Base_:
    """
        This class allows us to base the tablename off the class name.
        We also check for has_inherited_table, so as not to redeclare.
        We make the table name to lower case and underscored.

        We don't implement the primary key in base as some classes will use
        a foreign key to a parent table as their primary key.

        see: http://docs.sqlalchemy.org/
    """

    @declared_attr
    def __tablename__(self):
        if has_inherited_table(self):
            return None
        name = self.__name__  # pylint: disable=E1101
        return name[0].lower() + re.sub(
            r"([A-Z])", lambda m: "_" + m.group(0).lower(), name[1:]
        )

    __table_args__ = {"mysql_engine": "InnoDB"}


Base = declarative_base(cls=_Base_)
