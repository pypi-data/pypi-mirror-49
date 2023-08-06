from lmf.dbv2 import db_command, db_write, db_query
from os.path import join, dirname
import pandas as pd


def get_conp(name, database=None):
    path1 = join(dirname(__file__), "cfg_db")
    if database is None:
        df = db_query("select * from cfg where schema='%s' " % name, dbtype='sqlite', conp=path1)
    else:
        df = db_query("select * from cfg where schema='%s' and database='%s' " % (name, database), dbtype='sqlite',
                      conp=path1)
    conp = df.values.tolist()[0]
    return conp


def get_conp1(name):
    path1 = join(dirname(__file__), "cfg_db")

    df = db_query("select * from cfg where database='%s' and schema='public' " % name, dbtype='sqlite', conp=path1)
    conp = df.values.tolist()[0]
    return conp


def command(sql):
    path1 = join(dirname(__file__), "cfg_db")
    db_command(sql, dbtype="sqlite", conp=path1)


def query(sql):
    path1 = join(dirname(__file__), "cfg_db")
    df = db_query(sql, dbtype='sqlite', conp=path1)
    return df


def update(user=None, password=None, host=None):
    if host is not None:
        sql = "update cfg set host='%s' " % host
        command(sql)
    if user is not None:
        sql = "update cfg set user='%s' " % user
        command(sql)
    if password is not None:
        sql = "update cfg set password='%s' " % password
        command(sql)


def add_conp(conp):
    sql = "insert into cfg values('%s','%s','%s','%s','%s')" % (conp[0], conp[1], conp[2], conp[3], conp[4])
    command(sql)


data1 = {

        "qy": ["www_bidding_citic","bidding_sinopec_com","eps_shmetro_com","qg_zfcg","qg_ggzy",
         "mall_cdtbuy_cn","www_haierbid_com","www_hnbidding_com","www_hnzbcg_com_cn",
        # 新增
        "zbcg_nenu_edu_cn","cgw_xjbt_gov_cn",
        "www_gcbidding_com","www_gztpc_com","www_guangxibid_com_cn","zbb_nankai_edu_cn",
        "www_sxzzgs_com","www_soeasyjc_com","scs_inspur_com","www_hnsl_gov_cn",
        "www_cntec_com_cn","www_zybtp_com",
        # 2019/7/22
        "www_ztgh_com_cn","www_tsjj_com_cn","zc_gtcloud_cn",
        "www_cfcpn_com","www_ceiea_com","www_sntba_com","www_jxtb_org_cn",
        "sdhsg_com",

        ],



    }


def get_df():
    data = []
    for w in data1.keys():
        tmp1 = data1[w]
        for w1 in tmp1:
            tmp = ["postgres", "since2015", "192.168.4.201", 'zlest1', w1]
            data.append(tmp)

    df = pd.DataFrame(data=data, columns=["user", 'password', "host", "database", "schema"])
    return df



def create_all_schemas():
    conp = get_conp1('zlest1')
    for w in data1.keys():
        tmp1=data1[w]
        for w1 in tmp1:
            sql = "create schema if not exists %s" % w1
            db_command(sql, dbtype="postgresql", conp=conp)



def update_schemas(schema_list=[] ,drop_html=False):
    '''
        :param schema_list: 一个包含多个schema的列表; list 格式
        :param drop_html: False 不删除gg_html;True 删除gg_html;just 只删除gg_html
        :return:
    '''
    conp = get_conp1('zlest1')
    sql1 = '''select schemaname,tablename from pg_tables;'''
    tables = db_query(sql1, dbtype='postgresql', conp=conp)
    for table in tables.values:

        if drop_html == 'just':
            if (table[0] in schema_list) and ('gg_html' in table[1]):
                sql2 = '''drop table "%s"."%s" ''' % (table[0], table[1])
                db_command(sql2, dbtype="postgresql", conp=conp)
                print('已删除 %s.%s 表' % (table[0], table[1]))

        elif not drop_html:

            if (table[0] in schema_list) and ('gg_html' not in table[1]):
                sql2 = '''drop table "%s"."%s" ''' % (table[0], table[1])
                db_command(sql2, dbtype="postgresql", conp=conp)
                print('已删除 %s.%s 表' % (table[0], table[1]))

        else:
            if table[0] in schema_list:
                sql2 = '''drop table "%s"."%s" ''' % (table[0], table[1])
                db_command(sql2, dbtype="postgresql", conp=conp)
                print('已删除 %s.%s 表' % (table[0], table[1]))
    return 'over'


# # 生成cfg_db
# df=get_df()
# db_write(df,'cfg',dbtype='sqlite',conp=join(dirname(__file__),"cfg_db"))
# add_conp(["postgres","since2015","192.168.4.201",'zlest1','public'])
#
# # 查看cfg_db
# df=query("select * from cfg")
# print(df.values)
