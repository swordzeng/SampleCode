from PyQt5.Qt import *
from main_menue import Ui_man

from my_db import ado_mydadb





class main_me(QWidget,Ui_man):

    que=ado_mydadb()

    def __init__(self, parent=None):
        """
        设置一些表格样式
        """
        super(main_me, self).__init__(parent)
        self.setupUi(self)
        self.show_data()

    @pyqtSlot(int,int)
    def on_etl_job_list_cellClicked(self, row, column):
        print("表格被点击了")
        print(self.etl_job_list.currentRow())
        c_row = self.etl_job_list.currentRow()
        etl_job = self.etl_job_list.item(c_row, 0).text()

        self.show_dept_data(etl_job)
    def show_dept_data(self,etl_job):

        sel_cnt = self.etl_job_list.selectedRanges()

        print(sel_cnt)
        if not sel_cnt:
            print("未选中作业")
        else :
            if self.dept_type_all.isChecked():
                print("全部被选中")
                updn_dep = '1'
            elif self.dept_up.isChecked():
                print("上游被选中")
                updn_dep = '2'
            elif self.dept_down.isChecked():
                print("下游被选中")
                updn_dep = '3'

            if self.denpt_all.isChecked():
                print("所有被选中")
                dep = '1'
            elif self.one_dept.isChecked():
                print("一层依赖")
                dep = '2'
            elif self.two_dept.isChecked():
                print("两层依赖")
                dep = '3'

            if updn_dep == '1' and dep == '1':
                pass
            elif updn_dep == '1' and dep == '2':
                dep_job_sql = """
                select 
                    case
                         when t1.etl_job = 'etl_job_code' then '上游'
                        else '下游'
                    end as dep_type
                    ,case
                         when t1.etl_job =  'etl_job_code' then t1.dependent_job
                        else t1.etl_job 
                    end as etl_job
                    ,case
                         when t1.etl_job = 'etl_job_code' then t3.etl_job_nm
                        else t2.etl_job_nm
                    end as etl_job_nm                
                    ,t2.job_status
                from rdm_etl_job_dependent t1
                left join rdm_etl_job_ctrl t2
                        on t1.etl_job = t2.etl_job
                left join rdm_etl_job_ctrl t3
                       on t1.dependent_job = t3.etl_job
                where t1.etl_job =  'etl_job_code'
                or dependent_job =  'etl_job_code'
                order by 1
                """
                new_etl_job_sql = dep_job_sql.replace("etl_job_code",etl_job)
                print(new_etl_job_sql)

            elif updn_dep == '1' and dep == '3':
                pass
            elif updn_dep == '2' and dep == '1':
                pass
            elif updn_dep == '2' and dep == '2':
                pass
            elif updn_dep == '2' and dep == '3':
                pass
            elif updn_dep == '3' and dep == '1':
                pass
            elif updn_dep == '3' and dep == '2':
                pass
            elif updn_dep == '3' and dep == '3':
                pass
            else:
                print('没有选中任何按钮')

            dept = self.que.load(new_etl_job_sql)
            self.dept_tab.clearContents()
            print("显示依赖数据")
            cnt=dept.record().count()
            print(dept.size())
            self.dept_tab.setRowCount(10)
            # self.etl_job_list.insertRow(job_c)
            i = 0
            while dept.next():
                #self.dept_tab.insertRow(1)
                dep_type = dept.record().indexOf('dep_type')
                # job_str = '%d' %(job_str1)
                dep_type1 = QTableWidgetItem(dept.value(dep_type))

                etl_job = dept.record().indexOf('etl_job')
                etl_job1 = QTableWidgetItem(dept.value(etl_job))

                job_name = dept.record().indexOf('etl_job_nm')
                job_name1 = QTableWidgetItem(dept.value(job_name))

                job_st = dept.record().indexOf('job_status')
                job_st1 = QTableWidgetItem(dept.value(job_st))

                print(dept.value(etl_job), dept.value(job_name), dept.value(job_st))

                self.dept_tab.setItem(i, 0, dep_type1)
                self.dept_tab.setItem(i, 1, etl_job1)
                self.dept_tab.setItem(i, 2, job_name1)
                self.dept_tab.setItem(i, 4, job_st1)
                i += 1



    @pyqtSlot(int, int)
    def on_tableWidget_cellClicked(self, row, column):
        print("表格被点击了")
        print(self.tableWidget.currentRow())
        print(self.tableWidget.currentColumn())
        c_row = self.tableWidget.currentRow()
        c_clo = self.tableWidget.currentColumn()
        c_cnt = self.tableWidget.item(c_row,c_clo).text()

        if c_row == 0 :
            job_type = '1'
        elif c_row == 1 :
            job_type = '2'
        elif c_row == 2 :
            job_type = '4'
        elif c_row == 3 :
            job_type = '5'
        elif c_row == 4 :
            job_type = '6'
        elif c_row == 5 :
            job_type = '7'
        elif c_row == 6 :
            job_type = '8'
        elif c_row == 7 :
            job_type = 'ALL'
        else :
            job_type = 'null'

        if c_clo == 0 :
            job_status = 'Done'
        elif c_clo == 1 :
            job_status = 'Ready'
        elif c_clo == 2 :
            job_status = 'Running'
        elif c_clo == 3 :
            job_status = 'Failed'
        elif c_clo == 4 :
            job_status = 'ALL'
        else :
            job_status = 'null'
        print("xuan"+job_status)
        print("xuanz"+job_type)
        self.job_detail(job_type,job_status,int(c_cnt))


#显示点击单元格内具体的作业
    def job_detail(self,job_t,job_st,job_c):
        print("显示数据")
        job_sql = "select etl_job,job_name,job_status from etl_job_view where 1=1"
        if job_t == 'ALL':
            job_sql = job_sql+" AND job_status = '"+job_st+"'"
        elif job_st == 'ALL':
            job_sql = job_sql+" AND job_type = '"+job_t+"'"
        else :
            print(job_st)
            print(job_t)
            job_sql = job_sql + " AND job_status = '" + job_st + "' AND job_type = '"+job_t+"'"
        print(job_sql)
        rlist = self.que.load(job_sql)
        self.etl_job_list.clearContents()
        self.etl_job_list.setRowCount(job_c)
        #self.etl_job_list.insertRow(job_c)
        i = 0
        while rlist.next():
            etl_job = rlist.record().indexOf('etl_job')
            # job_str = '%d' %(job_str1)
            etl_job1 = QTableWidgetItem(rlist.value(etl_job))

            job_name = rlist.record().indexOf('job_name')
            job_name1 = QTableWidgetItem(rlist.value(job_name))

            job_st = rlist.record().indexOf('job_status')
            job_st1 = QTableWidgetItem(rlist.value(job_st))

            print(rlist.value(etl_job), rlist.value(job_name), rlist.value(job_st))

            self.etl_job_list.setItem(i, 0, etl_job1)
            self.etl_job_list.setItem(i, 1, job_name1)
            self.etl_job_list.setItem(i, 2, job_st1)
            i += 1


    def contextMenuEvent(self, event):
        """
        右键菜单
        """
        print("右键点击")
        pass
        #pmenu = QMenu(self)
        #pDeleteAct = QAction('删除行', self.tableWidget)
        #pmenu.addAction(pDeleteAct)
        #pDeleteAct.triggered.connect(self.deleterows)
        #pmenu.popup(self.mapToGlobal(event.pos()))

    def closeEvent(self, event):
        """
        提示保存
        """
        r = QMessageBox.warning(self, "提示", "你确定要关闭软件吗？", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)
        if r == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    @pyqtSlot(int, int)
    def on_tableWidget_2_cellClicked(self, row, column):
        print("表格被点击了")
        print()
        print("表格被点11111击了")



    def click_refase(self):
        #显示作业情况
        self.show_data()
    def auto_refs(self):
        print("刷新按钮已被点击")
    def dep_tog(self):
        print("依赖按钮已被点击")
        c_row = self.etl_job_list.currentRow()
        print(c_row)



        if c_row >= 0:
            etl_job = self.etl_job_list.item(c_row, 0).text()
            sel_cnt = self.etl_job_list.selectedRanges()
            print(etl_job)
            self.show_dept_data(etl_job)
    def find_job(self):
        print("查找按钮已被点击")
        if len(self.find_str.text()) >= 1 :
            pass
            print(self.find_str.text())
    def again_job(self):
        print("重调按钮已被点击")
        print(self.data_dt.text())

    def show_data(self):
        print("show方法被调用了")
        # query = QSqlQuery()
        # rilis={}
        qetl = """
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
                        when job_status = 'Failed' then 1
                        else 0
                    end) as job_fal
                    ,count(*)  as cnt_job
                from rdm_etl_job_ctrl
                group by 1
            """
        rlist = self.que.load(qetl)
        i = 0
        while rlist.next():
            job_done = rlist.record().indexOf('job_done')
            job_str1 = rlist.value(job_done)
            #job_str = '%d' %(job_str1)
            job_done1 = QTableWidgetItem(str(job_str1))
            job_done1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            job_ready = rlist.record().indexOf('job_ready')
            job_ready1 = QTableWidgetItem(str(rlist.value(job_ready)))
            job_ready1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            job_run = rlist.record().indexOf('job_run')
            job_run1 = QTableWidgetItem(str(rlist.value(job_run)))
            job_run1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            job_fal = rlist.record().indexOf('job_fal')
            job_fal1 = QTableWidgetItem(str(rlist.value(job_fal)))
            job_fal1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            cnt_job = rlist.record().indexOf('cnt_job')
            cnt_job1 = QTableWidgetItem(str(rlist.value(cnt_job)))
            cnt_job1.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            print( rlist.value(job_done), rlist.value(job_ready), rlist.value(job_run), rlist.value(job_fal), rlist.value(cnt_job))
            self.tableWidget.setItem(i,0,job_done1)
            self.tableWidget.setItem(i,1, job_ready1)
            self.tableWidget.setItem(i,2, job_run1)
            self.tableWidget.setItem(i,3, job_fal1)
            self.tableWidget.setItem(i,4, cnt_job1)
            i += 1



if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = main_me()
    #win.click_refase = lambda: print("按钮已被执行")
    win .show()
    sys.exit(app.exec())


