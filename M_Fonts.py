from PySide6.QtGui import QFont

def MyFont(size: int  = 10, bold: bool = False):
    Font = QFont()
    Font.setPointSize(size)
    Font.setBold(bold)
    Font.setFixedPitch(True)
    
    return Font