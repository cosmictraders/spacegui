class Contract:
    def __init__(self, contract_id, session, update=True):
        self.contract_id = contract_id
        self.session = session
        if update:
            self.update()

    def update(self, data=None):
        if data is None:
            r = self.session.get("https://api.spacetraders.io/v2/my/contracts/" + self.contract_id)
            data = r.json()["data"]
        self.on_accepted = data["terms"]["payment"]["onAccepted"]
        self.on_fulfilled = data["terms"]["payment"]["onFulfilled"]
        self.accepted = data["accepted"]
        self.fulfilled = data["fulfilled"]
        self.deadline = data["terms"]["deadline"]