# -*- coding: utf-8 -*-
# Handle openstack db keystone user, project with
# iaasui database project_user, project_project consistent

from ConfigParser import ConfigParser

import logging
import MySQLdb
import pprint
import time


_DB_MAP = {
    "openstack_keystone":{
       "user_sql": "select id, name, password from user",
       "project_sql": "select id, name, description from project"
       },
    "DEFAULT": {
       "user_sql": '''select id, userName, userPassword, roles,
                   email, tel, createTime from project_user''',
       "project_sql": '''select id, projectName, projectType, projectLeader,
                         projectManager, projectStatus, createTime, 
                         projectDescription from project_project'''}
}

class OpenStackDBError(Exception):
    pass

class GetDBInfo(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        """Generate a instance
        """
        if not cls._instance:
            cls._instance =object.__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, cpfile="db.conf"):
        self.cp_obj = ConfigParser()
        self.cp_obj.read(cpfile)
        
    def get(self, section, key):
        return self.cp_obj.get(section, key)

class MySQLBase(object):
    """MySQLBase 
    """

    def __init__(self, section):
        # logging set 
        logging.getLogger(__name__)
        logging.basicConfig(
        format= ("%(asctime)s: [%(levelname)s]: %(filename)s:"
                "%(lineno)s: %(message)s"),
        level= logging.INFO,
        filename = "openstack_db_op.log",
        filemode = "wb",
        )

        logging.info("MySQLBase start-------") 
        print "start-----"
        # database information
        self.db_obj = GetDBInfo()
        host, user, mpass, port, db = (self.db_obj.get(section, 'db_host'),
                                      self.db_obj.get(section, 'db_username'),
				      self.db_obj.get(section, 'db_password'),
				    int(self.db_obj.get(section, 'db_port')),
				      self.db_obj.get(section, 'db_dbname'))
        try:
            self.conn = MySQLdb.connect(host=host,user=user,
                                        passwd=mpass,port=port,
                                        db=db, charset="utf8")
            self.cursor = self.conn.cursor(cursorclass=MySQLdb.cursors.DictCursor)
        except MySQLdb.MySQLError as e:
            logging.error( str(e) )
            raise OpenStackDBError( str(e) )

    def get_result(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            self.conn.commit()
        except MySQLdb.MySQLError as err:
            logging.error( str(err) )
            raise OpenStackDBError( str(err) )
        else:
            return result

    def get_user_list(self):
        pass

    def get_project_list(self):
        pass

    def get_current_strtime(self):
        """Strftime 2015-03-11 09:55
        """
        return time.strftime("%Y-%m-%d %H:%M", time.localtime(time.time()))

    def __del__(self):
        try:
            self.cursor.close()
            self.conn.close()
        except:
            pass

class MySQLOper(MySQLBase):
    """MySQLdb operation
    """
    def __init__(self, section="openstack_keystone"):
        self.section = section
        super(MySQLOper, self).__init__(section)
    
    def get_user_list(self):
        """Get User list.
        -----
        """
        user_list = _DB_MAP[self.section]['user_sql'] 
        return self.get_result(user_list)

    def get_project_list(self):
        """Get project list.
        Project list
        """
        project_list = _DB_MAP[self.section]['project_sql'] 
        return self.get_result(project_list)

    def user_own_project_list(self):
        """user own project list.
        keystone db 
        User---project list
        """

        account_suffix = self.db_obj.get('user_info', 'email_default_suffix')
        if self.section == "DEFAULT":
            return False

        user_own_list =list()
        for row in self.get_user_list():
            # print "\t\t", "name:", row['name']
            if not account_suffix in row['name']:
                logging.info("format error user: %s" %(row['name']))
                continue

            user_proj_list = """select  distinct(target_id) from 
                             assignment where actor_id = '%s'""" % (row['id'])
            # logging.info(user_proj_list)

            # user own project_list
            project_list = []
            user_id_list = list()

            for project_id in self.get_result(user_proj_list):
                pid = project_id['target_id']
                user_own_project_name = """ select id, name from project
                                      where id = '%s'""" % (pid)
                project_list.append(self.get_result(user_own_project_name)[0])
            # print "\t\t", "name:", row['name']
            user_id_list.append(row['id'])
            user_own_list.append({'user': {'username': row['name'],
                                  'project': project_list,
                                  'uid': user_id_list}})
        return user_own_list

    # iaasui db operation

    def insert_project(self, pname=None, pdesc=None):
        """Insert project to iaasui.project_user.

        :param pname: project name.
        :param pdesc: project description.
        :rtype True 
        """
        if self.section == "openstack_keystone":
            logging.error("insert_project -- section error:")
            return False

        # validate project exists or not, if exist return else insert
        project_exist_sql = '''select projectName from project_project where 
                         projectName='%s' ''' % ( pname )
        if self.get_result(project_exist_sql):
            logging.warning("project: exists: %s" % pname)
            return False 

        pname, ptype, pleader, pmanager, pdesc = (pname, '', '',
                                                  '', pdesc)

        in_pro_sql = '''insert into project_project (projectName, projectType,
                     projectLeader, projectManager, projectStatus, createTime, 
                     projectDescription) values ('%s', '%s', '%s', '%s', '%s', 
                     '%s', '%s')'''%(pname, ptype, pleader, pmanager, 'yes',
                           self.get_current_strtime(), pdesc)
        self.get_result(in_pro_sql)
        return True

    def insert_user(self, user='cui_mw_test'):
        """Insert user to iaasui.project_user.

        :param user: username.
        :rtype: True/False. 
        """
        userpass = self.db_obj.get('user_info', 'user_default_pass')

        if self.section == "openstack_keystone":
            logging.error("insert_project -- section error:")
            return  False

        # Validate user exists or not, if exist return else insert.
        user_exist_sql = '''select userName from project_user where 
                         userName='%s' ''' % ( user )
        if self.get_result(user_exist_sql):
            logging.warning("user: exists: %s" % user)
            return False 

        for role in ['admin', '_member_']:
            uuser, upass, uroles, uctime = (user, userpass,
                       role, self.get_current_strtime())
    
            in_pro_sql = '''insert into project_user (userName, userPassword,
                         roles, email, tel, createTime) values (
                         '%s', '%s', '%s', '%s', '%s', '%s')''' % (
                           uuser, upass, uroles, uuser, '', uctime)
            # print in_pro_sql
            rlt = self.get_result(in_pro_sql)
        return True 

    def insert_user_project_relation(self, uid, pid):
        """Insert project_user_user relation.
        :param uid: user id.
        :param pid: project id.
        :rtype True.
        """
        if self.section == "openstack_keystone":
            logging.warning("insert_user_project_rela error: section error")
            return

        # check uid, project id exists or not
        u_p_sql = ''' select user_id from project_user_user where user_id=
                      %d and project_id=%d ''' % (uid, pid)
        if self.get_result(u_p_sql):
            logging.warning("insert_user_project_relation error: uid, %s
                            pid, %s exists") % (uid, pid)
            return False

        # off foreign_key_check
        self.get_result('set foreign_key_checks=off')
        i_user_pro_sql = ''' insert into project_user_user(user_id,
                         project_id) values (%d, %d)''' % (uid, pid)
        self.get_result(i_user_pro_sql)
        # insert over ,  on the foreign key check
        self.get_result('set foreign_key_checks=ON')
        return True

if __name__ == "__main__":
    # 1. keystone  user list 
    key_obj = MySQLOper()
    key_user_list = key_obj.get_user_list()
    pprint.pprint( key_user_list )

    # 2. keystone project list
    key_project_list = key_obj.get_project_list()
    pprint.pprint( key_project_list )

    # 3. keystone user own project list
    user_own_project_list = key_obj.user_own_project_list()
    pprint.pprint( user_own_project_list )

    # 4. insert iaasui project_user
    ui_obj = MySQLOper('DEFAULT')
    for user in key_user_list:
        # print user
        ui_obj.insert_user(user)

    # 5. insert iaasui project_project
    for project in key_project_list:
        print 'pname: %s, pdesc: %s' % (project['name'],
                                        project['description']) 
        ui_obj.insert_project(project['name'], project['description'])

    # 6. insert iaasui project_user_user for user_project relation
    for user_project in user_own_project_list:
        # pprint.pprint( user_project )
        print "user: %s, project: %s" % (user_project['user']['username'],
                                         user_project['user']['project'])
        user_project_map = dict()
        user_id_sql = '''select id from project_user where userName='%s' '''%(
			user_project['user']['username'])
        uid_list = ui_obj.get_result(user_id_sql)

        # project id list 
        for pname in user_project['user']['project']:
            project_id_sql=''' select id from project_project where
                         projectName = '%s' ''' % ( pname['name'])
            pid_list = ui_obj.get_result(project_id_sql)

            # print uid_list, pid_list
            # insert iaasui project_user_user( the last result)
            for uid in uid_list:
                for pid in pid_list:
                    print uid, pid
                    logging.info("uid: %s, pid: %s") % (uid, pid)
                    ui_obj.insert_user_project_relation(uid, pid)

    print '^_^ ' * 30
    print "########## database dump  succeed, please check !!!"
