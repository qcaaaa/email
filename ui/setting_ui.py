from ui.base_ui import BaseLabel, BaseLineEdit, BaseButton
from PyQt5.QtWidgets import QDialog, QGridLayout, QMessageBox, QDialogButtonBox
from utils.tools import load_file, dump_file
from constant import QSS_STYLE
from loguru import logger


class BaseSetting:

    def __init__(self, obj_ui):
        self.dialog = QDialog(obj_ui)
        self.dialog.setWindowTitle('修改基础配置')
        self.dialog.resize(400, 200)
        self.dialog.setStyleSheet("background-color: white;")

    def load_frame(self):
        try:

            def __body_change():
                button.setEnabled(True)

            dit_conf = load_file('config.json')
            grid = QGridLayout()
            grid.setSpacing(2)

            s3_id_label = BaseLabel(self.dialog, str_text='阿里云S3_ID').label
            grid.addWidget(s3_id_label, 1, 0)
            s3_id_line = BaseLineEdit(self.dialog, str_default=dit_conf.get('AccessKey_ID', ''),
                                      file_style=QSS_STYLE).lineedit
            s3_id_line.textChanged.connect(__body_change)
            grid.addWidget(s3_id_line, 1, 1, 1, 3)

            s3_key_label = BaseLabel(self.dialog, str_text='阿里云S3_key').label
            grid.addWidget(s3_key_label, 2, 0)
            s3_key_line = BaseLineEdit(self.dialog, str_default=dit_conf.get('AccessKey_Secret', ''),
                                       file_style=QSS_STYLE).lineedit
            s3_key_line.textChanged.connect(__body_change)
            grid.addWidget(s3_key_line, 2, 1, 1, 3)

            s3_bucket_label = BaseLabel(self.dialog, str_text='阿里云S3_桶').label
            grid.addWidget(s3_bucket_label, 3, 0)
            s3_bucket_line = BaseLineEdit(self.dialog, str_default=dit_conf.get('bucket', ''),
                                          file_style=QSS_STYLE).lineedit
            s3_bucket_line.textChanged.connect(__body_change)
            grid.addWidget(s3_bucket_line, 3, 1, 1, 1)

            s3_url_label = BaseLabel(self.dialog, str_text='阿里云S3_地址').label
            grid.addWidget(s3_url_label, 4, 0)
            s3_url_line = BaseLineEdit(self.dialog, str_default=dit_conf.get('url', ''), file_style=QSS_STYLE).lineedit
            s3_url_line.textChanged.connect(__body_change)
            grid.addWidget(s3_url_line, 4, 1, 1, 3)

            button = QDialogButtonBox(QDialogButtonBox.Ok)
            button.clicked.connect(self.dialog.accept)
            button.setDisabled(True)
            grid.addWidget(button, 6, 3)

            self.dialog.setLayout(grid)

            if self.dialog.exec() == QDialog.Accepted:
                str_id = s3_id_line.text()
                str_key = s3_key_line.text()
                str_bucket = s3_bucket_line.text()
                str_url = s3_url_line.text()

                if all([str_id, str_key, str_bucket, str_url]):
                    if dump_file({'AccessKey_ID': str_id, 'AccessKey_Secret': str_key,
                                  'bucket': str_bucket, 'url': str_url}, 'config.json') == 1:
                        QMessageBox.warning(self.dialog, '成功', '配置更新成功！', QMessageBox.Yes)
                    else:
                        QMessageBox.warning(self.dialog, '失败', '配置更新失败！', QMessageBox.Yes)
                else:
                    QMessageBox.warning(self.dialog, '错误', '不能有空数据！', QMessageBox.Yes)
        except Exception as err:
            logger.error(f"{err.__traceback__.tb_lineno}:--:{err}")
        finally:
            self.dialog.close()
