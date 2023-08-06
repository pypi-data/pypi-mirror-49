from lmf.dbv2 import db_command ,db_query
from lmf.bigdata import pg2csv
import sys 
import os 
from fabric import Connection
from zlhawq.core import add_quyu_tmp,restart_quyu_tmp
from zlhawq.zlsys.core import add_quyu_tmp as zlsys_add_quyu_tmp 
from zlhawq.zlsys.core import restart_quyu_tmp as zlsys_restart_quyu_tmp 
import traceback
from zlhawq.data import zhulong_diqu_dict,zl_diqu_dict,zl_shenpi_dict
#####对zhulong1 有效,从192.168.4.175 往192.168.4.179 更新


def add_quyu_db_local(quyu,tag='all'):
    sql="select * from public.cfg where quyu='%s' "%(quyu)
    df=db_query(sql,dbtype="postgresql",conp=['postgres','since2015','192.168.4.201','postgres','publc'])
    conp_pg=[df.at[0,'usr'],df.at[0,'password'],df.at[0,'host'],df.at[0,'db'],df.at[0,'schema']]


    conp_hawq=["gpadmin","since2015","192.168.4.179","base_db","v3"]
    dir='/data/lmf'
    addr='192.168.4.187:8111'
    if quyu.startswith('zlsys'):
        zlsys_add_quyu_tmp(quyu,conp_pg,conp_hawq,dir,addr,tag=tag)
    else:
        add_quyu_tmp(quyu,conp_pg,conp_hawq,dir,addr,tag=tag)

def restart_quyu_db_local(quyu):

    tag='all'
    sql="select * from public.cfg where quyu='%s' "%(quyu)
    df=db_query(sql,dbtype="postgresql",conp=['postgres','since2015','192.168.4.201','postgres','publc'])
    conp_pg=[df.at[0,'usr'],df.at[0,'password'],df.at[0,'host'],df.at[0,'db'],df.at[0,'schema']]

    conp_hawq=["gpadmin","since2015","192.168.4.179","base_db","v3"]
    dir='/data/lmf'
    addr='192.168.4.187:8111' 
    if quyu.startswith('zlsys'):
        zlsys_restart_quyu_tmp(quyu,conp_pg,conp_hawq,dir,addr,tag=tag)
    else:
        restart_quyu_tmp(quyu,conp_pg,conp_hawq,dir,addr,tag=tag)


def add_quyu_db_remote(quyu,tag='all'):
    conp_remote=["root@192.168.4.187","rootHDPHAWQDatanode5@zhulong"]
    c=Connection(conp_remote[0],connect_kwargs={"password":conp_remote[1]})
    try:
        c.run("""/opt/python35/bin/python3 -c "from zltask.hawq import add_quyu_db_local;add_quyu_db_local('%s','%s') " """%(quyu,tag),pty=True,encoding='utf8')
    except:
        traceback.print_exc()
        raise RuntimeError('Error')
    finally:
        c.close()

def restart_quyu_db_remote(quyu):
    conp_remote=["root@192.168.4.187","rootHDPHAWQDatanode5@zhulong"]
    c=Connection(conp_remote[0],connect_kwargs={"password":conp_remote[1]})
    try:
        c.run("""/opt/python35/bin/python3 -c "from zltask.hawq import restart_quyu_db_local;restart_quyu_db_local('%s') " """%(quyu),pty=True,encoding='utf8')
    except:
        traceback.print_exc()
        raise RuntimeError('Error')
    finally:
        c.close()


add_quyu=add_quyu_db_remote

restart_quyu=restart_quyu_db_remote