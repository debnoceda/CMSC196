import json
import struct
import pickle

class PhysicalLayer:
    def send(self, data):
        bits = ''.join(format(byte, '08b') for byte in data)
        print(f"Physical Layer Sending: {bits}")
        return bits.encode()
    
    def receive(self, bits):
        bits = bits.decode()
        data = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
        print(f"Physical Layer Received: {data}")
        return data

class DataLinkLayer:
    def send(self, data):
        frame = b"[MAC_HEADER]" + data + b"[MAC_FOOTER]"
        print(f"Data Link Layer Sending: {frame}")
        return frame
    
    def receive(self, frame):
        data = frame.replace(b"[MAC_HEADER]", b"").replace(b"[MAC_FOOTER]", b"")
        print(f"Data Link Layer Received: {data}")
        return data

class NetworkLayer:
    def send(self, data):
        if not isinstance(data, bytes):
            data = data.encode()
        packet = struct.pack('!I', len(data)) + data
        print(f"Network Layer Sending: {packet}")
        return packet
    
    def receive(self, packet):
        length = struct.unpack('!I', packet[:4])[0]
        data = packet[4:4+length]
        print(f"Network Layer Received: {data}")
        return data

class TransportLayer:
    def send(self, data):
        if not isinstance(data, bytes):
            data = data.encode()
        segment = struct.pack('!I', len(data)) + data
        print(f"Transport Layer Sending: {segment}")
        return segment
    
    def receive(self, segment):
        length = struct.unpack('!I', segment[:4])[0]
        data = segment[4:4+length]
        print(f"Transport Layer Received: {data}")
        return data

class SessionLayer:
    def send(self, data):
        session_data = b"[SESSION_START]" + data + b"[SESSION_END]"
        print(f"Session Layer Sending: {session_data}")
        return session_data
    
    def receive(self, session_data):
        data = session_data.replace(b"[SESSION_START]", b"").replace(b"[SESSION_END]", b"")
        print(f"Session Layer Received: {data}")
        return data

class PresentationLayer:
    def send(self, data):
        encoded_data = pickle.dumps(data)
        print(f"Presentation Layer Sending: {encoded_data}")
        return encoded_data
    
    def receive(self, encoded_data):
        data = pickle.loads(encoded_data)
        print(f"Presentation Layer Received: {data}")
        return data

class ApplicationLayer:
    def send(self, data):
        print(f"Application Layer Sending: {data}")
        return data
    
    def receive(self, data):
        print(f"Application Layer Received: {data}")
        return data

class OSISimulator:
    def __init__(self):
        self.application = ApplicationLayer()
        self.presentation = PresentationLayer()
        self.session = SessionLayer()
        self.transport = TransportLayer()
        self.network = NetworkLayer()
        self.datalink = DataLinkLayer()
        self.physical = PhysicalLayer()

    def send_data(self, data):
        data = self.application.send(data)
        data = self.presentation.send(data)
        data = self.session.send(data)
        data = self.transport.send(data)
        data = self.network.send(data)
        data = self.datalink.send(data)
        data = self.physical.send(data)
        return data

    def receive_data(self, data):
        data = self.physical.receive(data)
        data = self.datalink.receive(data)
        data = self.network.receive(data)
        data = self.transport.receive(data)
        data = self.session.receive(data)
        data = self.presentation.receive(data)
        data = self.application.receive(data)
        return data

if __name__ == "__main__":
    osi = OSISimulator()
    transmitted_data = osi.send_data("Hello, World!")
    print("\n--- Receiving Data ---\n")
    osi.receive_data(transmitted_data)
