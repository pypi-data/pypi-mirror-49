from .query import query
import pandas as pd


def student(df,*Args):  #cname/ename/sex
    """merge student info. *Args = cname/ename/sex
    """
    info = ','.join(Args)
    q = query(f'select distinct pyccode,{info} from views.student_info')
    return df.merge(q,how='left')

def schooling(df,*Args):   #ename/cname/sex/cardnum/form/class/num	
    """merge schooling info. *Args = #ename/cname/sex/cardnum/form/class/num
    """
    info = ','.join(Args) 
    q = query(f'select pyccode,{info} from views.student_info_current')
    return df.merge(q,how='left')

def schooling_in(df,year,*Args):   #ename/cname/sex/cardnum/form/class/num	
    """merge schooling info from a specific sch_year. *Args = #ename/cname/sex/cardnum/form/class/num
    """
    info = ','.join(Args) 
    q = query(f'select pyccode,{info} from views.student_info where sch_year={year}')
    return df.merge(q,how='left')

def staff(df,*Args):   #cname/ename/sname
    """merge staff info. *Args = #cname/ename/sname
    """
    info = ','.join(Args) 
    q = query(f'select pyccode,{info} from views.teacher_info')
    return df.merge(q,how='left')