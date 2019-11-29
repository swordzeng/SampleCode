import sys



from PyQt5.QtSql import QSqlDatabase,QSqlQuery



class ado_mydadb:
    def __init__(self):
        #super(ado_mydadb, self).__init__()
        db=QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('mydb.db')
        if not db.open():
            print("无法建立数据库连接")
            return False

    def insert_db(self, bookinfo):
        """
        新增一条图书记录
        """
        self.books = self.load()


    def load(self, jobid):
        """
        载入数据
        """
        query = QSqlQuery()
        query.exec_(jobid)
        #query.next()
        return query

if __name__ == '__main__':
    que=ado_mydadb()
    #query = QSqlQuery()
    #rilis={}
    qetl="""
        select 
            case
                when job_type in ('2','3') then '2'
                else job_type
            end as job_type
            ,sum(case
                when job_status = 'Done' then 1
                else 0
            end) as job_done
            ,sum(case
                when job_status = 'Ready' then 1
                else 0
            end) as job_ready
            ,sum(case
                when job_status in ( 'Running','Loading') then 1
                else 0
            end) as job_run
            ,sum(case
                when job_status = 'Faild' then 1
                else 0
            end) as job_fal
            ,count(*)  as cnt_job
        from etl_job
        group by 1
    """
    rlist=que.load(qetl)

    while rlist.next():
        job_type = rlist.record().indexOf('job_type')
        job_type = rlist.value(job_type)
        job_done = rlist.record().indexOf('job_done')
        job_done = rlist.value(job_done)
        job_ready = rlist.record().indexOf('job_ready')
        job_ready = rlist.value(job_ready)
        job_run = rlist.record().indexOf('job_run')
        job_run = rlist.value(job_run)
        job_fal = rlist.record().indexOf('job_fal')
        job_fal = rlist.value(job_fal)
        cnt_job = rlist.record().indexOf('cnt_job')
        cnt_job = rlist.value(cnt_job)

        print(job_type,job_done,job_ready,job_run,job_fal,cnt_job)
    #rlist.add("asdf")
    #print(type(rlist))

