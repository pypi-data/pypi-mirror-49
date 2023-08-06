class Sql_Query(object):
    def __init__(self):
        pass

    def get_colums_value_str(self, column_value, column_type):
        return column_value

    def get_select_colum_str(self, column_name, column_value, column_type,is_expression=True, with_col_name=False):
        value_str = self.get_colums_value_str(column_value, column_type)
        if with_col_name:
            column_str = f"""{value_str} AS [{column_name}]"""
        else:
            column_str = value_str
        return column_str

    def get_update_colum_str(self, column_name, column_value, column_type):
        value_str = self.get_colums_value_str(column_value, column_type)
        column_str = f"""[{column_name}]={value_str}"""
        return column_str

    def get_condition_colum_str(self, column_name, column_value, column_type):
        value_str = self.get_colums_value_str(column_value, column_type)
        if value_str == "Null":
            column_str = f"""[{column_name}] is {value_str}"""
        else:
            column_str = f"""[{column_name}]={value_str}"""
        return column_str

    # Condition的条件,用与1：判断是否存在，2：更新时的Where
    def get_condition_str(self, title_dict, row_dict, key_list):
        condition_str_list = []
        for column_name in key_list:
            # 获取该列的值类型
            column_type = title_dict[column_name]
            # 获取Value
            column_value = row_dict[column_name]
            column_str = self.get_condition_colum_str(
                column_name, column_value, column_type)
            condition_str_list.append(column_str)
        # 返回Where语句的条件
        return ' and '.join(condition_str_list)

    # 获取需要更新的列，排除主键
    def get_update_str(self, title_dict, row_dict, key_list):
        update_str_list = []
        for column_name in row_dict:
            # 主键列不需要更新
            if column_name not in key_list and column_name in title_dict:
                # 获取该列的值类型
                column_type = title_dict[column_name]
                # 获取Value
                column_value = row_dict[column_name]
                column_str = self.get_update_colum_str(
                    column_name, column_value, column_type)
                update_str_list.append(column_str)
        if len(update_str_list) > 0:
            columStr = ','.join(update_str_list)
        else:
            columStr = ""
        return columStr

    # 更新数据
    def get_update_sql(self, table_name, title_dict, row_dict, key_list):
        condition_str = self.get_condition_str(title_dict, row_dict, key_list)
        update_str = self.get_update_str(title_dict, row_dict, key_list)
        if update_str == "":
            update_sql = ""
        else:
            update_sql = f"""update t set {update_str} from {table_name} t with(nolock) 
        where {condition_str}
        """
        return update_sql

    def get_insert_title_str(self, table_name, dict_title):
        title_list = []
        for title in dict_title:
            title_list.append(f"[{title}]")
        insert_title_str = f"""Insert Into {table_name} ({','.join(title_list)})"""
        return insert_title_str

    # 从字典中生成数据行
    def get_select_row_str(self, title_dict, row_dict,expression_list=[]):
        list_column = []
        for column_name in title_dict:
            column_value = row_dict[column_name]
            column_type = title_dict[column_name]
            coumn_str = self.get_select_colum_str(
                column_name, column_value, column_type)
            list_column.append(coumn_str)
        select_str = "Select "+",".join(list_column)
        return select_str

    # 将数据字典中的行，拼接入sql语句中
    def get_select_data_str(self, data_sql, title_dict, row_dict):
        select_data_str = ""
        select_row_str = self.get_select_row_str(title_dict, row_dict)
        select_data_str += f"{select_row_str}\n" if data_sql == "" else f"""Union All\n" {select_row_str}"""
        return data_sql
