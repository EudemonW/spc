# 处理mysql的参数

# mysql
m_host = '127.0.0.1'
m_port = 3306
m_user = 'root'
m_password = 'root'
m_database = 'spc'
m_charset = 'utf8'  # 编码千万不要加- 如果写成了utf-8会直接报错
m_autocommit = True  # 这个参数配置完成后  增删改操作都不需要在手动加conn.commit了
