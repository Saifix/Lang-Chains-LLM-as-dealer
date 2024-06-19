import socketio
import eventlet

# Create a Socket.IO server
sio = socketio.Server(cors_allowed_origins='*')
#sio = socketio.Server(cors_allowed_origins='https://b453-2407-d000-1a-4f3c-bdd6-acb0-f1c8-caf5.ngrok-free.app/')

# Define event handlers
@sio.event
def connect(sid, environ):
    print('Client connected:', sid)

@sio.event
def disconnect(sid):
    print('Client disconnected:', sid)

@sio.event
def echo(sid, data):
    print('Message from client:', data)
    
    if "rating".lower() in data.lower().strip() or "price".lower() in data.lower().strip() or "pricing".lower() in data.lower().strip()  or "rate".lower() in data.lower().strip():
        sio.emit('response', {'data': 'deal done'})  # Emit to the client who sent the message
        print(data)
    else:
        print("Invalid message. Ignoring.")
        # You can send an invalid message back if needed
        # sio.emit('response', {'data': 'Invalid message received.'}, room=sid)


# Create a WSGI application
app = socketio.WSGIApp(sio)

if __name__ == '__main__':
    # Run the server
    eventlet.wsgi.server(eventlet.listen(('localhost', 8756)), app)
