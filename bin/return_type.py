class return_type:
    ret = None
    type = None
    IMG = "IMAGE"
    CSV = "CSV"
    TEXT = "TEXT"
    data = ""

    def __init__(self, ret, type, data=""):
        self.ret = ret
        self.type = type
        self.data = data