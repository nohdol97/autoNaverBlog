import sys, os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QCheckBox, QTextEdit
import blog
import expiration

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AutoBlog copyright © Gmail : nohdol97")
        self.setGeometry(100, 100, 1300, 400)

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

        # 여러 줄의 텍스트를 입력할 수 있는 공간
        self.comment1_label = QLabel("댓글 1")
        self.text_area1 = QTextEdit()
        self.comment2_label = QLabel("댓글 2")
        self.text_area2 = QTextEdit()
        self.getComment()

        # 저장하기 버튼
        self.save_button = QPushButton("저장하기")
        self.save_button.clicked.connect(self.saveComment)  # 버튼 클릭 시 action 메소드 실행

        # 댓글을 작성할지 랜덤값(작성할 확률)
        self.random_rate_label = QLabel("댓글작성 확률(%):")
        self.random_rate_input = QLineEdit()
        self.random_rate_input.setText("100")  # Allow only numbers

        # 체크박스: isSecret
        self.is_secret_checkbox = QCheckBox("비밀댓글 적용 여부(30% 확률)")
        self.is_secret_checkbox.setChecked(False)  # Default value

        # 체크박스: isUnNewPost
        self.is_unNewPost_checkbox = QCheckBox("게시글 하루 3개 이상 이웃 새글 보지 않기")
        self.is_unNewPost_checkbox.setChecked(True)  # Default value

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

        layout.addWidget(self.random_rate_label)
        layout.addWidget(self.random_rate_input)
        layout.addWidget(self.is_secret_checkbox)
        layout.addWidget(self.is_unNewPost_checkbox)

        layout.addWidget(self.action_button)  # 동작하기 버튼 추가
        if expiration.expiration_date != "":
            layout.addWidget(self.expiration_label) # 만료일정 추가

        # 기존 레이아웃과 텍스트 영역을 가로로 배치
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()  # 텍스트 영역을 세로로 배치
        vbox.addWidget(self.comment1_label)
        vbox.addWidget(self.text_area1)  # 텍스트 영역 1 추가
        vbox.addWidget(self.comment2_label)
        vbox.addWidget(self.text_area2)  # 텍스트 영역 2 추가
        vbox.addWidget(self.save_button)
        hbox.addLayout(layout)  # 기존 레이아웃 추가
        hbox.addLayout(vbox)  # 텍스트 영역 추가

        self.setLayout(hbox)  # 가로 레이아웃 설정

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

    def getComment(self):
        file_path = os.path.join(os.getcwd(), "commentList1.txt")
        if os.path.isfile(file_path):
            with open("commentList1.txt", "r", encoding='utf-8') as f:
                lines = f.readlines()
                self.text_area1.setText(''.join(f"{line}" for line in lines))
        file_path = os.path.join(os.getcwd(), "commentList2.txt")
        if os.path.isfile(file_path):
            with open("commentList2.txt", "r", encoding='utf-8') as f:
                lines = f.readlines()
                self.text_area2.setText(''.join(f"{line}" for line in lines))

    def action(self):
        time_list = []
        random_rate = float(self.random_rate_input.text()) / 100  # 숫자로 변환
        is_secret = self.is_secret_checkbox.isChecked()   # 체크 여부 확인
        is_unNewPost = self.is_unNewPost_checkbox.isChecked()
        with open("savedInfo.txt", "w") as f:
            f.write(self.id_input.text() + "\n" + self.pw_input.text() + "\n" + self.max_input.text() + "\n")
            for i, checkbox in enumerate(self.option_checkboxes):
                if checkbox.isChecked():
                    f.write(f"{i}\n")
                    time_list.append(i)
            f.write()
        blog.auto(self.id_input.text(), self.pw_input.text(), time_list, self.max_input.text(), random_rate, is_secret, is_unNewPost)
    
    def saveComment(self):
        with open("commentList1.txt", "w", encoding='utf-8') as f:
            f.write(self.text_area1.toPlainText())
        with open("commentList2.txt", "w", encoding='utf-8') as f:
            f.write(self.text_area2.toPlainText())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
