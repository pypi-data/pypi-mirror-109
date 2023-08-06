# %%
link = {}
derives = []
eventFormat = 'on_'
messageFormat = 'receive_'
mode = 'implicit'
eventReceipts = {}
messageReceipts = {}

def init(newlink):
    global link
    link = newlink

def alias(func, *names):
    for name in names:
        globals()[name] = lambda *args: func(*args)

def format(event='on_', message='receive_'):
    global eventFormat
    global messageFormat
    eventFormat = event
    messageFormat = message

def eventMode(new):
    global mode
    mode = new

def event_r(eventName, obj):
    global eventReceipts
    if eventName in eventReceipts:
        eventReceipts[eventName].append(obj)
    else:
        eventReceipts[eventName] = [obj]

def message_r(messageName, obj):
    global messageReceipts
    if messageName in messageReceipts:
        messageReceipts[messageName].append(obj)
    else:
        messageReceipts[messageName] = [obj]

def broadcast_change():
    for derive in derives:
        old_val = derive.previous_value
        new_val = derive.get()
        if old_val != new_val:
            derive.run_reacts()

def log1(content):
    print(f'Test2 Changed to {content}')
def log2(content):
    print(f'Test4 Changed to {content}')

class Base:
    def __init__(self, value):
        self.value = value
    def set(self, new):
        self.value = new
        broadcast_change()
    def get(self):
        return self.value

class Derive:
    def __init__(self, source):
        self.source = source
        self.previous_value = self.get()
        derives.append(self)
        self.reacts = []
    def set(self, new):
        self.source = new
    def get(self):
        self.previous_value = self.source()
        return self.source()
    def run_reacts(self):
        for react in self.reacts:
            react(self.get())
    def react(self, new):
        self.reacts.append(new)
        return self
    def react_to_change(self, new):
        self.react(new)

class Receiver:
    pass

def broadcast(event):
    global mode
    global eventFormat
    if mode == 'implicit':
        global link
        funcname = f'{eventFormat}{event}'
        for obj in link:
            if isinstance(link[obj], Receiver):
                if funcname in dir(link[obj]):
                    getattr(link[obj], funcname)()
    elif mode == 'explicit':
        global eventReceipts
        targetReceipt = eventReceipts[event]
        funcname = f'{eventFormat}{event}'
        for obj in targetReceipt:
            if isinstance(obj, Receiver):
                if funcname in dir(obj):
                    getattr(obj, funcname)()

def send(message, data):
    global mode
    global messageFormat
    if mode == 'implicit':
        global link
        funcname = f'{messageFormat}{message}'
        for obj in link:
            if isinstance(link[obj], Receiver):
                if funcname in dir(link[obj]):
                    getattr(link[obj], funcname)(data)
    elif mode == 'explicit':
        global messageReceipts
        targetReceipt = messageReceipts[message]
        funcname = f'{messageFormat}{message}'
        for obj in targetReceipt:
            if isinstance(obj, Receiver):
                if funcname in dir(obj):
                    getattr(obj, funcname)(data)
            
alias(Base, 'atom')
alias(Derive, 'derive')