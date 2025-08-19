class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
    
    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
    
    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False
    
    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)
    
    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False
    
    def check_funds(self, amount):
        return amount <= self.get_balance()
    
    def __str__(self):
        title = f"{self.name:*^30}"
        items = "\n".join(f"{item['description'][:23]:23}{item['amount']:7.2f}" for item in self.ledger)
        total = f"Total: {self.get_balance():.2f}"
        return f"{title}\n{items}\n{total}"

def create_spend_chart(categories):
    spent = [{"name": cat.name, "amount": sum(-item["amount"] for item in cat.ledger if item["amount"] < 0)} for cat in categories]
    total_spent = sum(item["amount"] for item in spent)
    
    if total_spent == 0:
        percentages = [0] * len(categories)
    else:
        percentages = [int((item["amount"] / total_spent) * 100 // 10) * 10 for item in spent]
    
    chart = "Percentage spent by category\n"
    for i in range(100, -1, -10):
        chart += f"{i:>3}| " + "  ".join("o" if percent >= i else " " for percent in percentages) + "  \n"
    
    chart += "    " + "-" * (len(categories) * 3 + 1) + "\n"
    
    max_len = max(len(cat.name) for cat in categories)
    names = [cat.name.ljust(max_len) for cat in categories]
    
    for i in range(max_len):
        chart += "     " + "  ".join(name[i] for name in names) + "  \n"
    
    return chart.rstrip() + "  "