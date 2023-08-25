from ui.base_element import BaseLabel, BaseLineEdit
from PyQt5 import QtGui
from PyQt5.QtWidgets import QDialog, QGridLayout, QMessageBox, QDialogButtonBox
from utils.tools import load_file, dump_file, str_2_int
from constant import QSS_STYLE
from loguru import logger


class BaseSetting:

    def __init__(self, obj_ui):
        self.obj_ui = obj_ui

    def load_frame(self):
        dialog = None
        try:

            def __body_change():
                button.setEnabled(True)

            dialog = QDialog(self.obj_ui)
            dialog.setWindowTitle('修改基础配置')
            dialog.resize(400, 200)
            dialog.setStyleSheet("background-color: white;")

            dit_conf = load_file('config.json')
            grid = QGridLayout()
            grid.setSpacing(2)

            s3_id_label = BaseLabel(dialog, str_text='阿里云S3_ID').label
            grid.addWidget(s3_id_label, 1, 0)
            s3_id_line = BaseLineEdit(dialog, str_default=dit_conf.get('AccessKey_ID', ''),
                                      file_style=QSS_STYLE).lineedit
            s3_id_line.textChanged.connect(__body_change)
            grid.addWidget(s3_id_line, 1, 1, 1, 3)

            s3_key_label = BaseLabel(dialog, str_text='阿里云S3_key').label
            grid.addWidget(s3_key_label, 2, 0)
            s3_key_line = BaseLineEdit(dialog, str_default=dit_conf.get('AccessKey_Secret', ''),
                                       file_style=QSS_STYLE).lineedit
            s3_key_line.textChanged.connect(__body_change)
            grid.addWidget(s3_key_line, 2, 1, 1, 3)

            s3_bucket_label = BaseLabel(dialog, str_text='阿里云S3_桶').label
            grid.addWidget(s3_bucket_label, 3, 0)
            s3_bucket_line = BaseLineEdit(dialog, str_default=dit_conf.get('bucket', ''),
                                          file_style=QSS_STYLE).lineedit
            s3_bucket_line.textChanged.connect(__body_change)
            grid.addWidget(s3_bucket_line, 3, 1, 1, 1)

            s3_url_label = BaseLabel(dialog, str_text='阿里云S3_地址').label
            grid.addWidget(s3_url_label, 4, 0)
            s3_url_line = BaseLineEdit(dialog, str_default=dit_conf.get('url', ''), file_style=QSS_STYLE).lineedit
            s3_url_line.textChanged.connect(__body_change)
            grid.addWidget(s3_url_line, 4, 1, 1, 3)

            db_name_label = BaseLabel(dialog, str_text='数据库名称').label
            grid.addWidget(db_name_label, 5, 0)
            db_name_line = BaseLineEdit(dialog, str_default=dit_conf.get('database', ''), file_style=QSS_STYLE).lineedit
            db_name_line.textChanged.connect(__body_change)
            grid.addWidget(db_name_line, 5, 1, 1, 3)

            db_ip_label = BaseLabel(dialog, str_text='数据库IP').label
            grid.addWidget(db_ip_label, 6, 0)
            db_ip_line = BaseLineEdit(dialog, str_default=dit_conf.get('ip', ''), file_style=QSS_STYLE).lineedit
            db_ip_line.textChanged.connect(__body_change)
            grid.addWidget(db_ip_line, 6, 1, 1, 3)

            db_port_label = BaseLabel(dialog, str_text='数据库端口').label
            grid.addWidget(db_port_label, 7, 0)
            db_port_line = BaseLineEdit(dialog, str_default=str(dit_conf.get('port', '3306')), file_style=QSS_STYLE).lineedit
            db_port_line.textChanged.connect(__body_change)
            db_port_line.setValidator(QtGui.QIntValidator())
            grid.addWidget(db_port_line, 7, 1, 1, 3)

            db_user_label = BaseLabel(dialog, str_text='数据库用户').label
            grid.addWidget(db_user_label, 8, 0)
            db_user_line = BaseLineEdit(dialog, str_default=dit_conf.get('user', ''), file_style=QSS_STYLE).lineedit
            db_user_line.textChanged.connect(__body_change)
            grid.addWidget(db_user_line, 8, 1, 1, 3)

            db_pwd_label = BaseLabel(dialog, str_text='数据库密码').label
            grid.addWidget(db_pwd_label, 9, 0)
            db_pwd_line = BaseLineEdit(dialog, str_default=dit_conf.get('pwd', ''), file_style=QSS_STYLE).lineedit
            db_pwd_line.textChanged.connect(__body_change)
            grid.addWidget(db_pwd_line, 9, 1, 1, 3)

            button = QDialogButtonBox(QDialogButtonBox.Ok)
            button.clicked.connect(dialog.accept)
            button.setDisabled(True)
            grid.addWidget(button, 11, 3)

            dialog.setLayout(grid)

            if dialog.exec() == QDialog.Accepted:
                str_id = s3_id_line.text().strip()
                str_key = s3_key_line.text().strip()
                str_bucket = s3_bucket_line.text().strip()
                str_url = s3_url_line.text().strip()
                str_ip = db_ip_line.text().strip()
                str_port = str_2_int(db_port_line.text().strip(), 3306)
                str_db = db_name_line.text().strip()
                str_user = db_user_line.text().strip()
                str_pwd = db_pwd_line.text().strip()

                if all([str_id, str_key, str_bucket, str_url, str_ip, str_db, str_user, str_pwd, str_port]):
                    dit_conf.update({
                        'AccessKey_ID': str_id, 'AccessKey_Secret': str_key,
                        'bucket': str_bucket, 'url': str_url, 'ip': str_ip, 'database': str_db,
                        'pwd': str_pwd, 'user': str_user, 'port': str_port
                    })
                    if dump_file(dit_conf, 'config.json') == 1:
                        QMessageBox.warning(dialog, '成功', '配置更新成功！', QMessageBox.Ok)
                    else:
                        QMessageBox.warning(dialog, '失败', '配置更新失败！', QMessageBox.Ok)
                else:
                    QMessageBox.warning(dialog, '错误', '不能有空数据！', QMessageBox.Ok)
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")
        finally:
            if dialog:
                dialog.close()
