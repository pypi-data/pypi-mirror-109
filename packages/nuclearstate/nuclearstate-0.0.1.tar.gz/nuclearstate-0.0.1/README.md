# Nuclear - Reactive state management for python

## Atoms and Derives

The base element in nuclear is called an atom. You can create one with `atom({starting value})`.

To create a derivative of an atom (or of another derivative) you can user the `derivative({source})` function.

To get or set any atoms or derivatives, you can use the `.set()` and `.get()` methods.

To add reactions to changed, you can use the `.react()` method.

Example program:

```
base = atom(10) #Creates an atom with value 10
derived = derive(lambda: base.get() * 2) #Creates a derive which will always be equal to base * 2
derived.react(lambda: print('The value of derived was changed))

print(base.get()) # prints 10
print(derived.get()) # prints 20

base.set(20) # prints 'The value of derived was changed'
print(derived.get()) # prints 40
```

## Events and Messages

To allow nuclear to implicitly send events and message, you must initialise it with `nuclear.init(globals())`.

To create a class that can recieve and send messages, it needs to inherit from `Receiver`.

To respond to events or messages, you can add methods to your class that follow the format:

For events, `on_{your event name}`

For messages, `receive_{your message name}`

Then to send events and messages you can use:

For events, `broadcast({your event name})`

For messages, `send({your message name}, {data})`

Example program:

```
nuclear.init(globals())

class TestClass(Receiver):
    def __init__(self):
        pass
    def on_TestEvent(self):
        print('Test Event received')
    def receive_TestMessage(self, data):
        print(f'TestMessage sent data {data}')

test1 = TestClass()

broadcast('TestEvent') # prints 'Test Event received'
send('TestMessage', 200) # prints 'TestMessage sent data 200'
```

You can also change the format with `nuclear.format({events}, {messages})`.

For better performance, you can change to explicit mode with `nuclear.eventMode('explicit')`. If you do this, you must tag every object that will receive an event or message with `nuclear.event_r({event name}, {object})` or `nuclear.message_r({message name}, {object})`.