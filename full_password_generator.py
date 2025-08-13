import sys
import re
import itertools
import random
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QFormLayout, QLineEdit, 
                            QDateEdit, QCheckBox, QPushButton, QTextEdit, QVBoxLayout, 
                            QHBoxLayout, QLabel, QGroupBox, QSpinBox, QFileDialog, 
                            QProgressDialog, QComboBox, QRadioButton, QButtonGroup,
                            QListWidget, QListWidgetItem, QSplitter, QMenu, QAction)
from PyQt5.QtCore import Qt, QDate, QSize
from PyQt5.QtGui import QColor, QFont

class PasswordGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        # 设置窗口基本属性
        self.setWindowTitle("增强版社会工程学密码生成器")
        self.setGeometry(100, 100, 1000, 700)
        
        # 主部件和布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # 创建分割器，用于左右布局
        splitter = QSplitter(Qt.Horizontal)
        
        # 左侧输入区域
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        
        # 基本信息输入区域
        input_group = QGroupBox("输入信息（均为选填）")
        input_layout = QFormLayout()
        input_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        input_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # 姓名相关
        self.first_name = QLineEdit()
        self.first_name.setPlaceholderText("请输入姓(英文)")
        self.second_name = QLineEdit()
        self.second_name.setPlaceholderText("名的第一个字(英文)")
        self.third_name = QLineEdit()
        self.third_name.setPlaceholderText("名的第二个字(如果有，英文)")
        
        name_layout = QHBoxLayout()
        name_layout.addWidget(self.first_name)
        name_layout.addWidget(self.second_name)
        name_layout.addWidget(self.third_name)
        input_layout.addRow("姓名", name_layout)
        
        # 生日相关
        self.birthday = QDateEdit()
        self.birthday.setDisplayFormat("yyyy-MM-dd")
        self.birthday.setCalendarPopup(True)
        self.birthday2 = QDateEdit()
        self.birthday2.setDisplayFormat("yyyy-MM-dd")
        self.birthday2.setCalendarPopup(True)
        
        bday_layout = QHBoxLayout()
        bday_layout.addWidget(self.birthday)
        bday_layout.addWidget(self.birthday2)
        input_layout.addRow("生日", bday_layout)
        
        # 邮箱
        self.email = QLineEdit()
        self.email.setPlaceholderText("请输入邮箱")
        input_layout.addRow("邮件", self.email)
        
        # 电话
        self.mobile = QLineEdit()
        self.mobile.setPlaceholderText("座机号(不要-号)")
        self.telephone = QLineEdit()
        self.telephone.setPlaceholderText("手机号")
        
        phone_layout = QHBoxLayout()
        phone_layout.addWidget(self.mobile)
        phone_layout.addWidget(self.telephone)
        input_layout.addRow("电话", phone_layout)
        
        # 用户名和账号
        self.username = QLineEdit()
        self.username.setPlaceholderText("用户名(英文)")
        self.account = QLineEdit()
        self.account.setPlaceholderText("用户账号")
        
        user_layout = QHBoxLayout()
        user_layout.addWidget(self.username)
        user_layout.addWidget(self.account)
        input_layout.addRow("用户名", user_layout)
        
        # 组织和公司
        self.organization = QLineEdit()
        self.organization.setPlaceholderText("组织名(英文)")
        self.company = QLineEdit()
        self.company.setPlaceholderText("公司名(英文)")
        
        org_layout = QHBoxLayout()
        org_layout.addWidget(self.organization)
        org_layout.addWidget(self.company)
        input_layout.addRow("组织", org_layout)
        
        # 常用短语
        self.like_use = QLineEdit()
        self.like_use.setPlaceholderText("常用短语(英文),多个用逗号分隔")
        input_layout.addRow("短语", self.like_use)
        
        # 身份证号和工号
        self.id_card = QLineEdit()
        self.id_card.setPlaceholderText("身份证号")
        input_layout.addRow("身份证号", self.id_card)
        
        self.work_no = QLineEdit()
        self.work_no.setPlaceholderText("工号")
        input_layout.addRow("工号", self.work_no)
        
        input_group.setLayout(input_layout)
        left_layout.addWidget(input_group)
        
        # 高级设置区域
        advanced_group = QGroupBox("高级设置")
        advanced_layout = QFormLayout()
        advanced_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        advanced_layout.setLabelAlignment(Qt.AlignRight | Qt.AlignVCenter)
        
        # 连接符设置
        self.connector = QLineEdit()
        self.connector.setText("!@#$%^&*")
        self.connector_left = QCheckBox("左")
        self.connector_middle = QCheckBox("中")
        self.connector_right = QCheckBox("右")
        
        connector_layout = QHBoxLayout()
        connector_layout.addWidget(self.connector)
        connector_layout.addWidget(self.connector_left)
        connector_layout.addWidget(self.connector_middle)
        connector_layout.addWidget(self.connector_right)
        advanced_layout.addRow("连接符", connector_layout)
        
        # 通用密码设置
        self.common = QLineEdit()
        self.common.setText("123,888,666,000,111,aaa,abc,qaz,qwe,asd,zxc,!@#,1234,1qaz")
        self.have_year = QCheckBox("包含年份")
        self.year = QSpinBox()
        self.year.setRange(1, 50)
        self.year.setValue(10)
        
        common_layout = QHBoxLayout()
        common_layout.addWidget(self.common)
        common_layout.addWidget(self.have_year)
        common_layout.addWidget(QLabel("近"))
        common_layout.addWidget(self.year)
        common_layout.addWidget(QLabel("年"))
        advanced_layout.addRow("通用密码", common_layout)
        
        # 过滤设置
        self.number_filter = QCheckBox("过滤纯数字")
        self.string_filter = QCheckBox("过滤纯字母")
        
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(self.number_filter)
        filter_layout.addWidget(self.string_filter)
        advanced_layout.addRow("过滤设置", filter_layout)
        
        # 长度设置
        self.short = QSpinBox()
        self.short.setRange(1, 32)
        self.short.setValue(6)
        self.long = QSpinBox()
        self.long.setRange(1, 32)
        self.long.setValue(16)
        
        len_layout = QHBoxLayout()
        len_layout.addWidget(QLabel("最短:"))
        len_layout.addWidget(self.short)
        len_layout.addWidget(QLabel("最长:"))
        len_layout.addWidget(self.long)
        advanced_layout.addRow("密码长度", len_layout)
        
        # 大小写设置
        self.capitalize = QCheckBox("首字母大写")
        self.capitalize.setChecked(True)
        self.lowercase = QCheckBox("全小写")
        self.uppercase = QCheckBox("全大写")
        
        case_layout = QHBoxLayout()
        case_layout.addWidget(self.capitalize)
        case_layout.addWidget(self.lowercase)
        case_layout.addWidget(self.uppercase)
        advanced_layout.addRow("大小写设置", case_layout)
        
        # 密码复杂度设置
        self.require_upper = QCheckBox("必须包含大写字母")
        self.require_lower = QCheckBox("必须包含小写字母")
        self.require_digit = QCheckBox("必须包含数字")
        self.require_special = QCheckBox("必须包含特殊字符")
        
        complexity_layout = QHBoxLayout()
        complexity_layout.addWidget(self.require_upper)
        complexity_layout.addWidget(self.require_lower)
        complexity_layout.addWidget(self.require_digit)
        complexity_layout.addWidget(self.require_special)
        advanced_layout.addRow("复杂度要求", complexity_layout)
        
        # 生成数量限制
        self.max_count = QSpinBox()
        self.max_count.setRange(100, 10000)
        self.max_count.setValue(1000)
        advanced_layout.addRow("最大生成数量", self.max_count)
        
        advanced_group.setLayout(advanced_layout)
        left_layout.addWidget(advanced_group)
        
        # 按钮区域
        btn_layout = QHBoxLayout()
        self.gen_btn = QPushButton("生成密码")
        self.gen_btn.clicked.connect(self.generate)
        self.reset_btn = QPushButton("重置")
        self.reset_btn.clicked.connect(self.reset)
        self.download_btn = QPushButton("下载结果")
        self.download_btn.clicked.connect(self.download)
        
        btn_layout.addWidget(self.gen_btn)
        btn_layout.addWidget(self.reset_btn)
        btn_layout.addWidget(self.download_btn)
        left_layout.addLayout(btn_layout)
        
        left_layout.addStretch()
        splitter.addWidget(left_panel)
        
        # 右侧结果区域
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # 结果控制区域
        result_ctrl_layout = QHBoxLayout()
        
        # 排序选项
        self.sort_option = QComboBox()
        self.sort_option.addItems(["不排序", "按长度升序", "按长度降序", "按强度升序", "按强度降序", "字母顺序"])
        self.sort_option.currentIndexChanged.connect(self.sort_passwords)
        
        # 视图切换
        self.view_mode = QButtonGroup()
        self.list_view_btn = QRadioButton("列表视图")
        self.grid_view_btn = QRadioButton("网格视图")
        self.list_view_btn.setChecked(True)
        self.view_mode.addButton(self.list_view_btn, 0)
        self.view_mode.addButton(self.grid_view_btn, 1)
        self.list_view_btn.toggled.connect(self.change_view_mode)
        
        result_ctrl_layout.addWidget(QLabel("排序:"))
        result_ctrl_layout.addWidget(self.sort_option)
        result_ctrl_layout.addSpacing(20)
        result_ctrl_layout.addWidget(self.list_view_btn)
        result_ctrl_layout.addWidget(self.grid_view_btn)
        result_ctrl_layout.addStretch()
        
        right_layout.addLayout(result_ctrl_layout)
        
        # 结果统计
        stats_layout = QHBoxLayout()
        self.first_count = QLabel("简单组合: 0")
        self.second_count = QLabel("双重组合: 0")
        self.third_count = QLabel("连接符组合: 0")
        self.total_count = QLabel("总计: 0")
        
        stats_layout.addWidget(self.first_count)
        stats_layout.addWidget(self.second_count)
        stats_layout.addWidget(self.third_count)
        stats_layout.addWidget(self.total_count)
        right_layout.addLayout(stats_layout)
        
        # 结果显示区域
        self.result_list = QListWidget()
        self.result_list.setAlternatingRowColors(True)
        self.result_list.setSelectionMode(QListWidget.ExtendedSelection)
        
        # 添加右键菜单支持
        self.result_list.setContextMenuPolicy(Qt.CustomContextMenu)
        self.result_list.customContextMenuRequested.connect(self.show_context_menu)
        
        right_layout.addWidget(self.result_list)
        
        # 结果操作按钮
        result_btn_layout = QHBoxLayout()
        self.copy_selected_btn = QPushButton("复制选中项")
        self.copy_selected_btn.clicked.connect(self.copy_selected)
        self.copy_all_btn = QPushButton("复制全部")
        self.copy_all_btn.clicked.connect(self.copy_all)
        self.clear_btn = QPushButton("清空结果")
        self.clear_btn.clicked.connect(self.clear_results)
        
        result_btn_layout.addWidget(self.copy_selected_btn)
        result_btn_layout.addWidget(self.copy_all_btn)
        result_btn_layout.addWidget(self.clear_btn)
        right_layout.addLayout(result_btn_layout)
        
        splitter.addWidget(right_panel)
        
        # 设置分割器比例
        splitter.setSizes([400, 600])
        
        main_layout.addWidget(splitter)
        
        # 初始化数据存储
        self.generated_passwords = []
        self.password_strength = {}  # 存储密码强度评分

    def show_context_menu(self, position):
        """显示右键菜单"""
        menu = QMenu()
        copy_action = QAction("复制", self)
        copy_action.triggered.connect(lambda: self.copy_selected())
        
        if self.result_list.selectedItems():
            menu.addAction(copy_action)
            menu.exec_(self.result_list.mapToGlobal(position))

    def change_view_mode(self):
        """切换视图模式"""
        if self.list_view_btn.isChecked():
            self.result_list.setViewMode(QListWidget.ListMode)
        else:
            self.result_list.setViewMode(QListWidget.IconMode)
            self.result_list.setIconSize(QSize(150, 30))
            self.result_list.setResizeMode(QListWidget.Adjust)

    def sort_passwords(self):
        """根据选择的选项排序密码"""
        if not self.generated_passwords:
            return
            
        sort_index = self.sort_option.currentIndex()
        passwords = [item.text().split(" [")[0] for item in self.result_list.findItems("", Qt.MatchContains)]
        
        # 根据不同选项排序
        if sort_index == 1:  # 按长度升序
            passwords.sort(key=lambda x: len(x))
        elif sort_index == 2:  # 按长度降序
            passwords.sort(key=lambda x: len(x), reverse=True)
        elif sort_index == 3:  # 按强度升序
            passwords.sort(key=lambda x: self.password_strength.get(x, 0))
        elif sort_index == 4:  # 按强度降序
            passwords.sort(key=lambda x: self.password_strength.get(x, 0), reverse=True)
        elif sort_index == 5:  # 字母顺序
            passwords.sort()
            
        # 重新显示排序后的密码
        self.result_list.clear()
        for pwd in passwords:
            self.add_password_item(pwd)

    def add_password_item(self, password):
        """添加密码项到列表，包含强度指示"""
        strength = self.calculate_strength(password)
        self.password_strength[password] = strength
        
        # 根据强度设置不同颜色
        color = QColor(255, 0, 0)  # 红色 - 弱
        strength_text = "弱"
        
        if strength >= 60:
            color = QColor(0, 128, 0)  # 绿色 - 强
            strength_text = "强"
        elif strength >= 30:
            color = QColor(255, 165, 0)  # 橙色 - 中
            strength_text = "中"
            
        item_text = f"{password} [{strength_text}]"
        item = QListWidgetItem(item_text)
        item.setForeground(color)
        self.result_list.addItem(item)

    def calculate_strength(self, password):
        """计算密码强度评分(0-100)"""
        strength = 0
        length = len(password)
        
        # 长度评分
        if length >= 12:
            strength += 25
        elif length >= 8:
            strength += 15
        elif length >= 6:
            strength += 5
            
        # 包含小写字母
        if re.search(r'[a-z]', password):
            strength += 15
            
        # 包含大写字母
        if re.search(r'[A-Z]', password):
            strength += 15
            
        # 包含数字
        if re.search(r'[0-9]', password):
            strength += 15
            
        # 包含特殊字符
        if re.search(r'[^a-zA-Z0-9]', password):
            strength += 20
            
        # 字符多样性
        char_types = 0
        if re.search(r'[a-z]', password): char_types += 1
        if re.search(r'[A-Z]', password): char_types += 1
        if re.search(r'[0-9]', password): char_types += 1
        if re.search(r'[^a-zA-Z0-9]', password): char_types += 1
        
        strength += (char_types - 1) * 5
        
        return min(strength, 100)

    def check_complexity(self, password):
        """检查密码是否符合复杂度要求"""
        if self.require_upper.isChecked() and not re.search(r'[A-Z]', password):
            return False
        if self.require_lower.isChecked() and not re.search(r'[a-z]', password):
            return False
        if self.require_digit.isChecked() and not re.search(r'[0-9]', password):
            return False
        if self.require_special.isChecked() and not re.search(r'[^a-zA-Z0-9]', password):
            return False
        return True

    def reset(self):
        """重置所有输入框和结果"""
        self.first_name.clear()
        self.second_name.clear()
        self.third_name.clear()
        self.birthday.setDate(QDate())
        self.birthday2.setDate(QDate())
        self.email.clear()
        self.mobile.clear()
        self.telephone.clear()
        self.username.clear()
        self.account.clear()
        self.organization.clear()
        self.company.clear()
        self.like_use.clear()
        self.id_card.clear()
        self.work_no.clear()
        self.connector.setText("!@#$%^&*")
        self.connector_left.setChecked(False)
        self.connector_middle.setChecked(False)
        self.connector_right.setChecked(False)
        self.common.setText("123,888,666,000,111,aaa,abc,qaz,qwe,asd,zxc,!@#,1234,1qaz")
        self.have_year.setChecked(False)
        self.year.setValue(10)
        self.number_filter.setChecked(False)
        self.string_filter.setChecked(False)
        self.short.setValue(6)
        self.long.setValue(16)
        self.capitalize.setChecked(True)
        self.lowercase.setChecked(False)
        self.uppercase.setChecked(False)
        self.require_upper.setChecked(False)
        self.require_lower.setChecked(False)
        self.require_digit.setChecked(False)
        self.require_special.setChecked(False)
        self.max_count.setValue(1000)
        self.clear_results()
        self.sort_option.setCurrentIndex(0)
        self.generated_passwords = []
        self.password_strength = {}

    def clear_results(self):
        """清空结果列表"""
        self.result_list.clear()
        self.first_count.setText("简单组合: 0")
        self.second_count.setText("双重组合: 0")
        self.third_count.setText("连接符组合: 0")
        self.total_count.setText("总计: 0")

    def copy_selected(self):
        """复制选中的密码"""
        selected = self.result_list.selectedItems()
        if not selected:
            return
            
        text = "\n".join([item.text().split(" [")[0] for item in selected])
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def copy_all(self):
        """复制所有密码"""
        all_items = [self.result_list.item(i).text().split(" [")[0] for i in range(self.result_list.count())]
        text = "\n".join(all_items)
        clipboard = QApplication.clipboard()
        clipboard.setText(text)

    def get_upper(self, lst):
        """将列表中的字符串转为大写，包含原文，去空"""
        upper_pattern = re.compile(".*[a-z].*")
        return list(filter(None, lst + [s.upper() if upper_pattern.match(s) else '' for s in lst]))

    def get_lower(self, lst):
        """将列表中的字符串转为小写，包含原文，去空"""
        lower_pattern = re.compile(".*[A-Z].*")
        return list(filter(None, lst + [s.lower() if lower_pattern.match(s) else '' for s in lst]))

    def get_capitalize(self, lst):
        """首字母大写，包含原文，去空"""
        capitalize_pattern = re.compile("^[a-z].*")
        return list(filter(None, lst + [s.capitalize() if capitalize_pattern.match(s) else '' for s in lst]))

    def get_distinct_list(self, lst):
        """去重去空后的列表"""
        return list(filter(None, list(set(lst))))

    def get_repeat(self, lst, x=3):
        """小于等于x位自动重复，返回原文及重复后的列表组合，去空"""
        return list(filter(None, lst + [s * 2 if 0 < len(s) <= x else '' for s in lst]))

    def get_head_tail(self, s, *lengths):
        """取字符串前几位及后几位，包含原文，去空"""
        result = [s] if s else []
        for l in lengths:
            if len(s) > l:
                result.append(s[:l])
                result.append(s[-l:])
        return list(filter(None, result))

    def drop_short_long(self, lst, start=6, end=16):
        """列表去掉过长和过短的元素"""
        return [s for s in lst if (start <= len(s) <= end)]

    def drop_string_int(self, lst, rtype):
        """去掉纯字母或纯数字"""
        if rtype not in ['str', 'int']:
            return lst
        pattern = re.compile(r'^[a-zA-Z]*$') if rtype == 'str' else re.compile(r'^[0-9]*$')
        return [s for s in lst if not pattern.match(s)]

    def generate(self):
        """生成密码列表的主函数"""
        # 显示进度对话框
        progress = QProgressDialog("正在生成密码...", "取消", 0, 100, self)
        progress.setWindowTitle("处理中")
        progress.setWindowModality(Qt.WindowModal)
        progress.setValue(10)
        
        # 获取输入值
        first_name = self.first_name.text().strip()
        second_name = self.second_name.text().strip()
        third_name = self.third_name.text().strip()
        
        birthday = self.birthday.date().toString("yyyy-MM-dd") if self.birthday.date().isValid() else ""
        birthday2 = self.birthday2.date().toString("yyyy-MM-dd") if self.birthday2.date().isValid() else ""
        
        email = self.email.text().strip()
        mobile = self.mobile.text().strip()
        telephone = self.telephone.text().strip()
        username = self.username.text().strip()
        account = self.account.text().strip()
        organization = self.organization.text().strip()
        company = self.company.text().strip()
        like_use = self.like_use.text().strip()
        id_card = self.id_card.text().strip()
        work_no = self.work_no.text().strip()
        
        connector = list(self.connector.text().strip())
        connector_left = self.connector_left.isChecked()
        connector_middle = self.connector_middle.isChecked()
        connector_right = self.connector_right.isChecked()
        
        common = self.common.text().strip()
        have_year = self.have_year.isChecked()
        year = self.year.value()
        number_filter = self.number_filter.isChecked()
        string_filter = self.string_filter.isChecked()
        short_len = self.short.value()
        long_len = self.long.value()
        capitalize = self.capitalize.isChecked()
        lowercase = self.lowercase.isChecked()
        uppercase = self.uppercase.isChecked()
        max_count = self.max_count.value()
        
        progress.setValue(20)

        # 处理姓名相关
        first_name_combine = self.get_repeat([first_name], 3) if re.match(r'^[a-zA-Z0-9]+$', first_name) else ['']
        last_name_combined = second_name + third_name
        last_name_combine = self.get_repeat([last_name_combined], 3) if re.match(r'^[a-zA-Z0-9]+$', last_name_combined) else ['']
        
        name_all = [first_name_combine[0] + last_name_combine[0], last_name_combine[0] + first_name_combine[0]]
        last_name_ab = second_name[:1] + third_name[:1]
        name_all.extend([
            first_name[:1] + last_name_ab,
            first_name_combine[0] + last_name_ab,
            last_name_ab + first_name[:1],
            last_name_ab + first_name_combine[0],
            first_name[:1] + second_name + third_name,
            second_name + third_name,
            first_name
        ])
        
        name_all.extend(self.get_repeat(self.get_head_tail(username, 3, 4)))
        name_all.extend(self.get_repeat(self.get_head_tail(account, 3, 4)))
        name_all = self.get_distinct_list(name_all)
        
        progress.setValue(30)

        # 处理生日相关
        birthday_all = []
        b = birthday.replace('-', '') if birthday else ''
        b2 = birthday2.replace('-', '') if birthday2 else ''
        
        birthday_all.extend(self.get_head_tail(b, 4))
        birthday_all.extend(self.get_head_tail(b2, 4))
        
        if len(b) >= 8 and b[4] == '0':
            birthday_all.extend([b[5:8], b[5:8] * 2])
        if len(b2) >= 8 and b2[4] == '0':
            birthday_all.extend([b2[5:8], b2[5:8] * 2])
            
        birthday_all = self.get_distinct_list(birthday_all)
        
        progress.setValue(40)

        # 处理邮箱相关
        email_local = email.split('@')[0] if email else ''
        email_all = self.get_distinct_list([email] + self.get_repeat(self.get_head_tail(email_local, 3, 4), 3))
        
        # 处理电话相关
        phone_all = self.get_distinct_list(
            self.get_repeat(self.get_head_tail(mobile, 3, 4, 5, 6)) + 
            self.get_repeat(self.get_head_tail(telephone, 3, 4, 5, 6))
        )
        
        progress.setValue(50)

        # 处理身份证号
        id_card_all = []
        if id_card:
            id_parts = self.get_head_tail(id_card, 3, 4, 6, 8)
            if len(id_card) > 1:
                id_parts.extend(self.get_head_tail(id_card[:-1], 3, 4, 6, 8)[1:])  # 排除原字符串
            id_card_all = self.get_distinct_list(id_parts)
        
        # 处理工号
        work_no_all = self.get_distinct_list(self.get_repeat(self.get_head_tail(work_no, 3, 4, 6, 8)))
        
        # 处理组织和公司
        org_parts = self.get_repeat(self.get_head_tail(organization, 3, 4)) if organization else []
        company_parts = self.get_repeat(self.get_head_tail(company, 3, 4)) if company else []
        org_all = self.get_distinct_list(org_parts + company_parts)
        
        progress.setValue(60)

        # 处理常用短语
        like_all = []
        if like_use:
            for item in like_use.split(','):
                like_all.extend(self.get_repeat(self.get_head_tail(item.strip(), 3, 4)))
        like_all = self.get_distinct_list(like_all)
        
        # 处理通用密码和年份
        common_all = common.split(',') if common else []
        if have_year:
            current_year = QDate.currentDate().year()
            for y in range(current_year - year, current_year + 1):
                common_all.append(str(y))
        common_all = self.get_distinct_list(common_all)
        
        progress.setValue(70)

        # 组合所有列表
        pass_list_all = [name_all, birthday_all, email_all, phone_all, 
                        id_card_all, work_no_all, org_all, like_all, common_all]
        
        # 简单组合
        pass_first = []
        for lst in pass_list_all:
            pass_first.extend(lst)
        pass_first = self.get_distinct_list(pass_first)
        
        # 双重组合
        pass_second = []
        # 生成所有可能的两个列表的组合
        for a, b in itertools.permutations(pass_list_all, 2):
            # 计算笛卡尔积
            for x, y in itertools.product(a, b):
                pass_second.append(x + y)
        pass_second = self.get_distinct_list(pass_second)
        
        progress.setValue(80)

        # 带连接符的组合
        pass_third = []
        for a, b in itertools.permutations(pass_list_all, 2):
            for x, y in itertools.product(a, b):
                for c in connector:
                    if connector_left:
                        pass_third.append(c + x + y)
                    if connector_middle:
                        pass_third.append(x + c + y)
                    if connector_right:
                        pass_third.append(x + y + c)
        pass_third = self.get_distinct_list(pass_third)
        
        # 应用长度过滤
        pass_lists = [pass_first, pass_second, pass_third]
        pass_lists = [self.drop_short_long(lst, short_len, long_len) for lst in pass_lists]
        
        # 应用内容过滤
        if number_filter:
            pass_lists = [self.drop_string_int(lst, 'int') for lst in pass_lists]
        if string_filter:
            pass_lists = [self.drop_string_int(lst, 'str') for lst in pass_lists]
        
        # 应用复杂度过滤
        pass_lists = [[pwd for pwd in lst if self.check_complexity(pwd)] for lst in pass_lists]
        
        # 应用大小写转换
        if capitalize:
            pass_lists = [self.get_capitalize(lst) for lst in pass_lists]
        if lowercase:
            pass_lists = [self.get_lower(lst) for lst in pass_lists]
        if uppercase:
            pass_lists = [self.get_upper(lst) for lst in pass_lists]
        
        # 最终去重
        pass_lists = [self.get_distinct_list(lst) for lst in pass_lists]
        
        # 应用最大数量限制
        total_passwords = []
        for lst in pass_lists:
            total_passwords.extend(lst)
        
        # 如果超过最大数量，随机抽样
        if len(total_passwords) > max_count:
            total_passwords = random.sample(total_passwords, max_count)
            # 重新分配到三个列表中，保持比例
            ratio1 = len(pass_lists[0]) / len(total_passwords) if len(total_passwords) > 0 else 0
            ratio2 = len(pass_lists[1]) / len(total_passwords) if len(total_passwords) > 0 else 0
            
            count1 = int(max_count * ratio1)
            count2 = int(max_count * ratio2)
            count3 = max_count - count1 - count2
            
            pass_lists[0] = random.sample(pass_lists[0], min(count1, len(pass_lists[0]))) if pass_lists[0] else []
            pass_lists[1] = random.sample(pass_lists[1], min(count2, len(pass_lists[1]))) if pass_lists[1] else []
            pass_lists[2] = random.sample(pass_lists[2], min(count3, len(pass_lists[2]))) if pass_lists[2] else []
        
        progress.setValue(90)

        # 保存结果
        self.generated_passwords = pass_lists
        self.password_strength = {}  # 重置强度字典
        
        # 显示结果
        self.result_list.clear()
        all_passwords = []
        for lst in pass_lists:
            all_passwords.extend(lst)
        
        # 添加到列表并显示
        for pwd in all_passwords:
            self.add_password_item(pwd)
        
        # 更新统计信息
        self.first_count.setText(f"简单组合: {len(pass_lists[0])}")
        self.second_count.setText(f"双重组合: {len(pass_lists[1])}")
        self.third_count.setText(f"连接符组合: {len(pass_lists[2])}")
        self.total_count.setText(f"总计: {len(all_passwords)}")
        
        progress.setValue(100)

    def download(self):
        """下载生成的密码列表"""
        if not self.generated_passwords:
            return
            
        all_passwords = []
        for lst in self.generated_passwords:
            all_passwords.extend(lst)
            
        if not all_passwords:
            return
            
        filename, _ = QFileDialog.getSaveFileName(self, "保存密码列表", "passwords.txt", "文本文件 (*.txt)")
        if filename:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write('\n'.join(all_passwords))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 确保中文显示正常
    font = QFont("SimHei")
    app.setFont(font)
    window = PasswordGenerator()
    window.show()
    sys.exit(app.exec_())
    