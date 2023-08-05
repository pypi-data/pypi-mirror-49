import time

from zhulong2.gansu import shenghui
from zhulong2.gansu import jinchang

from lmf.dbv2 import db_command

from zhulong2.util.conf import get_conp,get_conp1

#1
def task_shenghui(**args):
    conp=get_conp(shenghui._name_)
    shenghui.work(conp,pageloadtimeout=400,**args)

#2
def task_jinchang(**args):
    conp=get_conp(jinchang._name_)
    jinchang.work(conp,**args)



def task_all():
    bg=time.time()
    try:
        task_shenghui()
        task_jinchang()
    except:
        print("part1 error!")

    ed=time.time()
    cos=int((ed-bg)/60)
    print("共耗时%d min"%cos)


def create_schemas():
    conp=get_conp1('zfcg')
    arr=["gansu_shenghui","gansu_jinchang"]
    for diqu in arr:
        sql="create schema if not exists %s"%diqu
        db_command(sql,dbtype="postgresql",conp=conp)




