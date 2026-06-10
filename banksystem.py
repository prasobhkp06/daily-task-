#Bank System: BankAccount class with owner and balance.
#Methods: deposit(amount), withdraw(amount) — 
#raise InsufficientFundsError if balance too low, get_balance(), transaction_history() —
#list of all deposits and withdrawals, __str__. 
#SavingsAccount child class: adds interest_rate, apply_interest() increases balance by rate.
#CurrentAccount child class: adds overdraft_limit, withdraw() allows going negative up to the overdraft limit. 
#Test all methods including error cases.
class InsufficientFundsError(Exception):
    pass


class BankAcc:
    def __init__(self,owner,balance):
        self.owner=owner
        self.balance=balance
        self.transaction=[]
    def deposit(self,amount):
        self.balance+=amount
        a=f"Deposited {amount}"
        self.transaction.append(a)
        return a
    def withdraw(self,amount):
        if self.balance<amount:
            raise InsufficientFundsError("Kaayi nai")
        b=f"withdrawn {amount}"
        self.transaction.append(b)
        self.balance-=amount
        return b
    def get_balance(self):
        return self.balance
    def transaction_history(self):
        print(self.transaction)
    def __str__(self):
        return f"This is {self.owner}'s bank account"
class SavingsAcc(BankAcc):
    def int_rate(self):
        self.interest=self.balance*0.5
    def Apply_interest(self):
        self.balance+=self.interest
class CurrentAcc(BankAcc):
    overdraft_lim=-500
    def withdraw(self,amount):
        if self.balance-amount<self.overdraft_lim:
                return "You hit your OverDraft Limit"
        else:
            self.balance+=amount
    def Balance(self):
        x=f"Your Balance is {self.balance}"
        return x
    

Acc1=BankAcc("Babu",50000)


try:
    print(Acc1.deposit(5000))
    print(Acc1.withdraw(300))
except InsufficientFundsError as e:
    print("Kaayi Illyaa")
else:
    print("success")
finally:
    print("Done")