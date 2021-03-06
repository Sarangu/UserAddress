import pymysql
import json
import logging

import middleware.context as context

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class RDBService:

    def __init__(self):
        pass

    @classmethod
    def _get_db_connection(cls):

        db_connect_info = context.get_db_info()

        logger.info("RDBService._get_db_connection:")
        logger.info("\t HOST = " + db_connect_info['host'])

        db_info = context.get_db_info()

        db_connection = pymysql.connect(
           **db_info,
            autocommit=True
        )
        return db_connection

    @classmethod
    def run_sql(cls, sql_statement, args, fetch=False):

        conn = RDBService._get_db_connection()

        try:
            cur = conn.cursor()
            res = cur.execute(sql_statement, args=args)
            if fetch:
                res = cur.fetchall()
        except Exception as e:
            conn.close()
            raise e

        return res

    @classmethod
    def check_if_issue(cls, sql_statement, args, fetch=False):

        conn = RDBService._get_db_connection()

        try:
            cur = conn.cursor()
            res = cur.execute(sql_statement, args=args)
            if fetch:
                res = cur.fetchall()
        except Exception as e:
            conn.close()
            return 1

        return 0

    @classmethod
    def get_by_prefix(cls, db_schema, table_name, column_name, value_prefix):

        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        sql = "select * from " + db_schema + "." + table_name + " where " + \
            column_name + " like " + "'" + value_prefix + "%'"
        print("SQL Statement = " + cur.mogrify(sql, None))

        res = cur.execute(sql)
        res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def get_where_clause_args(cls, template):

        terms = []
        args = []
        clause = None

        if template is None or template == {}:
            clause = ""
            args = None
        else:
            for k,v in template.items():
                terms.append(k + "=%s")
                args.append(v)

            clause = " where " +  " AND ".join(terms)


        return clause, args

    @classmethod
    def find_by_template(cls, db_schema, table_name, template, limit, offset, field_list):

        wc,args = RDBService.get_where_clause_args(template)

        conn = RDBService._get_db_connection()
        cur = conn.cursor()

        limit_offset_stmt = ''
        if limit is not None and offset is not None:
            limit_offset_stmt = "limit " + limit + " offset " + offset
        elif limit is not None:
            limit_offset_stmt = "limit " + limit
        if field_list is None:
            sql = "select * from " + db_schema + "." + table_name + " " + wc + " " + limit_offset_stmt
        else:
            sql = "select " + field_list + " from " + db_schema + "." + table_name + " " + wc + " " + limit_offset_stmt
        res = RDBService.run_sql(sql, args, True)
        # res = cur.execute(sql, args=args)
        # res = cur.fetchall()

        conn.close()

        return res

    @classmethod
    def create(cls, db_schema, table_name, create_data):

        cols = []
        vals = []
        args = []

        for k,v in create_data.items():
            cols.append(k)
            vals.append('%s')
            args.append(v)


        cols_clause = "(" + ",".join(cols) + ")"
        vals_clause = "values (" + ",".join(vals) + ")"

        sql_stmt = "insert into " + db_schema + "." + table_name + " " + cols_clause + \
            " " + vals_clause

        res = RDBService.run_sql(sql_stmt, args)
        return res

    @classmethod
    def delete_by_template(cls, db_schema, table_name, template):

        wc, args = RDBService.get_where_clause_args(template)

        sql = "delete from " + db_schema + "." + table_name + " " + wc

        res = RDBService.run_sql(sql, args)
        return res

    @classmethod
    def update_by_primary_key(cls, db_schema, table_name, key, template):

        wc, args_wc = RDBService.get_where_clause_args(key)

        cols = []
        vals = []
        args = []
        terms = []

        for k, v in template.items():
            cols.append(k)
            vals.append('%s')
            args.append(v)
            terms.append(k + "=%s")

        new_values = " , ".join(terms)

        sql = "update " + db_schema + "." + table_name + " set " + new_values + " " + wc
        # check = RDBService.check_if_issue(sql, (args, args_wc))
        # if check:
        #     return 2
        res = RDBService.run_sql(sql, (args, args_wc))
        return res