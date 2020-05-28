from time import time

from Server.spcapi.spcapi.model.dbcommon import dbcommon


class spcSource(dbcommon):
    def __init__(self):
        self.mdb = dbcommon()

    def saveOri(self, data):
        SQL = "INSERT INTO `spc_source` (`device_no`, `size_type`, `change_val`, `control_up`, `control_center`,`control_down`,`r_control_up`,`r_control_down`,`r_control_center`, `timestamp`)" \
              " VALUES (NULL, '{device_no}', '{size_type}', '{change_val}', '{control_up}', '{control_center}', '{control_down}', '{timestamp}');" \
            .format(device_no=data["device_no"], size_type=data["size_type"], change_val=data["change_val"],
                    control_center=data["control_center"], control_up=data["control_up"],
                    control_down=data["control_down"],
                    r_control_up=data["r_control_up"], r_control_down=data["r_control_down"],
                    r_control_center=data["r_control_center"], timestamp=data["timestamp"])
        self.mdb.execute(SQL)

    def saveUpd(self, data):
        SQL = "UPDATE  `spc_source` SET `process_person`='{process_person}',`process_procedure`='{process_procedure}',`process_time`='{process_time}'" \
              " WHERE `device_no`='{device_no}' and `timestamp`='{timestamp}';" \
            .format(process_person=data["process_person"], process_procedure=data["process_procedure"],
                    process_time=data["process_time"], device_no=data["device_no"], timestamp=data["timestamp"])
        self.mdb.execute(SQL)

    def getList(self, no):
        SQL = "SELECT * FROM spc_source where device_no = {no}".format(no=no)
        return self.mdb.readQuery(SQL)

    def getDeviceNo(self):
        SQL = "SELECT distinct device_no FROM spc_source"
        return self.mdb.readQuery(SQL)

    def getCount(self):
        SQL = "SELECT COUNT(*) FROM spc_source"
        return self.mdb.readQuery(SQL)

    def getUpAndDown(self, device_no, size_type):
        SQL = "SELECT control_up,control_center,control_down,r_contro_up,r_contro_down,r_contro_center FROM spc_source where device_no='{device_no}' " \
              "and size_type = '{size_type}' and timestamp = (select MAX(timestamp) from spc_source)".format(
            device_no=device_no, size_type=size_type)
        return self.mdb.readQuery(SQL)

    def getNameAndMethod(self, device_no, size_type):
        SQL = "SELECT process_person,process_procedure FROM spc_source where device_no='{device_no}' " \
              "and size_type = '{size_type}'".format(
            device_no=device_no,size_type=size_type)
        return self.mdb.readQuery(SQL)
