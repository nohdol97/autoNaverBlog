import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox
import blog
import expiration

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoBlog copyright © Gmail : nohdol97")
        self.setGeometry(100, 100, 400, 200)

        # 아이디와 비밀번호 입력
        self.id_label = QLabel("아이디:")
        self.id_input = QLineEdit()

        self.pw_label = QLabel("비밀번호:")
        self.pw_input = QLineEdit()
        self.pw_input.setEchoMode(QLineEdit.Password)

        # 최대 공감 동작
        self.max_label = QLabel("동작시 최대 공감수(숫자 입력):")
        self.max_input = QLineEdit()

        # 시간대 체크 및 확인
        self.checked_list = []
        self.getInfo()

        # 다중 선택 가능한 체크박스
        self.option_label = QLabel("동작 시간대(다중 선택):")
        self.option_checkboxes = []
        for i in range(24):
            checkbox = QCheckBox(f"{i:02d}")
            if i in self.checked_list:
                checkbox.setChecked(True)
            self.option_checkboxes.append(checkbox)

        # 동작하기 버튼
        self.action_button = QPushButton("동작하기")
        self.action_button.clicked.connect(self.action)  # 버튼 클릭 시 action 메소드 실행

        # 만료 일정
        self.expiration_label = QLabel(f"만료일정: {expiration.expiration_date}")

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.id_label)
        layout.addWidget(self.id_input)
        layout.addWidget(self.pw_label)
        layout.addWidget(self.pw_input)
        layout.addWidget(self.max_label)
        layout.addWidget(self.max_input)
        layout.addWidget(self.option_label)

        # 체크박스를 가로로 배열
        for i in range(0, 24, 6):
            hbox = QHBoxLayout()
            hbox.addStretch(1)
            for j in range(i, i + 6):
                hbox.addWidget(self.option_checkboxes[j])
                hbox.addStretch(1)  # 체크박스 간에 공간 추가
            hbox.addStretch(1)
            layout.addLayout(hbox)

        layout.addWidget(self.action_button)  # 동작하기 버튼 추가
        if expiration.expiration_date != "":
            layout.addWidget(self.expiration_label) # 만료일정 추가

        self.setLayout(layout)

    def getInfo(self):
        file_path = os.path.join(os.getcwd(), "savedInfo.txt")
        if os.path.isfile(file_path):
            with open("savedInfo.txt", "r") as f:
                lines = f.readlines()
                self.id_input.setText(lines[0].strip())
                self.pw_input.setText(lines[1].strip())
                self.max_input.setText(lines[2].strip())
                for line in lines[3:]:
                    self.checked_list.append(int(line.strip()))

    def action(self):
        time_list = []
        with open("savedInfo.txt", "w") as f:
            f.write(self.id_input.text() + "\n" + self.pw_input.text() + "\n" + self.max_input.text() + "\n")
            for i, checkbox in enumerate(self.option_checkboxes):
                if checkbox.isChecked():
                    f.write(f"{i}\n")
                    time_list.append(i)
        blog.auto(self.id_input.text(), self.pw_input.text(), time_list, self.max_input.text())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
