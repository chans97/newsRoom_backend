class ApiRes:
    def __init__(self):
        self.SUCCESS = False
        self.DATA = {}
        self.ERROR = {}

    def set_success(self, success: bool):
        self.SUCCESS = success

    def update_data(self, data: dict):
        self.DATA.update(data)
    def set_error(self, data: str):
        self.DATA.update({"message":data})
    # deprecated 
    # 어차피 object로 보내도 알아서 json으로 만들어줌
    def to_dict(self):
        return {"SUCCESS": self.SUCCESS, "DATA": self.DATA}
