import struct
import pickle
import netifaces

def get_mac_address():
    interfaces = netifaces.interfaces()
    for interface in interfaces:
        try:
            mac = netifaces.ifaddresses(interface)[netifaces.AF_LINK][0]['addr']
            if mac:
                return mac
        except (KeyError, IndexError):
            continue
    return "00:00:00:00:00:00"

class PhysicalLayer:
    def send(self, data, mac_address):
        bits = ''.join(format(byte, '08b') for byte in data)
        print(f"Physical Layer Sending: {bits} to {mac_address}")
        return bits.encode()
    
    def receive(self, bits):
        bits = bits.decode()
        data = bytes(int(bits[i:i+8], 2) for i in range(0, len(bits), 8))
        print(f"Physical Layer Received: {data}")
        return data

class DataLinkLayer:
    def send(self, data, mac_address):
        frame = b"[MAC_HEADER]" + mac_address.encode() + b"|" + data + b"[MAC_FOOTER]"
        print(f"Data Link Layer Sending: {frame}")
        return frame
    
    def receive(self, frame):
        data = frame.split(b"|")[1].replace(b"[MAC_FOOTER]", b"")
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

    def send_data(self, data, mac_address):
        data = self.application.send(data)
        data = self.presentation.send(data)
        data = self.session.send(data)
        data = self.transport.send(data)
        data = self.network.send(data)
        data = self.datalink.send(data, mac_address)
        data = self.physical.send(data, mac_address)
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
    mac_address = get_mac_address()
    print(f"Using MAC Address: {mac_address}")
    message = input("Enter message to send: ")
    print("\n\n--- Sending Data ---\n")
    osi = OSISimulator()
    transmitted_data = osi.send_data(message, mac_address)
    print("\n\n--- Receiving Data ---\n")
    osi.receive_data(transmitted_data)
