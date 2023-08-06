"""
This file contains static SQL queries that can be used in asset access
"""
ALL_TABLES = (
    "SELECT relname AS DataBase "
    "FROM pg_catalog.pg_class "
    "WHERE relnamespace={} ORDER BY relname DESC"
)

OID_QUERY = (
    "SELECT oid FROM pg_catalog.pg_namespace "
    "WHERE nspname='org_{}'"
)
